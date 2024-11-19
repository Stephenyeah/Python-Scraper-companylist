import requests
import pandas as pd
import time

# List of countries to filter
countries = ['bulgaria', 'croatia', 'hungary', 'romania', 'serbia', 'czech-republic', 'poland', 'ukraine']

# Keywords for filtering
keywords = ['import', 'export']

def get_companies_from_page(page):
    url = "https://avoindata.prh.fi/opendata-ytj-api/v3/all_companies"
    params = {
        "page": page  # API supports pagination, passing the current page number
    }
    response = requests.get(url, params=params)

    # Check if request was successful
    if response.status_code == 200:
        if response.text:  # Check if response text is not empty
            data = response.json()  # Parse JSON response
            return data['data']  # Adjust based on actual structure
        else:
            print("Empty response received.")
            return None
    else:
        print(f"Failed to fetch data for page {page}. Status Code: {response.status_code}, Response: {response.text}")
        return None

def contains_keyword(company_name):
    """Check if company name contains any of the keywords."""
    return any(keyword in company_name.lower() for keyword in keywords)

def scrape_companies(max_pages=20):
    all_companies = []

    for page in range(1, max_pages + 1):
        print(f"Scraping page {page}...")
        data = get_companies_from_page(page)
        
        if data is None or len(data) == 0:
            print("No more data available or error occurred.")
            break
        
        for company in data:
            company_country = company.get('country', '').lower()  # Convert to lowercase for comparison
            company_name = company.get('name', '').lower()  # Convert name to lowercase for keyword checking

            # Check if the company is in one of the specified countries or contains import/export keywords
            if company_country in countries or contains_keyword(company_name):
                all_companies.append({
                    'Name': company.get('name', ''),
                    'City': company.get('city', ''),
                    'Country': company_country,
                    'CompanyForm': company.get('companyForm', '')
                })
        
        time.sleep(1)  # Delay between requests to avoid hitting rate limits
    
    return all_companies

# Scrape company data
companies = scrape_companies(max_pages=10)

# Convert to a pandas DataFrame and export to CSV
df = pd.DataFrame(companies)
df.to_csv('filtered_import_export_companies.csv', index=False)

print("Scraping completed and filtered data saved to 'filtered_import_export_companies.csv'.")
