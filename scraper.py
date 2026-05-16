# Website se data nikalne ke liye libraries
import requests
from bs4 import BeautifulSoup

# ============================================
# FUNCTION — Ek page ka text nikalo
# ============================================
def scrape_page(url):
    try:
        # URL pe request bhejo — page ka HTML lao
        response = requests.get(url, timeout=10)
        
        # HTML ko BeautifulSoup se parse karo
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Unnecessary cheezein hatao
        # Script aur style tags remove karo
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        
        # Sirf clean text nikalo
        text = soup.get_text()
        
        # Extra spaces aur blank lines hatao
        lines = [line.strip() for line in text.splitlines()]
        clean_text = "\n".join(
            line for line in lines if line
        )
        
        return clean_text
    
    except Exception as e:
        print(f"Error aaya {url}: {e}")
        return ""

# ============================================
# MAIN — Doctor website ke pages scrape karo
# ============================================

# Yahan doctor ki website ke pages daalo
pages = [
    "https://brandgrowth.tech",
    "https://brandgrowth.tech/services",
    "https://brandgrowth.tech/contact",
]

# Saara data store karne ke liye
all_text = ""

print("Scraping shuru ho rahi hai...")

# Har page scrape karo
for url in pages:
    print(f"Scraping: {url}")
    text = scrape_page(url)
    
    # Page ka naam aur text save karo
    all_text += f"\n\n=== PAGE: {url} ===\n\n"
    all_text += text

# Sab kuch ek file mein save karo
with open("website_data.txt", "w", encoding="utf-8") as f:
    f.write(all_text)

print("Done! website_data.txt file ban gayi.")
print(f"Total characters: {len(all_text)}")