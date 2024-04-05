# Imports
import os
import time
import random
import requests
from bs4 import BeautifulSoup

# Define the function to fetch HTML content
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching HTML content for {url}: {e}")
        return None

# Define function to scrape the site structure
def scrape_site_structure(url):
    try:
        html = fetch_html(url)
        if html:
            return html
    except Exception as e:
        print(f"Error scraping site structure for {url}: {e}")
    return None

# Define function to save HTML content to HTML file with formatting
def save_html_to_file(html_content, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)
        print(f"HTML content saved to {file_path}")
    except Exception as e:
        print(f"Error saving HTML content to {file_path}: {e}")

# Main function
def main():
    # List of URLs to scrape
    urls = [
    "https://www.gocart.ph/shopwise?buId=1&zoneNum=16&selected=all", 
    "https://www.gocart.ph/robinsons-supermarket?buId=1&zoneNum=9&selected=all"
    ]
    
    # Directory to save HTML files
    output_directory = "html_files"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate over URLs and scrape site structure
    for idx, url in enumerate(urls, start=1):
        print(f"Scraping website {idx}/{len(urls)}: {url}")
        html_content = scrape_site_structure(url)
        
        # Save HTML content to HTML file
        file_name = f"website_{idx}.html"
        file_path = os.path.join(output_directory, file_name)
        if html_content:
            save_html_to_file(html_content, file_path)
        else:
            print(f"Failed to scrape {url}")

        time.sleep(random.uniform(1, 2))  # Add a delay between requests to avoid overloading the server

if __name__ == "__main__":
    main()