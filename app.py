from flask import Flask, Response, redirect, url_for
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import io
import csv

app = Flask(__name__)

def scrape_stock_data(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            try:
                page.goto(url, timeout=90000)

                page.wait_for_selector("a[target='_self']", timeout=60000)

                page.wait_for_load_state("networkidle", timeout=60000)
                
                html = page.content()
            finally:
                browser.close()

        soup = BeautifulSoup(html, "html.parser")
        
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
                    .replace(",", "")
                    .strip()
                )

                stock_data.append({
                    "name": symbol,
                    "price": float(price),
                    "change": float(change_percentage)
                })
            except (AttributeError, ValueError) as e:
                print(f"Error parsing stock card: {e}")
                continue

        return stock_data

    except Exception as e:
        print(f"Error during scraping: {e}")
        raise

def generate_csv_response(stock_data, filename):
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['name', 'price', 'change'])
        for stock in stock_data:
            writer.writerow([stock['name'], stock['price'], stock['change']])

        response = Response(output.getvalue(), mimetype='text/csv')
        response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return response

    except Exception as e:
        return Response(f"Error: {str(e)}", status=500, mimetype='text/plain')

@app.route('/')
def index():
    return redirect(url_for('get_stocks_csv_nifty'))

@app.route('/api/MIDCAP50', methods=['GET'])
def get_stocks_csv_midcap():
    try:
        stock_data = scrape_stock_data("https://portal.tradebrains.in/index/MIDCAP50/heatmap")
        return generate_csv_response(stock_data, "midcap50_stock_data.csv")
    except Exception as e:
        return Response(f"Error: {str(e)}", status=500, mimetype='text/plain')

@app.route('/api/NIFTY', methods=['GET'])
def get_stocks_csv_nifty():
    try:
        stock_data = scrape_stock_data("https://portal.tradebrains.in/index/NIFTY/heatmap")
        return generate_csv_response(stock_data, "nifty_stock_data.csv")
    except Exception as e:
        return Response(f"Error: {str(e)}", status=500, mimetype='text/plain')
    
@app.route('/api/NIFTYNEXT50', methods=['GET'])
def get_stocks_csv_nifty_next50():
    try:
        stock_data = scrape_stock_data("https://portal.tradebrains.in/index/NIFTYJR/heatmap")
        return generate_csv_response(stock_data, "nifty_next50_stock_data.csv")
    except Exception as e:
        return Response(f"Error: {str(e)}", status=500, mimetype='text/plain')
    
@app.route('/api/NIFTYBANK', methods=['GET'])
def get_stocks_csv_nifty_bank():
    try:
        stock_data = scrape_stock_data("https://portal.tradebrains.in/index/BANKNIFTY/heatmap")
        return generate_csv_response(stock_data, "nifty_bank_stock_data.csv")
    except Exception as e:
        return Response(f"Error: {str(e)}", status=500, mimetype='text/plain')
    
@app.route('/api/NIFTYFINANCE', methods=['GET'])
def get_stocks_csv_nifty_finance():
    try:
        stock_data = scrape_stock_data("https://portal.tradebrains.in/index/NIFTYFINANCE/heatmap")
        return generate_csv_response(stock_data, "nifty_finance_stock_data.csv")
    except Exception as e:
        return Response(f"Error: {str(e)}", status=500, mimetype='text/plain')
    
@app.route('/api/NIFTYIT', methods=['GET'])
def get_stocks_csv_nifty_it():
    try:
        stock_data = scrape_stock_data("https://portal.tradebrains.in/index/NIFTYIT/heatmap")
        return generate_csv_response(stock_data, "nifty_it_stock_data.csv")
    except Exception as e:
        return Response(f"Error: {str(e)}", status=500, mimetype='text/plain')
    

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
