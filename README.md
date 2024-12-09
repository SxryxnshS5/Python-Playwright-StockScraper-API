# Flask Stock Data Scraper API

**Note:** The API offers two ways to retrieve stock data:

1. **Live Scraped Data Endpoint**: Takes approximately **3-4 minutes** to return the CSV data due to the use of a free-tier deployment on Render and the time required for headless browsers to fully load and render the source website during scraping.
2. **Automated Scraped Data Endpoint**: Returns data in just a **few seconds** by using pre-scraped data generated twice a day through GitHub Actions *(It may still take 30 seconds to 1 minute for Render to wake up from sleep mode.)*.

This project provides a RESTful API to scrape stock data and return it as a CSV file. The application is built with Flask, Playwright, and BeautifulSoup. It is deployed on [Render](https://render.com) and containerized using Docker.

⚠️ **This project is for educational purposes only.**

---

## Base URL

```
https://python-scraper-api-r1uj.onrender.com
```

---

## Available API Endpoints

### 1. Live Scraped Data Endpoint

**Endpoint**: `/api/<symbol>`

This endpoint performs live scraping of stock data from the source website when requested. Since it uses a headless browser via Playwright, it may take **3-4 minutes** to complete.

- **Example Requests**:

  ```
  GET /api/NIFTY
  GET /api/BANKNIFTY
  GET /api/NIFTYIT
  GET /api/NIFTY500
  GET /api/NIFTYMIDCAP
  GET /api/NIFTYAUTO
  ```

- **How it Works**:
  - Initiates a live scrape of the stock data for the specified symbol.
  - Returns a CSV file with the latest stock data once the scraping is complete.

- **Use Case**:
  - When you need real-time, up-to-date stock data.

### 2. Automated Scraped Data Endpoint

**Endpoint**: `/api-asd/<symbol>`

This endpoint serves pre-scraped stock data stored in CSV files. The data is automatically updated **twice daily** via GitHub Actions, making the response time just a **few seconds**.

- **Example Requests**:

  ```
  GET /api-asd/NIFTY
  GET /api-asd/BANKNIFTY
  GET /api-asd/NIFTYIT
  GET /api-asd/NIFTY500
  GET /api-asd/NIFTYMIDCAP
  GET /api-asd/NIFTYAUTO
  ```

- **How it Works**:
  - Checks if a pre-scraped CSV file for the requested symbol exists in the `Scraped data` folder.
  - Returns the CSV file if available. If not, returns an error message indicating no data is available.

- **Use Case**:
  - When you need quick access to recently updated stock data without waiting for live scraping.

---

## Supported Symbols

**Note:** All supported symbols are listed in `symbols.txt`.

Some commonly used symbols include:

- **NIFTY**
- **BANKNIFTY**
- **NIFTYIT**
- **NIFTY500**
- **NIFTYMIDCAP**
- **NIFTYAUTO**

---

## Example Response

When you call the endpoint `/api/NIFTY` or `/api-asd/NIFTY`, the API returns a CSV file with the following format:

```
name,price,change
RELIANCE,2490.50,2.45
TCS,3245.65,-1.12
INFY,1500.75,0.89
```

---

## How GitHub Actions Automate Scraping

The project uses a **GitHub Actions workflow** to automate the scraping process:

1. **Scheduled Execution**:
   - Runs **twice daily** at **1 AM** and **1 PM IST** (7:30 PM and 7:30 AM UTC).
   - Ensures the stock data remains fresh and up-to-date.

2. **Workflow Steps**:
   - **Checkout Repository**: Pulls the latest code.
   - **Create Directory**: Ensures the `Scraped data` directory exists.
   - **Scrape Data**: Triggers the scraping process for all supported symbols.
   - **Save CSVs**: Downloads the scraped data and saves it as CSV files in the `Scraped data` folder.
   - **Commit and Push**: Updates the repository with the new CSVs.

3. **Manual Trigger**:
   - The workflow can also be triggered manually via GitHub Actions.

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

   Visit `http://localhost:5000/api/<symbol>` for live scraping or `http://localhost:5000/api-asd/<symbol>` for automated scraped data.

---

## Deployment

This application is deployed on [Render](https://render.com). The Docker image is used for deployment, ensuring consistent behavior across environments.

---

## Technologies Used

- **Flask**: Web framework for creating API endpoints.
- **Playwright**: For automating browser interactions to perform live scraping.
- **BeautifulSoup**: For parsing HTML content and extracting stock data.
- **Docker**: For containerizing the application.
- **Render**: For deploying the API.
- **GitHub Actions**: For automating the scraping process and maintaining up-to-date data.

---

## 🤝 Contributing

We’d love your help! Check out our [Contributing Guide](CONTRIBUTING.md) to get started. If you have questions or want to brainstorm ideas, visit the [Discussions](https://github.com/yourusername/repo/discussions) page.

**Let’s build this together!** 🚀

---

## License

MIT License. This project is for educational purposes only.

---
