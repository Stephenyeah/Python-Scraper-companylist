import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_company_data(country, page):
    # Replace with the business directory URL you are scraping
    url = f"https://avoindata.prh.fi/opendata-ytj-api/v3/all_companies"
    
    # Send GET request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve data from {url}")
        return []
    
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find company details based on HTML structure (you need to inspect the page for actual tags)
    company_list = []
    
    # This is an example, update according to the actual site structure
    companies = soup.find_all('div', class_='company-profile')
    for company in companies:
        name = company.find('h2', class_='company-name').text.strip()
        address = company.find('div', class_='company-address').text.strip()
        contact = company.find('div', class_='company-contact').text.strip()
        
        company_list.append({
            'Name': name,
            'Address': address,
            'Contact': contact,
        })
    
    return company_list

def scrape_companies_for_countries(countries, max_pages=5):
    all_companies = []
    
    # Loop through each country and scrape data
    for country in countries:
        print(f"Scraping companies in {country}...")
        for page in range(1, max_pages + 1):
            companies = get_company_data(country, page)
            if not companies:
                break
            all_companies.extend(companies)
    
    return all_companies



# Define the list of countries
countries = ['bulgaria', 'croatia', 'hungary', 'romania', 'serbia', 'czech-republic', 'poland', 'ukraine']

# Scrape data for the countries
companies = scrape_companies_for_countries(countries)

# Save the data to a CSV file
df = pd.DataFrame(companies)
df.to_csv('company_data.csv', index=False)

print("Data scraping completed and saved to company_data.csv")
