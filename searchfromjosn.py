import json
import pandas as pd

# Load the downloaded JSON file with specified encoding
with open('all_companies.json', 'r', encoding='utf-8', errors='ignore') as f:
    data = json.load(f)

# List of countries to filter
countries = ['bulgaria', 'croatia', 'hungary', 'romania', 'serbia', 'czech-republic', 'poland', 'ukraine']

# Keywords for filtering
keywords = ['import', 'export']

def contains_keyword(company_names):
    """Check if any company name contains any of the keywords."""
    return any(keyword in name['name'].lower() for name in company_names for keyword in keywords)

# Filter companies based on the criteria
filtered_companies = []

for company in data:  # Iterate directly over the list
    # Check if mainBusinessLine exists and is not None
    main_business_line = company.get('mainBusinessLine')
    company_country = ''
    
    if main_business_line and 'descriptions' in main_business_line:
        company_country = main_business_line['descriptions'][0].get('description', '').lower()

    company_names = company.get('names', [])
    website = company.get('website', {}).get('url', '') if company.get('website') else ''

    # Check if the company belongs to specified countries, contains the keywords, and has a website
    if (any(country in company_country for country in countries) or contains_keyword(company_names)) and website:
        filtered_companies.append({
            'Name': company_names[0]['name'] if company_names else '',  # Get the first name if available
            'Website': website,
            'Main Business Line': main_business_line['type'] if main_business_line else '',
        })

# Convert to a pandas DataFrame and export to CSV
df = pd.DataFrame(filtered_companies)
df.to_csv('filtered_import_export_companies_with_website.csv', index=False)

print("Filtering completed and filtered data saved to 'filtered_import_export_companies_with_website.csv'.")
