# Imports
import os
import pandas as pd
import time
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Define the infinite scrolling function
def scroll_page(driver):
    try:
        # Execute slow loading to properly load all the elements including images
        last_height = driver.execute_script("return document.body.scrollHeight")

        current_scroll = 0
        while current_scroll < last_height:
            current_scroll += 5
            driver.implicitly_wait(5)
            driver.execute_script("window.scrollTo(0, {});".format(current_scroll))
            
            # Update the last height of scrolling
            last_height = driver.execute_script("return document.body.scrollHeight")
            
    except Exception as e:
        print(f"An error occurred while scrolling: {e}")

    return driver

# Define function for scraper
def scrape_search_results(keyword):
    start_time = time.time()
    driver = None
    
    # Initialize the empty dictionary
    results_data = {
                    "keyword": [],
                    "website_link": [],
                    "website_title": [],
                    "description": []
                }
                
    try:
        # Start the webdriver
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        
        # Maximize the browser window
        driver.maximize_window()

        # Open Google search
        driver.get("https://www.google.com/")

        # Find the search bar and input the keyword
        search_box = driver.find_element(By.XPATH, "//*[@id='APjFqb']")
        #search_box = driver.find_element_by_name("q")

        # Input the keyword
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        # Wait for search results to load
        sleep_time = random.uniform(1, 2)
        time.sleep(sleep_time)

        try:
            # Slow scrolling
            scroll_page(driver)

            # Get the HTML of the search results page
            html = driver.page_source

            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")
                
            # Find all search result titles and descriptions
            search_results = soup.find_all("div", class_="tF2Cxc")
            print("Located all website elements")

            try:
                # Extract titles and descriptions
                for result in search_results:
                    # Find the website links
                    links = result.select('div.yuRUbf a')

                    # Extract the result title
                    website_title_element = result.find("h3")
                    website_title = website_title_element.text if website_title_element else None

                    # Extract the description snippet
                    description_element = result.find("div", class_="VwiC3b yXK7lf lVm3ye r025kc hJNv6b Hdw6tb")
                    description = description_element.text if description_element else None

                    # Append the data to the dictionary
                    if links:
                        for link_element in links:
                            link = link_element.get('href')
                            results_data["website_link"].append(link)
                            results_data["website_title"].append(website_title)
                            results_data["description"].append(description)
                    else:
                        results_data["website_link"].append(None)
                        results_data["website_title"].append(website_title)
                        results_data["description"].append(description)

                    sleep_time = random.uniform(1, 2)
                    time.sleep(sleep_time)

            except:
                pass
                
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Scroll Exception: {e}")

            # Find the "Next" button and click it to go to the next page
            #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='botstuff']/div/div[3]/div[4]/a[1]/h3/div")))
            #next_button = driver.find_element_by_xpath(xpath="//*[@id='botstuff']/div/div[3]/div[4]/a[1]/h3/div")
                    
            #if next_button.is_enabled():
            #    next_button.click()
            #    time.sleep(2)
            #    scroll_page(driver)
                
            #else:
            #    break

    except (TimeoutException, NoSuchElementException) as e:
        print(f"Driver Exception: {e}")

    finally:
        # Close the browser
        driver.quit()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Scraping time for '{keyword}': {elapsed_time:.2f} seconds")

    return results_data


def main(keywords):
    # Specify the full path for the output file
    output_file_path = "C:\DAVI\webscraper_sample_project\sample_scrape.csv"

    # Check if the output file exists
    if not os.path.exists(output_file_path):
        # If the file does not exist, create an empty CSV file with headers
        with open(output_file_path, 'w', newline='') as f:
            f.write("keyword,website_link,website_title,description\n")

    # Scrape search results for each keyword
    for keyword in keywords:
        print(f"Scraping search results for '{keyword}'...")
        results = scrape_search_results(keyword)
        
        # Append the keyword in the dict
        results["keyword"] = [keyword] * len(results["website_link"])

        # Check
        print(len(results["website_link"]))
        print(len(results["website_title"]))
        print(len(results["description"]))

        # Convert the dictionary to DataFrame and transpose it to have keys as columns
        #new_dict = dict([(key, pd.Series(value)) for key, value in results.items()])
        df = pd.DataFrame(results)

        # Fill the keyword nulls
        #df["keyword"] = df["keyword"].fillna(method="ffill")

        # Drop the null rows without description
        df = df.dropna(subset=["description"])

        # Append the empty list
        #df_list.append(df)

        # Concatenate teh list of dfs
        #final_df = pd.concat(df_list, ignore_index=True)

        # Append the DataFrame to the CSV file
        df.to_csv(output_file_path, mode='a', index=False, header=False)
        print("==========================================")
        print("SUCCESSFULLY SAVED A DATAFRAME AS CSV!!")
        print("==========================================")

def main():
    with open("C:\DAVI\webscraper_sample_project\input_data\search.txt", "r") as file:
        urls = file.readlines()
        for url in urls:
            url = url.strip()
            scrape_search_results(url)

if __name__ == "__main__":
    main()