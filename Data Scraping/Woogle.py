import requests
import os
import gzip
import shutil
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from pathlib import Path

password = 'qIc*F5lL(JrW'
login_url = 'https://surfdrive.surf.nl/files/index.php/s/NEpv6uiFwvigxqx/authenticate'

template_url = "https://surfdrive.surf.nl/files/index.php/s/NEpv6uiFwvigxqx/download?path=%2F&files={resource}.csv.gz"
urls = [
    # bodytext database
    template_url.format(resource='woo_bodytext_2k'),

    # dossiers database
    template_url.format(resource='woo_dossiers'),

    # documents database
    template_url.format(resource='woo_documents'),
]

# create folder if it does not yet exist
Path('../Data/Woogle').mkdir(parents=True, exist_ok=True)


def download_file(login_url, download_url):
    # make a session to keep the connection alive
    with requests.session() as session:
        response = session.get(login_url).text
        html = BeautifulSoup(response, 'html.parser')
        token = html.find("input", {"name": "requesttoken"})['value']

        payload = {
            'password': password,
            'requesttoken': token
        }

        # login to the server
        response = session.post(login_url, data=payload)
        response.raise_for_status()  # check for HTTP errors during login

        # download the file
        print('downloading file...')
        response = session.get(download_url)
        response.raise_for_status()  # check for HTTP errors during download

        # save the file
        print('saving file...')
        target_path = str('../Data/Woogle/' + download_url.split('=')[-1])
        with open(target_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=10 * 1024):
                f.write(chunk)

    # # unzip the file
    # print('unzipping file...')
    # file_name = target_path.replace('.gz', '')
    # with gzip.open(target_path, 'rb') as f_in:
    #     with open(file_name, 'wb') as f_out:
    #         shutil.copyfileobj(f_in, f_out)

    # remove the .gz file
    # os.remove(target_path)


if __name__ == '__main__':
    # use ThreadPoolExecutor to download multiple files at once
    with ThreadPoolExecutor() as executor:
        executor.map(download_file, [login_url] * len(urls), urls)
        executor.shutdown(wait=True, cancel_futures=False)
