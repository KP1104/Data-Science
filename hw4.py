import argparse
import os
import json
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time


def static_mode(static_path):
    """Reads and prints static dataset."""

    start_time = time.time()

    if os.path.exists(static_path):
        if static_path.endswith(".csv"):
            df = pd.read_csv(static_path)
            print(f"Dataset Loaded: {static_path}\nShape: {
                  df.shape}\nSample Data:\n", df.head())
        elif static_path.endswith(".json"):
            with open(static_path, 'r') as f:
                data = json.load(f)
                print(f"Dataset Loaded: {static_path}\nSample Data:\n", json.dumps(
                    data, indent=2)[:500])
        else:
            print("Unsupported file format. Only CSV and JSON are supported.")
    else:
        print(f"File not found at path: {static_path}")

    end_time = time.time()
    print(f"Time taken for Static Mode: {end_time - start_time:.2f} seconds\n")


def scrape_mode():
    """Scrapes a sample dataset and prints it."""

    start_time = time.time()

    yelp_url = "https://www.yelp.com/biz/gol97typwuGAaRvklK5viA"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "TE": "Trailers"
    }
    response = requests.get(yelp_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page. HTTP Status Code: {
              response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    image_div = soup.find(
        "div", class_="photo-header-media__09f24__ojlZt photo-header-media--overlay__09f24__KwCp5 y-css-1wz9c5l")

    image_url = (
        image_div.find("img")["src"]
        if image_div and image_div.find("img")
        else "Not available"
    )

    data = {
        "business_name": soup.find("h1").text.strip() if soup.find("h1") else "Not available",
        "address": soup.find("address").text.strip() if soup.find("address") else "Not available",
        "rating": soup.find("div", {"role": "img"})['aria-label'] if soup.find("div", {"role": "img"}) else "Not available",
        "website_url": soup.find("div", class_="y-css-8x4us").find("p", class_="y-css-19xonnr").text.strip(
        ) if soup.find("div", class_="y-css-8x4us") else "Not available",
        "image_url": image_url,
    }
    print(f"Scraped Data:\n{data}")

    end_time = time.time()
    print(f"Time taken for Scrape Mode: {end_time - start_time:.2f} seconds\n")


def default_mode():
    """Performs scraping, API fetching, and saves combined data."""

    start_time = time.time()

    # Scrape data
    scrape_url = "https://www.yelp.com/biz/gol97typwuGAaRvklK5viA"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(scrape_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page. HTTP Status Code: {
              response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    image_div = soup.find(
        "div", class_="photo-header-media__09f24__ojlZt photo-header-media--overlay__09f24__KwCp5 y-css-1wz9c5l")

    image_url = (
        image_div.find("img")["src"]
        if image_div and image_div.find("img")
        else "Not available"
    )
    scraped_data = {
        "business_name": soup.find("h1").text.strip() if soup.find("h1") else "Not available",
        "address": soup.find("address").text.strip() if soup.find("address") else "Not available",
        "rating": soup.find("div", {"role": "img"})['aria-label'] if soup.find("div", {"role": "img"}) else "Not available",
        "website_url": soup.find("div", class_="y-css-8x4us").find("p", class_="y-css-19xonnr").text.strip(
        ) if soup.find("div", class_="y-css-8x4us") else "Not available",
        "image_url": image_url,
    }
    print("Scraping Completed. Sample Data:\n", scraped_data)

    # API fetching
    api_url = "https://api.yelp.com/v3/businesses/gol97typwuGAaRvklK5viA"

    headers = {"Authorization": "Bearer 7juqd6WjCFzLxHO4gi-fejdROu-Ud68EqcfGKc3s8XUgu3_2pLJgu6wlPMOx_WLCez3mniYgf2_UYd5wxerAgHbmwSaADE4Os5laZHRmqmTe0hRiiRSTH-WeQJo9Z3Yx"}
    api_response = requests.get(api_url, headers=headers)
    if api_response.status_code != 200:
        print(f"Failed to fetch API data. HTTP Status Code: {
              api_response.status_code}")
        return

    api_data = api_response.json()
    scraped_data["review_count"] = api_data['review_count']

    # save data to csv
    combined_data = [scraped_data]
    os.makedirs("data", exist_ok=True)
    combined_file = "data/scrape_data.csv"
    pd.DataFrame(combined_data).to_csv(combined_file, index=False)
    print(f"Data saved as {combined_file}")

    end_time = time.time()
    print(f"Time taken for Default Mode: {
          end_time - start_time:.2f} seconds\n")


# Main function with argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run script in static, scrape, or default mode.")
    parser.add_argument(
        "--static", help="Path to the static dataset (CSV/JSON).")
    parser.add_argument("--scrape", action="store_true",
                        help="Run in scrape mode.")
    args = parser.parse_args()

    if args.static:
        print("Running in Static Mode...")
        static_mode(args.static)
    elif args.scrape:
        print("Running in Scrape Mode...")
        scrape_mode()
    else:
        print("Running in Default Mode...")
        default_mode()
