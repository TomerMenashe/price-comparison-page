# Price Comparison Page

Welcome to the Price Comparison Page project! This application allows users to search for a specific product across multiple e-commerce websites and compare prices in a user-friendly interface.

## Project Overview

This project comprises two main components:

1. **Price Checker API**: A FastAPI-based backend that scrapes prices from BestBuy, Walmart, and Newegg.
2. **Price Comparison App**: A Next.js-based frontend that lets users enter a product name and displays a comparison table of prices from the aforementioned websites.

## Features

- **Multi-site Scraping**: Scrapes product prices from BestBuy, Walmart, and Newegg.
- **User-friendly Interface**: Simple and intuitive interface for searching and viewing price comparisons.
- **Clickable Links**: Product names in the results table link directly to the respective product pages on each site.

## Screenshots

### Welcome Page
![Welcome Page](./path/to/Screenshot%202024-05-27%20at%2019.21.54%20(2).png)

### Search Page
![Search Page](./path/to/Screenshot%202024-05-27%20at%2019.21.58%20(2).png)

### Search Results
![Search Results](./path/to/Screenshot%202024-05-27%20at%2019.23.19.png)

## Getting Started

Follow these steps to run the project locally.

### Prerequisites

- Node.js
- Python 3.7+
- npm (Node Package Manager)
- pip (Python Package Installer)

### Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/yourusername/price-comparison-page.git
   cd price-comparison-page
   
2. **Set up the backend**

Navigate to the price-checker-api directory:
cd price-checker-api

Install Python dependencies:
pip install -r requirements.txt

Run the FastAPI server:
uvicorn main:app --reload

3. **Set up the backend**

Open a new terminal and navigate to the price-comparison-app directory:
cd price-comparison-app

Install Node.js dependencies:
npm install

Run the Next.js development server:
npm run dev

4. **Access the Application**

Open your web browser and navigate to http://localhost:3000.

### Usage
Enter the product name in the search bar and click "Search".
View the comparison table with prices from BestBuy, Walmart, and Newegg.
Click on the product names to be redirected to the respective product pages on each site.


### Project Structure
price-comparison-page/
├── price-checker-api/
│   ├── main.py
│   ├── scrapers/
│   │   ├── bestbuy_scraper.py
│   │   ├── walmart_scraper.py
│   │   └── newegg_scraper.py
│   ├── requirements.txt
│   └── ...
├── price-comparison-app/
│   ├── pages/
│   │   ├── index.js
│   │   └── ...
│   ├── public/
│   │   ├── Screenshot 2024-05-27 at 19.21.54 (2).png
│   │   ├── Screenshot 2024-05-27 at 19.21.58 (2).png
│   │   └── Screenshot 2024-05-27 at 19.23.19.png
│   ├── package.json
│   └── ...
└── README.md

### Contributing
Contributions are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch for your feature or bugfix.
Commit your changes with clear and descriptive messages.
Push your changes to your forked repository.
Create a pull request to the main repository.

### Authors
Tomer Menashe
