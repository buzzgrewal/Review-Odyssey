# Review-Odyssey: Chart Your Course Through the Sea of Opinions.


Review Odyssey is a dynamic web scraping tool designed to extract user reviews from IMDb and similar review-based websites. It leverages Selenium to interact with dynamically loaded content, BeautifulSoup for efficient HTML parsing, and Streamlit for an intuitive, interactive interface. Whether you're a data enthusiast or a developer looking to analyze user opinions, Review Odyssey makes it easy to collect, view, and download review data.

## Features

- **Dynamic Web Scraping:** Automatically scrolls, clicks "All" at the end of the page, and loads additional reviews by handling "Load More" or "25 more" buttons.
- **HTML Parsing with BeautifulSoup:** Processes the final rendered HTML to accurately extract review details such as title, rating, and review text.
- **Interactive Streamlit Interface:** Provides a user-friendly web interface where you can input a base URL, initiate scraping, view scraped reviews in real time, and download the data.
- **Multiple Output Formats:** Export scraped reviews as CSV or JSON for further analysis.
- **Customizable Settings:** Easily adjust wait times, headless mode, and browser options to suit different environments and improve scraping reliability.
- **Robust Error Handling:** Gracefully manages missing elements and exceptions during scraping.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/review-odyssey.git
   cd review-odyssey
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install the required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

2. **Open the provided URL** in your browser.

3. **Input the base URL** for IMDb reviews (or any similar review page) and click **"Start Scraping"**.

4. **View the scraped reviews** in the interactive table, and use the download buttons to export the data as CSV or JSON.

## Interface
# Main Page
![250226_17h04m15s_screenshot](https://github.com/user-attachments/assets/23864a3c-315d-40d1-b63e-68e2fc4075c6)

# Processing
![250226_17h04m25s_screenshot](https://github.com/user-attachments/assets/a526c225-243d-4843-b63a-41e858d9ed24)
![250226_17h05m03s_screenshot](https://github.com/user-attachments/assets/05af1ad0-9730-45c7-a38e-d6c9f108c056)

# Links Extracted
![250226_17h05m47s_screenshot](https://github.com/user-attachments/assets/dd99c327-03ad-4968-9f80-6b9d38ee3571)

# Scraping
![250226_17h09m56s_screenshot](https://github.com/user-attachments/assets/ceb4113a-bd7f-40c8-9ddd-bd81e0b45037)
![250226_19h23m28s_screenshot](https://github.com/user-attachments/assets/a2dafda9-7f56-4731-9243-faf9fca32cbb)

# Scraped Data
![250226_19h40m02s_screenshot](https://github.com/user-attachments/assets/d5558c03-4cdf-4653-9b2b-83f370f3434e)

# Download Formats
**CSV**
![250226_19h41m00s_screenshot](https://github.com/user-attachments/assets/818e3acf-4af7-4c28-a8e9-df1767cc8ec2)

**JSON**


## Technologies Used

- **Python**
- **Selenium:** For automating browser interactions and handling dynamic content.
- **BeautifulSoup:** For parsing HTML and extracting review data.
- **Streamlit:** For building a user-friendly web interface.
- **Pandas:** For data handling and exporting to CSV.
- **Webdriver Manager:** For managing browser drivers seamlessly.



## Acknowledgements

- **IMDb:** For providing a rich source of user reviews.


