# Flask Stock Data Scraper API

**Note:** The API takes approximately 3-4 minutes to return the CSV data due to the use of a free-tier deployment on Render and the time required for headless browsers to fully load and render the source website during scraping. <br>

This project provides a RESTful API to scrape stock data and return it as a CSV file. The application is built with Flask, Playwright, and BeautifulSoup. It is deployed on [Render](https://render.com) and containerized using Docker.

⚠️ **This project is for educational purposes only.**

---

## Technologies Used

- **Flask**: Web framework for Python used to create API endpoints.
- **Playwright**: For automating browser interactions to scrape data dynamically.
- **BeautifulSoup**: For parsing HTML content and extracting stock data.
- **Docker**: Containerization tool used to package the application.
- **Render**: Platform used to deploy the application.

---

## Base URL

```
https://python-scraper-api-r1uj.onrender.com
```

---

## Available API Endpoints

**Note: All symbols are avaiable in symbols.txt**

1. **Get NIFTY Stock Data**
   ```
   GET /api/NIFTY
   ```

2. **Get BANKNIFTY Stock Data**
   ```
   GET /api/BANKNIFTY
   ```

3. **Get NIFTYIT Stock Data**
   ```
   GET /api/NIFTYIT
   ```

4. **Get NIFTY500 Stock Data**
   ```
   GET /api/NIFTY500
   ```

5. **Get NIFTYMIDCAP Stock Data**
   ```
   GET /api/NIFTYMIDCAP
   ```

6. **Get NIFTYAUTO Stock Data**
   ```
   GET /api/NIFTYAUTO
   ```

Each endpoint returns a CSV file containing stock data for the specified symbol.

---

## Example Response

When you call the endpoint `/api/NIFTY`, the API returns a CSV file with the following columns:

```
name,price,change
RELIANCE,2490.50,2.45
TCS,3245.65,-1.12
INFY,1500.75,0.89
```

---

## Running the Application Locally

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/stock-scraper-api.git
   cd stock-scraper-api
   ```

2. **Build the Docker image**:

   ```bash
   docker build -t stock-scraper-api .
   ```

3. **Run the Docker container**:

   ```bash
   docker run -p 5000:5000 stock-scraper-api
   ```

4. **Access the API**:

   Visit `http://localhost:5000/api/<symbol>` to get stock data.

---

## Deployment

This application is deployed on [Render](https://render.com). The Docker image is used for deployment, ensuring consistent behavior across environments.

---

## Notes

- This project uses Playwright for browser automation. Playwright requires additional system dependencies (e.g., Chromium browser libraries) which are included in the Dockerfile.
- Be mindful of scraping ethics and website terms of service when using this code.

---

## License

MIT License. This project is for educational purposes only.
