#!/usr/bin/env python3
"""
Basic web scraper: fetches a URL, cleans HTML with BeautifulSoup,
and saves the result to data/<hostname>.html.
"""
import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def main():
    if len(sys.argv) != 2:
        print("Usage: python scrape.py <URL>")
        sys.exit(1)
    url = sys.argv[1]
    parsed = urlparse(url)
    hostname = parsed.netloc
    if not hostname:
        print("Error: Invalid URL – no hostname detected.")
        sys.exit(1)

    # Ensure the data directory exists (relative to this script)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, '..', 'data')
    os.makedirs(data_dir, exist_ok=True)

    output_path = os.path.join(data_dir, f"{hostname}.html")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        sys.exit(1)

    # Parse and clean HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    cleaned_html = soup.prettify()

    # Save cleaned HTML
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_html)
    except OSError as e:
        print(f"Error writing file: {e}")
        sys.exit(1)

    print(f"Saved cleaned HTML to: {output_path}")

if __name__ == '__main__':
    main()