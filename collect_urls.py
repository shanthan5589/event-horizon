from get_page_urls import get_article_urls_from_page
import time

def collect_urls(pages=1):

    all_urls = []

    for page in range(1, pages+1):
        urls = get_article_urls_from_page(page)
        print(f"Page {page}: found {len(urls)} articles")
        all_urls.extend(urls)
        time.sleep(1) 

    # Remove duplicates
    all_urls = list(set(all_urls))
    print(f"\nTotal unique URLs collected: {len(all_urls)}")

    # Save to file
    with open("urls.txt", "w") as f:
        for url in all_urls:
            f.write(url + "\n")

    print("Saved to urls.txt")