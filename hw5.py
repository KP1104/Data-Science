import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import requests

# Function to analyze and draw conclusions from the data


def analyze_data(df):
    """Analyzes and draws conclusions from the data."""
    if df.empty:
        print("No data available for analysis.")
        return

    df['price_bucket'] = df['price_bucket'].str.replace(
        '$', r'\$', regex=False)

    # 1. Basic analysis: Review Rating Distribution
    print(f"Average Rating: {df['review_rating'].mean():.2f}")
    print(f"Review Count: {df['review_count'].sum()}")

    # 2. Rating Distribution Plot
    plt.figure(figsize=(10, 6))
    sns.histplot(df['review_rating'], kde=True, bins=10, color='skyblue')
    plt.title('Review Rating Distribution')
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

    # 3. Review Count vs Rating (Scatter Plot)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='review_count', y='review_rating', hue='price_bucket',
                    palette='coolwarm', size='review_count', sizes=(20, 200))
    plt.title('Review Count vs Rating (Price Bucket)')
    plt.xlabel('Review Count')
    plt.ylabel('Review Rating')
    plt.legend(title='Price Bucket')
    plt.grid(True)
    plt.show()

    # 4. Review Rating Distribution by Price Bucket (Box Plot)
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x='price_bucket', y='review_rating', palette='Set2')
    plt.title('Review Rating Distribution by Price Bucket')
    plt.xlabel('Price Bucket')
    plt.ylabel('Review Rating')
    plt.grid(True)
    plt.show()

    # 5. Rating vs Location (City) - Box Plot
    plt.figure(figsize=(15, 8))
    sns.boxplot(data=df, x='city', y='review_rating', palette='muted')
    plt.title('Review Ratings by City')
    plt.xlabel('City')
    plt.ylabel('Review Rating')
    plt.xticks(rotation=90, ha='center')
    plt.grid(True)
    plt.show()

    # 6. Distribution of Review Counts (Histogram)
    plt.figure(figsize=(10, 6))
    sns.histplot(df['review_count'], kde=True, color='purple', bins=20)
    plt.title('Distribution of Review Counts')
    plt.xlabel('Review Count')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

    # 7. Correlation between Latitude and Longitude (Geospatial Analysis)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='longitude', y='latitude', hue='review_rating',
                    palette='coolwarm', size='review_count', sizes=(20, 200))
    plt.title('Geospatial Distribution of Businesses (Rating vs Location)')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.show()

# Function to load CSV data


def load_data(csv_file_path):
    """Loads data from a CSV file."""
    try:
        df = pd.read_csv(csv_file_path)
        print(f"Data loaded successfully from {csv_file_path}.")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

# Modify default_mode to include analysis from CSV file


def default_mode():
    """Reads data from CSV, performs analysis, and saves combined data."""
    # Specify the path to your CSV file here
    csv_file_path = 'Ubereats_dataset.csv'  # Change to your CSV file's path

    # Load the data
    df = load_data(csv_file_path)

    # If data is loaded, perform analysis
    if not df.empty:
        analyze_data(df)
    else:
        print("No data available for analysis.")

    # Combine Data and Save (if needed, you can modify this step)
    # If additional API or scraping data is available, you can combine it here
    combined_data = df
    os.makedirs("static_datasets", exist_ok=True)
    combined_file = "static_datasets/combined_data.csv"
    combined_data.to_csv(combined_file, index=False)
    print(f"Data saved as {combined_file}")


if __name__ == "__main__":
    default_mode()
