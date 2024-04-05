# Web Scraping Project

This project contains a simple web scraping script written in Python.

## Usage

1. Clone this repository.
2. Install dependencies using `pip install -r src/requirements.txt`.
3. Place the URLs to be scraped in `input_data/urls.txt`.
4. Run the scraper script locally: `python src/scraper.py`.

## Running with Azure Databricks Workflow

To run the scraper using Azure Databricks Workflow:

1. Create an Azure Databricks cluster.
2. Set up your Databricks workspace and obtain an access token.
3. Update `config/databricks_config.yaml` with your workspace URL, access token, and cluster ID.
4. Create a Databricks notebook to run the script and schedule it using Azure Databricks Workflow.