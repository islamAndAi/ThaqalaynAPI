import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
import os
import requests
from unidecode import unidecode


#The following code creates a json with all the books, and with the min and max ranges.
# allBooksJson = []

URL = "https://thaqalayn.net/"
mainPage = requests.get(URL)
mainPageSoup = BeautifulSoup(mainPage.content, "html.parser")
mainPageResults = mainPageSoup.find(id="library")
absolute_path = os.path.dirname(__file__)
allBooksJson = []
count = 1
for bookLink in mainPageResults.find_all('a'):
    bookPage = requests.get(bookLink.get('href'))
    bookSoup = BeautifulSoup(bookPage.content, "html.parser")
    bookPageResults = bookSoup.find(id="content")
    bookPageTitle = bookSoup.find("h1").get_text() #this will store the title of the book
    bookPageTitle = unidecode(bookPageTitle)
    bookPageTitle=bookPageTitle.replace(" ", "-")
    bookPageTitle=bookPageTitle.replace("--","")
    bookPageTitle=bookPageTitle.replace("`","")
    bookPageTitle=bookPageTitle.replace("'","")
    bookPageAuthor = bookSoup.find("h6").get_text()
    if "Ṭūsī" in bookPageAuthor:
        r =requests.get('https://9pq0cudihi.execute-api.us-east-1.amazonaws.com/dev/api/Kitab-al-Ghayba-Tusi')
        array = json.loads(r.text)
        newBookObject = {"id":count,"BookName":bookPageTitle+"-Tusi","idRangeMin":1,"idRangeMax":len(array)}
    elif "Nuʿmānī" in bookPageAuthor:
        r =requests.get('https://9pq0cudihi.execute-api.us-east-1.amazonaws.com/dev/api/Kitab-al-Ghayba-Numani')
        array = json.loads(r.text)
        newBookObject = {"id":count,"BookName":bookPageTitle+"-Numani","idRangeMin":1,"idRangeMax":len(array)}
    else:
        r =requests.get('https://9pq0cudihi.execute-api.us-east-1.amazonaws.com/dev/api/'+bookPageTitle)
        array = json.loads(r.text)
        newBookObject = {"id":count,"BookName":bookPageTitle,"idRangeMin":1,"idRangeMax":len(array)}
    allBooksJson.append(newBookObject)
    count+=1  

with open("BookNames"+".json", 'w', encoding='utf8') as json_file:
    json.dump(allBooksJson, json_file, ensure_ascii=False)