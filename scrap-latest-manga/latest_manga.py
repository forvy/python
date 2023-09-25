# Run with: python latest_manga.py

from datetime import datetime
from csv import writer
from bs4 import BeautifulSoup as beauty
import cloudscraper

def get_data(response):
    mangaArr = []
    latest = response.find("div", {"id": "latestchapters"})
    groups = latest.find_all("div", {"class": "panel-default"})
    for group in groups:
        mangas = group.find_all("div", {"class": "media-body"})
        for manga in mangas:
            title = manga.find("a").text
            chapter = manga.find("span", {"class": "text-secondary"}).text
            link = manga.find("a", {"class": "DpTTM"})['href']
            mangaArr.append(f"{title} {chapter} - {link}")
    return mangaArr

def scrape_manga_data(url):
    # Create a CloudScraper instance
    scraper = cloudscraper.create_scraper(delay=10, browser='chrome')
    info = scraper.get(url).text
    response = beauty(info, "html.parser")
    return get_data(response)

def main():
    url = "https://mangahub.io/"
    datas = scrape_manga_data(url)
    
    filename = f"Latest manga ({datetime.utcnow().strftime('%Y-%m-%d %H%M%S')}).csv"
    
    with open(filename, 'w', encoding='utf8', newline='') as file:
        wtr = writer(file, delimiter=',')
        for x in datas:
            wtr.writerow([x])
    
if __name__ == "__main__":
    main()