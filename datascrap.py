from bs4 import BeautifulSoup
import requests, openpyxl

def main():
    data = openpyxl.Workbook()
    sheet = data.active
    sheet.title = "test dummy"
    
    try:
        scrapper(sheet)
        data.save("test dummy.xlsx")
    # break
    except Exception as e:
        print(e)

def scrapper(sheet):
    movies = requests.get("https://www.yidio.com/movies")
    movies.raise_for_status()

    soup = BeautifulSoup(movies.text, 'html.parser')
    # print(soup)
    all_movies = soup.find('div', class_= "cards").find_all('a', class_= "card")
    # for loop
    for movie in all_movies:
        #movie name
        movie_name = movie.find( class_= "title").text
        
        print(movie_name)
        sheet.append([movie_name])
    

if __name__ =='__main__':
    main()