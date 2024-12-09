from flask import Flask, Response, send_file
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import io
import csv
import time
import os

app = Flask(__name__)

def scrape_stock_data(url):
    print(f"Starting scrape_stock_data with URL: {url}")
    try:
        with sync_playwright() as p:
            print("Launching browser...")
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            print(f"Navigating to URL: {url}")
            page.goto(url, timeout=180000)
            print("Waiting for selector 'a[target=\"_self\"]'...")
            page.wait_for_selector("a[target='_self']", timeout=60000)
            print("Sleeping for 10 seconds to ensure page load...")
            time.sleep(10)
            
            html = page.content()
            print("Page content retrieved.")
            browser.close()
            print("Browser closed.")

        soup = BeautifulSoup(html, "html.parser")
        print("HTML parsed with BeautifulSoup.")

        stock_data = []
        for card in soup.select("a[target='_self']"):
            try:
                print("Extracting data from stock card...")
                change_percentage = (
                    card.select_one("p.d-flex.justify-content-end").text
                    .strip()
                    .replace("%", "")
                    .replace("+", "")
                    .strip()
                )
                symbol = card.select_one("p.text-white.fs-14-12.fw-600").text.strip()
                price = (
                    card.select_one("p.mb-0.fs-14-12.ff-lato.text-white").text
                    .strip()
                    .replace("₹", "")
                    .strip()
                )

                print(f"Parsed data - Symbol: {symbol}, Price: {price}, Change: {change_percentage}")
                stock_data.append({
                    "name": symbol,
                    "price": float(price.replace(",", "")),
                    "change": float(change_percentage)
                })
            except (AttributeError, ValueError) as e:
                print(f"Error parsing stock card: {e}")
                continue

        print(f"Finished scraping. Total stocks scraped: {len(stock_data)}")
        return stock_data

    except Exception as e:
        print(f"Error during scraping: {e}")
        raise

def generate_csv_response(stock_data, filename):
    print(f"Generating CSV response with filename: {filename}")
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['name', 'price', 'change'])
        for stock in stock_data:
            print(f"Writing row: {stock}")
            writer.writerow([stock['name'], stock['price'], stock['change']])

        response = Response(output.getvalue(), mimetype='text/csv')
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        print("CSV response generated successfully.")
        return response

    except Exception as e:
        print(f"Error generating CSV: {e}")
        return Response(f"Error: {str(e)}", status=500, mimetype='text/plain')

symbol_url_map = {
    "NIFTY": "NIFTY",
    "NIFTYIT": "NIFTYIT",
    "NIFTYJR": "NIFTYJR",
    "BANKNIFTY": "BANKNIFTY",
    "NIFTYMIDCAP": "NIFTYMIDCAP",
    "NIFTY500": "NIFTY500",
    "MIDCAP50": "MIDCAP50",
    "NIFTY100": "NIFTY100",
    "NIFTYFMCG": "NIFTYFMCG",
    "NIFTYPSU": "NIFTYPSU",
    "NIFTYMNC": "NIFTYMNC",
    "NIFTYSERVICE": "NIFTYSERVICE",
    "NIFTYENERGY": "NIFTYENERGY",
    "NIFTYPHARMA": "NIFTYPHARMA",
    "NIFTYINFRAST": "NIFTYINFRAST",
    "NIFTYREALTY": "NIFTYREALTY",
    "NIFTYPSUBANK": "NIFTYPSUBANK",
    "NIFTYSMALL": "NIFTYSMALL",
    "NIFTYPSE": "NIFTYPSE",
    "NIFTYCONSUMP": "NIFTYCONSUMP",
    "NIFTYAUTO": "NIFTYAUTO",
    "NIFTYMETAL": "NIFTYMETAL",
    "NIFTY200": "NIFTY200",
    "NIFTYMEDIA": "NIFTYMEDIA",
    "NIFTYCDTY": "NIFTYCDTY",
    "NIFTYFINANCE": "NIFTYFINANCE",
    "NIFTYCPSE": "NIFTYCPSE",
    "NIFTYPTBNK": "NIFTYPTBNK",
    "NIFTYMIDCAP150": "NIFTYMIDCAP150",
    "NIFTYSMALLCAP250": "NIFTYSMALLCAP250",
    "NIFTYSMALLCAP50": "NIFTYSMALLCAP50",
    "NCONSDUR": "NCONSDUR",
    "NOILGAS": "NOILGAS",
    "NIFTYHEALTH": "NIFTYHEALTH",
    "NIFTYMICRO250": "NIFTYMICRO250",
    "NIFTYMFG": "NIFTYMFG",
    "NIFTYMIDSELECT": "NIFTYMIDSELECT",
    "MIDCAP50": "MIDCAP50"
}

SCRAPED_DATA_DIR = "Scraped data"
os.makedirs(SCRAPED_DATA_DIR, exist_ok=True)

@app.route('/api/<symbol>', methods=['GET'])
def get_stocks_csv(symbol):
    print(f"Received request for symbol: {symbol}")

    if symbol not in symbol_url_map:
        print(f"Symbol '{symbol}' not supported.")
        return Response(f"Error: Symbol '{symbol}' not supported.", status=400, mimetype='text/plain')

    filename = f"{symbol.lower()}_stock_data.csv"
    file_path = os.path.join(SCRAPED_DATA_DIR, filename)

    if os.path.exists(file_path):
        print(f"CSV for symbol '{symbol}' already exists. Returning existing file.")
        return send_file(file_path, mimetype='text/csv', as_attachment=True, download_name=filename)

    url = f"https://portal.tradebrains.in/index/{symbol_url_map[symbol]}/heatmap"
    print(f"URL for scraping: {url}")

    try:
        Response("Scraping has begun and may take 2-4 minutes to complete. The page will continue loading until the data is fully scraped, after which a dialog box will appear for saving the scraped data.")
        stock_data = scrape_stock_data(url)

        with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['name', 'price', 'change'])
            for stock in stock_data:
                writer.writerow([stock['name'], stock['price'], stock['change']])

        print(f"CSV for symbol '{symbol}' scraped and saved successfully.")
        return send_file(file_path, mimetype='text/csv', as_attachment=True, download_name=filename)

    except Exception as e:
        print(f"Error in get_stocks_csv: {e}")
        return Response(f"Error: {str(e)}", status=500, mimetype='text/plain')

@app.route('/')
def index():
    print("Index route accessed.")
    return Response(
        "Welcome! Use the '/api/<symbol>' endpoint to get stock data for supported symbols. "
        "Please note: Scraping might take 2-4 minutes. The page will load until the data is scraped, "
        "after which a dialog box will appear to save the scraped data.",
        mimetype='text/plain'
    )


if __name__ == '__main__':
    print("Starting Flask application...")
    app.run(debug=False, host="0.0.0.0", port=5000)
