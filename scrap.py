from  bs4 import BeautifulSoup
import requests, openpyxl


def scrapper():
    movies_data = openpyxl.Workbook()
    sheet = movies_data.active
    sheet.title = "IMDB TOP RATED"
# adding colums to our data sheet
    sheet.append(["Movie Rank", "Movie Name", "Release Year", "IMDB Rating"])

    try:
        movies = requests.get("https://www.imdb.com/chart/top/")
        movies.raise_for_status()
    
        soup = BeautifulSoup(movies.text, 'html.parser')
    # print(soup)
        movies_list = soup.find('tbody', class_= "lister-list").find_all('tr')
    # print(movies_list)
    # loop through the list to get all movies
        for movie in movies_list:
        # movie rank
            movie_rank = movie.find('td', class_= "titleColumn").get_text(strip = True).split(".")[0]
        
        # movie name
            movie_name = movie.find('td', class_= "titleColumn").a.text
        
        # movie year
            movie_year = movie.find('span', class_="secondaryInfo").text.strip("()")
        
        # movie rating
            movie_rating = movie.find('td', class_= "ratingColumn imdbRating").strong.text
            print(movie_rank, movie_name, movie_year, movie_rating)
        # to parse our data into our sheet
            sheet.append([movie_rank, movie_name, movie_year, movie_rating])
        
    except Exception as e:
        print(e)
# to save our movie data scrapped csv file
    movies_data.save("IMDB TOP RATED MOVIES.xlsx")

if __name__ == '__main__':
    scrapper()