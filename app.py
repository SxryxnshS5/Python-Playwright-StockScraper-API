from flask import Flask, Response, redirect, url_for
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import io
import csv

app = Flask(__name__)

def scrape_stock_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://portal.tradebrains.in/index/MIDCAP50/heatmap")

        # Wait for elements to load
        page.wait_for_selector("a[target='_self']")
        time.sleep(5)  # Additional wait time for dynamic content
        
        # Fetch the page content
        html = page.content()
        browser.close()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    
    # Extract stock data
    stock_data = []
    for card in soup.select("a[target='_self']"):
        try:
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

            # Append the stock data
            stock_data.append({
                "name": symbol,
                "price": float(price.replace(",", "")),  # Ensure price is a float
                "change": float(change_percentage)       # Ensure change is a float
            })
        except (AttributeError, ValueError) as e:
            print(f"Error parsing stock card: {e}")  # Debugging output
            continue

    return stock_data

@app.route('/')
def index():
    return redirect(url_for('get_stocks_csv'))

@app.route('/api/MIDCAP50', methods=['GET'])
def get_stocks_csv():
    try:
        # Scrape the stock data
        stock_data = scrape_stock_data()

        # Create an in-memory CSV file
        output = io.StringIO()
        writer = csv.writer(output)
        # Write the header
        writer.writerow(['name', 'price', 'change'])
        # Write the data rows
        for stock in stock_data:
            writer.writerow([stock['name'], stock['price'], stock['change']])

        # Return the CSV as a response
        response = Response(output.getvalue(), mimetype='text/csv')
        response.headers["Content-Disposition"] = "attachment; filename=stock_data.csv"
        return response

    except Exception as e:
        return Response(f"Error: {str(e)}", status=500, mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=True)
