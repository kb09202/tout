# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 11:31:58 2024

@author: pc
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from pymongo import MongoClient
import time

# MongoDB Configuration
def connect_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["IMDbDatabase"]
    collection = db["Movies"]
    return collection

# Scraping IMDb with Selenium
def scrape_imdb():
    # Configure Selenium WebDriver
    driver_path = "./chromedriver"  # Chemin vers le WebDriver
    driver = webdriver.Chrome(executable_path=driver_path)
    driver.get("https://www.imdb.com/chart/top/")

    # Collect movie data
    movies = []
    rows = driver.find_elements(By.XPATH, '//tbody[@class="lister-list"]/tr')

    for row in rows[:50]:  # Limité aux 50 premiers films pour la démonstration
        title = row.find_element(By.XPATH, './/td[@class="titleColumn"]/a').text
        year = row.find_element(By.XPATH, './/td[@class="titleColumn"]/span').text.strip("()")
        rating = row.find_element(By.XPATH, './/td[@class="ratingColumn imdbRating"]').text
        link = row.find_element(By.XPATH, './/td[@class="titleColumn"]/a').get_attribute("href")

        # Collect more details from movie page
        driver.get(link)
        time.sleep(1)
        genre = driver.find_element(By.XPATH, '//span[@class="ipc-chip__text"]').text
        director = driver.find_element(By.XPATH, '//a[contains(@href, "tt_ov_dr")]').text
        driver.back()

        movies.append({
            "Title": title,
            "Year": int(year),
            "Rating": float(rating) if rating else None,
            "Genre": genre,
            "Director": director,
            "Link": link
        })

    driver.quit()
    return movies

# Store Data in MongoDB
def store_to_mongodb(data, collection):
    collection.insert_many(data)
    print(f"Data successfully stored in MongoDB: {len(data)} records.")

# Main Script
if __name__ == "__main__":
    # Step 1: Scrape IMDb data
    print("Scraping data from IMDb...")
    movie_data = scrape_imdb()

    # Step 2: Process data with Pandas
    print("Processing data...")
    df = pd.DataFrame(movie_data)
    print(df.head())

    # Step 3: Store data in MongoDB
    print("Storing data to MongoDB...")
    collection = connect_mongo()
    store_to_mongodb(movie_data, collection)
    print("Done.")

