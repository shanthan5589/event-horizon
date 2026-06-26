import requests
from bs4 import BeautifulSoup

def get_article_urls_from_page(page_num):

    if page_num == 1:
        url = "https://www.quantamagazine.org/?s=black+holes"
    else:
        url = f"https://www.quantamagazine.org/page/{page_num}/?s=black+holes"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Page {page_num} failed: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all article links
    links = soup.find_all("a", href=True)
    
    article_urls = []
    for link in links:
        href = link["href"]
        # Quanta article URLs follow this pattern
        if href.startswith("https://www.quantamagazine.org/") and href.endswith("/") and "-20" in href:
            if href not in article_urls:
                article_urls.append(href)
    
    return article_urls
