import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import List

class ReviewsScraper:
    def __init__(self, asin: str, pages: int):
        self.asin = asin
        self.pages = pages
        self.url = f'https://www.amazon.in/EASYSHOP-Magnetic-Replacement-Charging-Colourfit/product-reviews/{asin}/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber='
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def get_reviews_from_page(self) -> List[dict]:
        reviews = []
        review_containers = self.driver.find_elements("css selector", 'div[data-hook=review]')
        for container in review_containers:
            user = container.find_element("css selector", 'span.a-profile-name').text
            title = container.find_element("css selector", 'a[data-hook=review-title]').text
            star_rating = container.find_element("css selector", 'i[data-hook=review-star-rating]').text
            date = container.find_element("css selector", 'span[data-hook=review-date]').text
            message = container.find_element("css selector", 'span[data-hook=review-body]').text.replace('\n', '')
            reviews.append({
                'user': user,
                'title': title,
                'star_rating': star_rating,
                'date': date,
                'message': message
            })
        return reviews

    def has_reviews(self) -> bool:
        return bool(self.driver.find_elements("css selector", 'div[data-hook=review]'))

    def iterate_over_pages(self) -> List[dict]:
        reviews = []
        for i in range(1, self.pages + 1):
            print(f"Page: {i}")
            self.driver.get(f'{self.url}{i}')
            if self.has_reviews():
                new_reviews = self.get_reviews_from_page()
                print("New reviews")
                print(new_reviews)
                reviews += new_reviews
            else:
                print("No reviews")
                break
        return reviews

    def save_to_file(self, reviews: List[dict]):
        with open('results.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['user', 'title', 'star_rating', 'date', 'message']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write the header
            writer.writeheader()

            # Write the reviews
            writer.writerows(reviews)

if __name__ == '__main__':
    asin = 'B09HC2QQZ2'
    scraper = ReviewsScraper(asin, 3)
    all_reviews = scraper.iterate_over_pages()
    print("Done.")
    print(all_reviews)
    scraper.save_to_file(all_reviews)
