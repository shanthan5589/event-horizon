import requests
from bs4 import BeautifulSoup

def fetch_article(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract title
    title = soup.find("h1")
    title_text = title.get_text(strip=True) if title else "No title found"
    
    # Extract article body paragraphs
    paragraphs = soup.find_all("p")
    body_text = "\n\n".join([p.get_text(separator=" ", strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 100])

    # Remove comment section garbage
    cutoff_phrases = [
        "Quanta Magazine moderates comments",
        "Share this article",
        "Newsletter",
        "Get Quanta Magazine"
    
    ]
    for phrase in cutoff_phrases:
        if phrase in body_text:
            body_text = body_text[:body_text.index(phrase)]
    
    return {
        "title": title_text,
        "url": url,
        "text": body_text
    }