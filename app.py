import streamlit as st
import pandas as pd
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse


s_timer = 0

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2) 
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    st.write("Reached the bottom of the page.")

def click_all_button_at_end(driver):
    wait = WebDriverWait(driver, 10)
    try:
        scroll_to_bottom(driver)
        all_buttons = driver.find_elements(By.XPATH, "//button[.//span[contains(text(), 'All')]]")
        if all_buttons:
            all_button = all_buttons[-1]
            driver.execute_script("arguments[0].scrollIntoView(true);", all_button)
            time.sleep(1)  
            driver.execute_script("arguments[0].click();", all_button)
            st.write("Clicked on 'All' button at the end of the page. Waiting for content to load...")
            time.sleep(s_timer)
        else:
            st.write("No 'All' button found at the end of the page.")
    except Exception as e:
        st.write("Could not click on 'All' button at the end. Exception:", e)

def get_all_review_links(driver, base_url):
    driver.get(base_url)
    time.sleep(2)
    click_all_button_at_end(driver)
    
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'review-container')))
    except Exception as e:
        st.write("Reviews did not load as expected")
    
    domain = urlparse(base_url).netloc
    links = set()
    for a_tag in driver.find_elements(By.TAG_NAME, 'a'):
        href = a_tag.get_attribute('href')
        if href and urlparse(href).netloc == domain and 'review' in href.lower():
            links.add(href)
    return list(links)

def fetch_reviews(driver, url):
    driver.get(url)
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'review-container')))
    except Exception as e:
        st.write("No review container found on", url, e)
        return []
    
    reviews = []
    actions = ActionChains(driver)
    
    while True:
        review_elements = driver.find_elements(By.CLASS_NAME, 'review-container')
        # st.write(f"Found {len(review_elements)} review elements on {url}")
        for review in review_elements:
            try:
                title = review.find_element(By.CLASS_NAME, 'title').text.strip()
            except Exception:
                title = 'No Title'
            try:
                rating = review.find_element(By.CLASS_NAME, 'rating-other-user-rating').text.strip()
            except Exception:
                rating = 'No Rating'
            try:
                text = review.find_element(By.CLASS_NAME, 'text').text.strip()
            except Exception:
                text = 'No Review'
            review_data = {
                'title': title,
                'rating': rating,
                'text': text,
                'url': url
            }
            if review_data not in reviews:
                reviews.append(review_data)
        try:
            load_more_button = wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Load More') or contains(text(), '25 more')]"))
            )
            driver.execute_script("arguments[0].click();", load_more_button)
            st.write("Clicked 'Load More' button. Waiting for more reviews to load...")
            time.sleep(0)
        except Exception as e:
            st.write("No more 'Load More' button found on", url)
            break
        actions.send_keys(Keys.END).perform()
        time.sleep(2)
    
    return reviews

def save_to_csv(reviews):
    df = pd.DataFrame(reviews)
    csv = df.to_csv(index=False, encoding='utf-8')
    return csv

def save_to_json(reviews):
    json_str = json.dumps(reviews, ensure_ascii=False, indent=4)
    return json_str

def main():
    st.title("Review Odyssey")
    st.write("Enter the base URL for IMDB reviews and click the button to start scraping.")
    
    base_url = st.text_input("Base URL", "https://www.imdb.com/title/tt1375666/reviews")
    start_scraping = st.button("Start Scraping")
    
    if start_scraping:
        with st.spinner("Scraping reviews... This may take a while."):
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920x1080")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            review_links = get_all_review_links(driver, base_url)
            st.write("Review links found:", review_links)
            all_reviews = []
            if not review_links:
                review_links = [base_url]  
            st.write("Total review links found:", len(review_links))
            for link in review_links:
                st.write("Scraping:", link)
                reviews = fetch_reviews(driver, link)
                st.write("Total reviews scraped from", link, ":", len(reviews))
                all_reviews.extend(reviews)
            driver.quit()
            
            st.success("Scraping completed!")
            
            if all_reviews:
                df = pd.DataFrame(all_reviews)
                st.write("Scraped Reviews:", df)
                
                csv_data = save_to_csv(all_reviews)
                json_data = save_to_json(all_reviews)
                
                st.download_button("Download CSV", csv_data, file_name="reviews.csv", mime="text/csv")
                st.download_button("Download JSON", json_data, file_name="reviews.json", mime="application/json")
            else:
                st.write("No reviews were scraped.")

if __name__ == "__main__":
    main()
