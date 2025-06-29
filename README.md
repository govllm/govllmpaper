# LLM4GovTracking Project

## Overview
This repository contains a comprehensive toolkit for operationalizing Government Technology (GovTech) benchmarks using Large Language Models (LLMs). It spans the full lifecycle of GovTech framework benchmarking, from data scraping and cleaning to generating prompts and operationalizing benchmarks with LLMs.

## Installation
To set up the project, ensure you have Python installed, then run the following commands:
```bash
git clone https://github.com/govllm/govllmpaper
```

To install the requirements:

```bash
pip install -r requirements.txt
```

## Usage
Each document in the repo includes specific guidelines on its use. 

## Directory Structure

- **Data Processing:** Converts raw data into a structured format suitable for retrieval-augmented generation, using ChromaDB vector databases.
- **Data Scraping:** Scripts to extract data from various sources like the Dutch Government Open Data Portal, Tendernet, Binnenlands Bestuur and iBestuur.
- **Evaluation:** Analyzes outcomes and generates visualizations to demonstrate the model's accuracy in applying the GTMI-benchmark.
- **Model Finetuning:** Contains the scripts to finetune the base LLM.