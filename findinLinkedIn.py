import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# Load the CSV file
df = pd.read_csv('filtered_import_export_companies_with_website.csv',on_bad_lines='skip')

# Set up the WebDriver using ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# LinkedIn URL
linkedin_url = "https://www.linkedin.com/login"

# Log in to LinkedIn (provide your credentials)
def login_to_linkedin():
    driver.get(linkedin_url)
    time.sleep(2)
    
    # Find username and password fields and log in
    username_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")
    
    # Replace with your actual LinkedIn credentials
    username_input.send_keys('arogon21@gmail.com')  # Your LinkedIn email
    password_input.send_keys('7758258@Yyq')  # Your LinkedIn password
    password_input.send_keys(Keys.RETURN)
    
    time.sleep(5)  # Wait for the login to complete

        # Click the accept button for cookies or any pop-up
    try:
        accept_button = driver.find_element(By.XPATH, '//button[text()="Accept"]')  # Adjust the XPath if necessary
        accept_button.click()
        print("Clicked the accept button.")
    except Exception as e:
        print("No accept button found or another issue:", e)
    

# Search for companies on LinkedIn
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_companies(company_name):
    search_box = driver.find_element(By.XPATH, '//input[contains(@placeholder, "Search")]')
    search_box.clear()
    search_box.send_keys(company_name)
    search_box.send_keys(Keys.RETURN)

    # Explicit wait for search results
    try:
        # Wait for the search results container to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//ul[contains(@class, "reusable-search__entity-result-list")]'))
        )

        results_container = driver.find_element(By.XPATH, '//ul[contains(@class, "reusable-search__entity-result-list")]')
        results = results_container.find_elements(By.XPATH, './/li')

        for result in results:
            result_text = result.text.lower()
            if company_name.lower() in result_text:
                return True

    except Exception as e:
        print(f"Error while searching for {company_name}: {e}")
        print(driver.page_source)  # For debugging

    return False

# Main function
def main():
    login_to_linkedin()
    
    found_companies = []
    
    for index, row in df.iterrows():
        company_name = row['Name']
        print(f"Searching for: {company_name}")
        
        if search_companies(company_name):
            print(f"Found: {company_name}")
            found_companies.append(company_name)
        else:
            print(f"Not found: {company_name}")
    
    # Save the found companies to a new CSV file
    pd.DataFrame(found_companies, columns=['Found Companies']).to_csv('found_companies_on_linkedin.csv', index=False)
    print("Search completed. Found companies saved to 'found_companies_on_linkedin.csv'.")
    
    driver.quit()

if __name__ == "__main__":
    main()



