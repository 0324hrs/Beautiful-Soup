from bs4 import BeautifulSoup, Stylesheet
import requests, openpyxl
quotes_link = "https://quotes.toscrape.com"

def quotes():
    quotes_data = openpyxl.Workbook()
    sheet = quotes_data.active
    sheet.title = "QUOTES TO SCRAP"
    sheet.append(["QUOTE", "AUTHOR", "TAGS"])
    try:
        quotes = requests.get(f"{quotes_link}/page/1/")
        quotes.raise_for_status()        
        scrappy(quotes,sheet)
    except Exception as e:
        print(e)
    quotes_data.save("QUOTES DATA.xlsx")

def scrappy(quotes, sheet):
    soup = BeautifulSoup(quotes.text, 'html.parser')
    all_qoutes = soup.find_all('div', class_= "quote")

    for quote in all_qoutes:
        qoute = quote.find('span', class_='text').text
        author = quote.select('small[itemprop="author"]')[0].text
        tags = ''.join([tag.text for  tag in quote.find('div', class_= "tags").find_all('a', class_= "tag")])
        about_page =requests.get(quotes_link + quote.select('span a')[0].get('href'))
        about_soup = BeautifulSoup(about_page.text, 'html.parser')
        # author_description = about_soup.find('div', class_= "author-description").text.strip()
        print(qoute, author, tags)
        sheet.append([qoute, author, tags])
            
    next_present =  soup.nav.ul.find('li', class_= 'next')
    if next_present is not None:
        next_page = requests.get(quotes_link + next_present.a.get('href'))
        scrappy(next_page, sheet)
    
    
if __name__ == '__main__':
    quotes()