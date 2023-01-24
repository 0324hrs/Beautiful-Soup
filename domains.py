from bs4 import BeautifulSoup, Stylesheet
import requests, openpyxl
sni_link = "https://bestwebsiterank.com/domains/.ke"

def urls():
    url_data = openpyxl.Workbook()
    sheet = url_data.active
    sheet.title = "SNI TO SCRAP"
    sheet.append(["URL"])
    
    try:
        for page in range(1,250):
            page_response = requests.get(f"{sni_link}/{page}")
            scrappy(page_response, sheet)
    except Exception as e:
        print(e)
    url_data.save("extra_pages.xlsx")
    print("DONE SCRAPING")
    checkSNI()

def checkSNI():
    sni_data = openpyxl.load_workbook("extra_pages.xlsx")
    sheet = sni_data.active
    sni_list = []
    for row in range(2, sheet.max_row + 1):
        row_value = 'http://'+sheet.cell(row, 1).value
        row_value = row_value.replace(" ", "")
        sni_list.append(row_value)
    sni_data.close()
    for sni in sni_list:
        try:
            sni_response = requests.get(sni)
            if sni_response.status_code == 200:
                sni_name = sni_response.headers['Server']
                sni_url = sni_response.url
                print(sni_name+" - "+sni_url)
        except Exception as e:
            print(e)
    sni_data.close()
    print("DONE CHECKING")

def scrappy(response, page):
    # print(domains.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_domains = soup.find_all('tr', class_= "")

    for domain in all_domains:
        domain = domain.find('td', class_='').text
        domain = str(domain)
        domain = domain.split(":")
        qt = domain[1]
        page.append([qt])
    next_present =  soup.div.find('li', class_= 'col-xs-12')
    if next_present is not None:
        next_page = requests.get(sni_link + next_present.a.get('href'))
        scrappy(next_page, page)
    
    
if __name__ == '__main__':
    urls()