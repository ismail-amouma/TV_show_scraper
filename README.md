
# TV Show Scraper and Flask App


https://github.com/ismail-amouma/TV_show_scraper/assets/91847466/688846cb-ddc9-4a90-a1af-72d18c9e0ce2


This project is a Python application that combines web scraping using Selenium with a Flask web application to display and manage scraped data from a streaming website. The primary focus of this project is to scrape information about TV shows that you can watch online. The scraped data includes details about TV show episodes and their corresponding streaming links.

## Prerequisites

To run this project, you need the following:

- Python (>= 3.6)
- Flask (`pip install Flask`)
- Flask-SQLAlchemy (`pip install Flask-SQLAlchemy`)
- Flask-Migrate (`pip install Flask-Migrate`)
- Selenium (`pip install selenium`)

You also need to have the Chrome WebDriver installed for Selenium. Download it from [here](https://sites.google.com/chromium.org/driver/) and place it in the project directory.

## Getting Started

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. Install the required dependencies:

   ```bash
   flask db init Flask,Flask-SQLAlchemy,Flask-Migrate,selenium
   ```
3. Run the migration to set up the database:

   ```bash
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

4. Run the Flask app:

   ```bash
   python app.py
   ```

5. Access the app in your web browser at `http://127.0.0.1:5000/`.

## Features

- **TV Show Scraping**: The app uses Selenium to scrape TV show information, including posters, titles, years, and streaming links for each episode. This makes it easy for you to discover and watch TV shows online.

- **SQLite Database**: Scraped data is stored in an SQLite database named `scraped_data.db`.

- **View Data**: Visit the home page to view the scraped data. Each entry includes details about the show and its episodes, along with streaming links.

- **Submit URLs**: You can submit URLs of TV show pages from the streaming website to scrape data for storage.

- **Delete Entries**: You can delete entries from the database using the delete button next to each entry.

## Usage Notes

- This code example is intended for educational purposes and may require further customization to fit your specific needs.

- Always respect the terms of use and policies of the websites you are scraping. Ensure that you are scraping data responsibly and within legal and ethical boundaries.

## Contributions

Contributions are welcome! If you have suggestions or improvements, feel free to submit a pull request.

*Disclaimer: This project is for educational purposes only. Please ensure that you adhere to the terms of use and policies of any websites you interact with through this application.*


