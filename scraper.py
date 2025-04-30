import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

# Target website (test site)
URL = "http://books.toscrape.com/"

def fetch_data():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")

    data = []
    for book in books:
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        availability = book.find("p", class_="instock availability").text.strip()
        data.append({
            "Title": title,
            "Price": price,
            "Availability": availability
        })
    return data

def save_to_excel(data):
    df = pd.DataFrame(data)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"data/products_{now}.xlsx"
    os.makedirs("data", exist_ok=True)
    df.to_excel(filename, index=False)
    print(f" Data saved to {filename}")

if __name__ == "__main__":
    print(" Scraping data...")
    product_data = fetch_data()
    save_to_excel(product_data)
