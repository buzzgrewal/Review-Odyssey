from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json
import time
from urllib.parse import urlparse

total_reviews = 0
s_timer = 10

def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        last_height = new_height
    print("Reached the bottom of the page.")

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
            print("Clicked on 'All' button at the end of the page. Waiting for content to load...")
            time.sleep(s_timer)
        else:
            print("No 'All' button found at the end of the page.")
        
    except Exception as e:
        print("Could not click on 'All' button at the end, proceeding with the current page. Exception:", e)

def get_all_review_links(driver, base_url):
    driver.get(base_url)
    time.sleep(2)

    click_all_button_at_end(driver)

    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'review-container')))
    except Exception as e:
        print("Reviews did not load as expected:", e)

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
        print("No review container found on", url, e)
        return []
    
    reviews = []
    actions = ActionChains(driver)
    
    while True:
        review_elements = driver.find_elements(By.CLASS_NAME, 'review-container')
        print(f"Found {len(review_elements)} review elements on {url}")
        
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
            print("Clicked 'Load More' button. Waiting for more reviews to load...")
            time.sleep(5)
        except Exception as e:
            print("No more 'Load More' button found on", url, e)
            break
        
        actions.send_keys(Keys.END).perform()
        time.sleep(2)
    
    return reviews

def save_to_csv(reviews, filename='reviews.csv'):
    df = pd.DataFrame(reviews)
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"Data saved to {filename}")

def save_to_json(reviews, filename='reviews.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
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
    
    base_url = "https://www.imdb.com/title/tt1375666/reviews"  
    review_links = get_all_review_links(driver, base_url)
    print("Review links found:", review_links)
    
    all_reviews = []
    if not review_links:
        review_links = [base_url] 
        
    print("Total review links found:", len(review_links))
    
    for link in review_links:
        print("Scraping:", link)
        reviews = fetch_reviews(driver, link)
        print("Total reviews scraped from", link, ":", len(reviews))
        total_reviews = total_reviews + 1
        print("Total reviews scraped from all links:", total_reviews)
        all_reviews.extend(reviews)
    
    driver.quit()
    
    save_to_csv(all_reviews)
    save_to_json(all_reviews)
