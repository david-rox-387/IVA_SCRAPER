# Italian VAT Number Company Scraper

This Python script allows you to retrieve company information using Italian VAT numbers (Partita IVA) and/or company names by scraping data from ufficiocamerale.it through Google Custom Search API.

## Features

- Retrieves company information using:
  - VAT numbers (Partita IVA)
  - Company names
  - Or a combination of both
- Extracts data such as:
  - Company name
  - VAT number
  - ATECO code and description
  - Share capital
  - Number of employees
  - Company registration date
  - Legal form
- Uses Google Custom Search API for precise search results
- Environment variables for secure credential management

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

# Get company information using VAT number
result = scraper.get_company_info("07727071008")
print(result)

# Get company information using company name
result = scraper.get_company_info("COMPANY SRL")
print(result)

# Get company information using both
result = scraper.get_company_info("COMPANY SRL 07727071008")
print(result)
```

## Search Parameter

The `get_company_info` method accepts a string parameter that can be:

- A VAT number (e.g., "07727071008")
- A company name (e.g., "COMPANY SRL")
- A combination of both (e.g., "COMPANY SRL 07727071008")

The search will be performed using the provided information to find the most relevant company data.

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

The script returns error messages in JSON format:

```json
{
  "error": "Error message description"
}
```

## Contributing

Feel free to open issues or submit pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
