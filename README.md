# Italian Company Information Scraper

This Python script allows you to retrieve Italian company information by searching with VAT numbers (Partita IVA) and/or company names. It scrapes data from ufficiocamerale.it through Google Custom Search API.

## Features

- Flexible search options:
  - Search by VAT number (Partita IVA)
  - Search by company name
  - Search using both VAT number and company name
- Extracts comprehensive company data:
  - Company name
  - VAT number
  - ATECO code and description
  - Share capital
  - Number of employees
  - Company registration date
  - Legal form
- Uses Google Custom Search API for accurate results
- Secure credential management through environment variables

## Prerequisites

- Python 3.6 or higher
- Google Custom Search API credentials (API Key and Search Engine ID)

## Setup

1. Clone the repository:

```bash
git clone https://github.com/david-rox-387/IVA_SCRAPER.git
cd IVA_SCRAPER
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Set up Google Custom Search API:

   - Visit [Google Custom Search API Documentation](https://developers.google.com/custom-search/v1/overview)
   - Create a new project in Google Cloud Console
   - Enable Custom Search API
   - Create API credentials (API Key)
   - Create a new search engine at [Programmable Search Engine](https://programmablesearchengine.google.com/about/)
   - Get your Search Engine ID (cx)
   - In the search engine settings, make sure to:
     - Set it to search the entire web
     - Add `ufficiocamerale.it` to the sites to search
4. Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_api_key_here
GOOGLE_CSE_ID=your_search_engine_id_here
```

## Usage

The script provides multiple ways to search for company information:

```python
from iva_company_scraper import CompanyScraper
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize scraper
scraper = CompanyScraper(
    api_key=os.getenv('GOOGLE_API_KEY'),
    cse_id=os.getenv('GOOGLE_CSE_ID')
)

# Search methods:

# 1. Search by VAT number only
result = scraper.get_company_info("07727071008")
print(result)

# 2. Search by company name only
result = scraper.get_company_info("COMPANY SRL")
print(result)

# 3. Search by both name and VAT number
result = scraper.get_company_info("COMPANY SRL 07727071008")
print(result)
```

## Search Parameters

The `get_company_info` method is flexible and accepts:

- VAT number only: `"07727071008"`
- Company name only: `"COMPANY SRL"`
- Combined search: `"COMPANY SRL 07727071008"`

The search will use the provided information to find the most relevant company data. When using both name and VAT number, the search is typically more accurate.

## Response Format

The script returns a JSON string with the following structure:

```json
{
  "company": {
    "vat_number": "IT07727071008",
    "website_url": "https://example.com",
    "company_name": "Example Company S.r.l.",
    "ateco_description": "Example business activity",
    "ateco_code": "12.34.56",
    "share_capital": "10000",
    "employees": "50",
    "company_registration_date": "2010-01-01",
    "legal_form": "S.r.l."
  }
}
```

## Error Handling

If any errors occur, the script returns a JSON error message:

```json
{
  "error": "Error message description"
}
```

## Contributing

Contributions are welcome! Feel free to:
- Open issues for bugs or suggestions
- Submit pull requests for improvements
- Suggest new features or enhancements

## License

This project is licensed under the MIT License - see the LICENSE file for details.
