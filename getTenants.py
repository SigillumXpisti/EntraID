import requests
import csv

filename = "C:\\temp\\domains_you_own.csv"

def load_csv_to_json(filename):
    with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
        return [row for row in csv.DictReader(csvfile)]

def get_tenant(domain):
    url1 = f"https://login.microsoftonline.com/common/userrealm/{domain}?api-version=2.1"
    url2 = f"https://login.microsoftonline.com/{domain}/.well-known/openid-configuration"
    
    response1 = requests.get(url1)
    response2 = requests.get(url2)

    if response1.ok and response2.ok:
        data1 = response1.json()
        data2 = response2.json()
        
        federation_brand_name = data1.get('FederationBrandName')
        token_endpoint = data2.get('token_endpoint')
        tenant_id = token_endpoint.split("/")[3] if token_endpoint else None
        tenant_region_scope = data2.get('tenant_region_scope')

        if tenant_id:
            print(f"{domain};{federation_brand_name};{tenant_id};{tenant_region_scope}")

# Load domain names from CSV
json_array = load_csv_to_json(filename)

# Fetch tenant information for each domain
for line in json_array:
    get_tenant(line['Domain Name'])
