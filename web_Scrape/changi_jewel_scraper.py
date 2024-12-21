import requests
from bs4 import BeautifulSoup
import json
import os

os.makedirs('data', exist_ok=True) 
def scrape_website(url, output_file):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        content = [p.text.strip() for p in soup.find_all('p') if p.text.strip()] 
        
        if content:  
            with open(os.path.join('data', output_file), 'w', encoding='utf-8') as file:
                json.dump(content, file, indent=4)
            print(f"Content scraped and saved to {os.path.join('data', output_file)}")
        else:
            print(f"No content found on {url}.")
    
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")

scrape_website("https://www.changiairport.com", "changi_airport_content.json")
scrape_website("https://www.jewelchangiairport.com", "jewel_changi_content.json")

def merge_json_files(file_paths, output_file):
    combined_content = []
    for file_path in file_paths:
        try:
            with open(os.path.join('data', file_path), 'r', encoding='utf-8') as file:
                combined_content.extend(json.load(file))
        except FileNotFoundError:
            print(f"File {file_path} not found. Skipping.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {file_path}. Skipping.")
    
    cleaned_content = clean_data(combined_content)  # Clean the combined content before saving
    
    with open(os.path.join('data', output_file), 'w', encoding='utf-8') as file:
        json.dump(cleaned_content, file, indent=4)
    print(f"Content merged and saved to {os.path.join('data', output_file)}")

def clean_data(content):
    cleaned_content = list(set(content))  # Remove duplicates
    cleaned_content = [text.strip() for text in cleaned_content if text]  # Strip whitespace and remove empty strings
    return cleaned_content

merge_json_files(["changi_airport_content.json", "jewel_changi_content.json"], "changi_jewel_content.json")