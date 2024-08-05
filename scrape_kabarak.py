import requests
from bs4 import BeautifulSoup
import json

# Manually specified URLs to scrape
urls = [
    'https://kabarak.ac.ke/',
    'https://kabarak.ac.ke/about-us',
    'https://kabarak.ac.ke/academics',
    'https://kabarak.ac.ke/admissions',
    'https://kabarak.ac.ke/campus-life',
    'https://kabarak.ac.ke/news'
]

def scrape_page_content(url):
    print(f"Scraping URL: {url}")
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            content = ' '.join([para.text for para in paragraphs])
            cleaned_content = clean_content(content)
            print(f"Scraped {len(paragraphs)} paragraphs.")
            return cleaned_content
        else:
            print(f"Failed to scrape URL: {url} with status code {response.status_code}")
            return ""
    except Exception as e:
        print(f"Exception occurred while scraping {url}: {e}")
        return ""

def clean_content(content):
    unwanted_sections = ['menu', 'Home', 'About Us', 'Library', 'Downloads', 'Services', 'Contacts']
    lines = content.split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip() and not any(tag in line for tag in unwanted_sections)]
    return ' '.join(cleaned_lines)

def build_knowledge_base(urls):
    knowledge_base = {}

    for url in urls:
        content = scrape_page_content(url)
        if content:
            knowledge_base[url] = content

    with open('knowledge_base.json', 'w') as f:
        json.dump(knowledge_base, f, indent=4)
    print("Knowledge base built successfully.")

if __name__ == '__main__':
    build_knowledge_base(urls)
