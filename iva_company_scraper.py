#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
from typing import Optional, Dict
import re
from dotenv import load_dotenv
import os

class CompanyScraper:
    def __init__(self, api_key: str, cse_id: str):
        self.api_key = api_key
        self.cse_id = cse_id
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.base_google_url = "https://www.googleapis.com/customsearch/v1"

    def google_search(self, query: str) -> Optional[str]:
        """Performs a Google search and returns the first valid link."""
        params = {
            'q': query,
            'key': self.api_key,
            'cx': self.cse_id,
            'num': 1
        }
        try:
            response = requests.get(self.base_google_url, params=params, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get('items', [{}])[0].get('link')
        except requests.RequestException as e:
            print(f"Error in Google search: {e}")
            return None

    def get_html(self, url: str) -> Optional[str]:
        """Downloads the page HTML and returns it as a string."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error downloading page: {e}")
            return None

    def get_canonical_url(self, soup: BeautifulSoup) -> str:
        """Extracts the canonical URL from the <link rel='canonical'> tag if present."""
        link = soup.find("link", rel="canonical")
        return link["href"] if link and link.has_attr("href") else ""

    def get_field(self, soup: BeautifulSoup, field_id: str) -> str:
        """Returns the text of the element identified by field_id or an empty string."""
        element = soup.find(id=field_id)
        return element.get_text(strip=True) if element else ""

    def scrape_company_data(self, html_content: str, url: str) -> Dict:
        """Scrapes company data from HTML and returns a formatted dictionary."""
        soup = BeautifulSoup(html_content, 'html.parser')
        company_data = {
            "company": {
                "vat_number": "",
                "website_url": url,
                "company_name": "",
                "ateco_description": "",
                "ateco_code": "",
                "share_capital": "",
                "employees": "0",
                "company_registration_date": "",
                "legal_form": ""
            }
        }
        
        # Update website URL with canonical link if present
        canonical = self.get_canonical_url(soup)
        if canonical:
            company_data["company"]["website_url"] = canonical

        # Extract data from JSON-LD if present
        json_ld_script = soup.find('script', type='application/ld+json', string=re.compile('"Organization"'))
        if json_ld_script:
            try:
                json_data = json.loads(json_ld_script.string)
                if isinstance(json_data, dict) and json_data.get("@type") == "Organization":
                    company_data["company"]["vat_number"] = json_data.get("vatID", "")
                    company_data["company"]["company_name"] = json_data.get("name", "")
                    company_data["company"]["company_registration_date"] = json_data.get("foundingDate", "")
                    company_data["company"]["employees"] = json_data.get("numberOfEmployees", "0")
                    company_data["company"]["ateco_code"] = json_data.get("isicV4", "")
            except Exception as e:
                print(f"Error parsing JSON-LD: {e}")

        # Extract visible data from the page
        vat = self.get_field(soup, "field_piva")
        if vat:
            if not vat.startswith("IT"):
                vat = "IT" + vat
            company_data["company"]["vat_number"] = vat

        company_data["company"]["company_name"] = self.get_field(soup, "field_denominazione") or company_data["company"]["company_name"]
        company_data["company"]["ateco_description"] = self.get_field(soup, "field_desc_ateco")
        company_data["company"]["ateco_code"] = self.get_field(soup, "field_ateco") or company_data["company"]["ateco_code"]
        share_capital = self.get_field(soup, "field_capitale_sociale")
        if share_capital:
            company_data["company"]["share_capital"] = share_capital.replace('€', '').replace('\xa0', '').strip()
        company_data["company"]["employees"] = self.get_field(soup, "field_addetti") or company_data["company"]["employees"]
        company_data["company"]["company_registration_date"] = self.get_field(soup, "field_data") or company_data["company"]["company_registration_date"]
        company_data["company"]["legal_form"] = self.get_field(soup, "field_formagiuridica")
        
        return company_data

    def get_company_info(self, vat_number: str) -> str:
        """
        Main method:
          1. Performs a Google search on ufficiocamerale.it using the VAT number
          2. Downloads the HTML of the first page found
          3. Scrapes to extract company data
          4. Returns formatted JSON
        """
        query = f'IVA {vat_number} site:ufficiocamerale.it'
        first_link = self.google_search(query)
        
        if not first_link:
            return json.dumps({"error": "No results found on UfficioCamerale.it"}, indent=2)
        
        html_content = self.get_html(first_link)
        if not html_content:
            return json.dumps({"error": "Unable to download the page"}, indent=2)
        
        company_data = self.scrape_company_data(html_content, first_link)
        return json.dumps(company_data, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Get API credentials from environment variables
    API_KEY = os.getenv('GOOGLE_API_KEY')
    CSE_ID = os.getenv('GOOGLE_CSE_ID')
    VAT_NUMBER = '07727071008'

    if not all([API_KEY, CSE_ID]):
        print("Error: Missing API credentials in .env file")
        exit(1)

    scraper = CompanyScraper(API_KEY, CSE_ID)
    result = scraper.get_company_info(VAT_NUMBER)
    print(result)
