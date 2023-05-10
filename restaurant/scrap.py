import requests
from bs4 import BeautifulSoup
import mysql.connector

db = mysql.connector.connect(host="localhost",user="root",password="ID::nizarpleasedonthackmeagain$$4444endID",database="web2")
cursor = db.cursor()

url = 'https://fr.foursquare.com/explore?mode=url&near=France&nearGeoId=72057594040945318&q=Nourriture'
html = requests.get(url)
soup = BeautifulSoup(html.content, 'html.parser')
type_list = []
ratings_list = []
comments_list = []
locations_list = []
restaurantnames_list = []
img_list = []
typeresult = soup.findAll("span", class_='categoryName')
ratingresult = soup.findAll("div", class_='venueScore positive')
imgresult = soup.findAll("img", class_='photo')
neutralratingresult = soup.findAll("div", class_='venueScore neutral')
restaurantnameresult = soup.findAll("h2")
locationresult = soup.findAll("div", class_='venueAddress')
commentsresult = soup.findAll("p", class_='tipText')
for rating in ratingresult:
    rating_text = rating.text
    ratings_list.append(rating_text)
for neutralrating in neutralratingresult:
    neutralrating_text = neutralrating.text
    ratings_list.append(neutralrating_text)
for comment in commentsresult:
    comments_text = comment.text
    comments_list.append(comments_text)
for restaurantname in restaurantnameresult:
    restaurantnames_text = restaurantname.text
    restaurantnames_list.append(restaurantnames_text)
for location in locationresult:
    location_text = location.text
    locations_list.append(location_text)
for img in imgresult:
    img_text = img['src']
    img_list.append(img_text)
for type in typeresult:
    type_text = type.text
    type_list.append(type_text)

list_lengths = [len(l) for l in (type_list, ratings_list, comments_list, locations_list, restaurantnames_list, img_list)]
min_length = min(list_lengths)
# iterate over the lists and insert the data into the table
for i in range(min_length):
    # get the data from the lists for this iteration
    rating = ratings_list[i]
    comment = comments_list[i]
    location = locations_list[i]
    restaurantname = restaurantnames_list[i]
    img = img_list[i]
    type = type_list[i]

    # define the SQL query to insert the data into the table
    sql = "INSERT INTO scrapping (rating, location, restaurantname, comment, img, type) VALUES (%s, %s, %s, %s, %s, %s)"

    # define the values to be inserted into the table
    val = (rating, location, restaurantname, comment, img, type)

    # execute the SQL query with the values
    cursor.execute(sql, val)
db.commit()
cursor.close()
db.close()
# print a message indicating how many rows were inserted
print(cursor.rowcount, "rows were inserted.")
