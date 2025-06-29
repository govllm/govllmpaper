from langchain.docstore.document import Document
import pandas as pd
import hashlib


def add_to_database(documents_set, file_path, columns_to_embed, columns_to_metadata,
                    retriever, chunk_size=1000, unique_identifier="documentId",
                    ):
    """
    Add documents from a CSV file to a database collection.
    """
    counter = 1

    # loop over the csv in chunks
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        # preprocess the chunk
        chunk.astype(str)

        # check if there are any new documents in the chunk, skip if not
        new_rows = set(chunk[unique_identifier]) - documents_set

        # if to_process.empty:
        if len(new_rows) == 0:
            print(f"Chunk {counter}: only duplicates, skipping to next chunk...")
            counter += 1
            # continue to next chunk
            continue

        # make list of content to process
        to_process = chunk[chunk[unique_identifier].isin(new_rows)]

        # print number of new documents
        print(f"Chunk {counter}: processing {len(to_process)} new documents...")

        # make list of content and metadata to make embeddings
        to_metadata = [{col: row[col] for col in columns_to_metadata} for index, row in to_process.iterrows()]
        to_content = ["\n".join(str(row[col]).strip() for col in columns_to_embed) for index, row in
                      to_process.iterrows()]

        # create document of the to_metadata and to_content without splitting
        documents = []
        for i in range(len(to_content)):
            document = Document(
                page_content=to_content[i],
                metadata=to_metadata[i]
            )
            documents.append(document)

        # add documents to the collection using the child splitter,
        # 40000 is the maximum number of embeddings that can be added at once
        for i in range(0, len(documents), 40000):
            retriever.add_documents(ids=None,
                                    documents=documents)

        # add documents in the chunk to the set
        documents_set.update(to_process[unique_identifier].values)
        counter += 1


def main_to_database(collection, file_path, columns_to_embed, columns_to_metadata,
                     retriever, unique_identifier, chunk_size=1000):
    """
    Add documents from a CSV file to a database collection.
    """

    # make a set of all documents already in the database
    print("Getting existing documents from the database...")
    documents_set = {i[unique_identifier] for i in collection.get().get("metadatas", {})}

    # add documents to the database
    add_to_database(documents_set, file_path, columns_to_embed, columns_to_metadata,
                    retriever, chunk_size, unique_identifier)
