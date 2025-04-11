# Amazon Product Scraper & SQL Pipeline

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![License](https://img.shields.io/badge/License-MIT-green)

A project to scrape Amazon product data (titles, reviews, colors, images), process it with NLP, and store it in a structured MySQL database. Ideal for e-commerce analytics.

## Features
- **Web Scraping**: Extract product titles, reviews, colors, and image links.
- **NLP Cleaning**: Lemmatization, stopword removal, and punctuation stripping.
- **JSON-to-SQL Pipeline**: Automate data transfer to a relational database.
- **Schema Design**: Tables for Products, Colors, Images, and relationships.

## Project Structure  
  
  ├── scraper.py             # Scrapes Amazon product data → saves as JSON  
  ├── Data_Insertion.py      # Processes JSON and inserts into MySQL  
  ├── main_data.json         # Sample scraped data (excluded via .gitignore)  
  ├── requirements.txt       # Python dependencies  
  ├── Report/                # Project report/documentation  
  └── README.md  

## Prerequisites
- Python 3.9+
- MySQL Server 8.0
- NLTK Data (run `nltk.download('stopwords')` and `nltk.download('wordnet')` in Python)

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/Amazon-Product-Scraper-DB.git
   cd Amazon-Product-Scraper-DB
Install dependencies:
 
    pip install -r requirements.txt

MySQL Setup:
Create a database named amazon_data.
Update MySQL credentials in Data_Insertion.py.

Run the scraper:

    python scraper.py  # Outputs data to main_data.json
Insert data into MySQL:
  
    python Data_Insertion.py
## Report  
See the Project Report for methodology, challenges, and analysis.  

## Troubleshooting  
- **MySQL Connection Errors**: Ensure the database name and credentials in `Data_Insertion.py` match your local MySQL setup.  
- **Missing NLTK Data**: Run the following in a Python shell to download required datasets:  
  ```python
  import nltk  
  nltk.download('stopwords')  
  nltk.download('wordnet')  

---
License
MIT License. See LICENSE.
### Key Additions:
1. **Avoided Code Snippets**: Focused on setup/usage instead of implementation details.  
2. **Modular Structure**: Separated scraper and data insertion logic for clarity.  
3. **NLP/NLTK Setup**: Added instructions for downloading stopwords/WordNet.  
4. **Security Note**: Removed hardcoded credentials from the code example.  



