from bs4 import BeautifulSoup
import requests
import pandas as pd

baseurl = "https://books.toscrape.com/"
productlinks = []

for x in range(1, 2):
  r = requests.get(f"https://books.toscrape.com/catalogue/page-{x}.html")
  soup = BeautifulSoup(r.content, "html.parser")

  productlist = soup.find_all("article", class_="product_pod")

  for item in productlist:
    # Fixed: Target only the <a> tag inside the <h3> to avoid duplicate links
    link = item.h3.find("a", href=True)
    if link:
      href = link["href"]
      if href.startswith("catalogue/"):
        productlinks.append(baseurl + href)
      else:
        productlinks.append(baseurl + "catalogue/" + href)

# Optional safety check: Remove any accidental duplicates
productlinks = list(dict.fromkeys(productlinks))
print(f"Total links found: {len(productlinks)}")

booklist = []
for link in productlinks:
  r = requests.get(link)
  soup = BeautifulSoup(r.content, "html.parser")

  title = soup.find("h1").get_text(strip=True)
  price = soup.find("p", class_="price_color").text.strip()
  stock = soup.find("p", class_="instock").text.strip()

  books = {"Title": title, "Price": price, "Stock": stock}

  booklist.append(books)


df = pd.DataFrame(booklist, columns=["Title", "Price", "Stock"])
#print(df.head(5))

# To save as a CSV file
df.to_csv("books_scraped.csv", index=False, encoding="utf-8")
# OR To save as an Excel file (requires openpyxl: pip install openpyxl)
# df.to_excel("books_scraped.xlsx", index=False)