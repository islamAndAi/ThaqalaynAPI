import requests
from bs4 import BeautifulSoup
import json
import os
from unidecode import unidecode



# the following code is used to scrape data from a single book in Thaqalayn.net. Simply change the URL on line 7 to that of the book you're trying to scrape.
# example URL: https://thaqalayn.net/book/13
bookPage = requests.get("https://thaqalayn.net/book/13")
bookSoup = BeautifulSoup(bookPage.content, "html.parser")
bookPageResults = bookSoup.find(id="content")
bookPageTitle = bookSoup.find("h1").get_text() #this will store the title of the book
bookPageTitle = unidecode(bookPageTitle)
bookPageTitle=bookPageTitle.replace(" ", "-")
bookPageTitle=bookPageTitle.replace("--","")
bookPageTitle=bookPageTitle.replace("`","")
bookPageTitle=bookPageTitle.replace("'","")
bookPageAuthor = bookSoup.find("h6").get_text()
authorAndTranslator = bookPageAuthor.split("\n")
author = authorAndTranslator[0].replace("Author: ","")
translator = authorAndTranslator[1].strip().replace("Translator: ","")
if "Ṭūsī" in bookPageAuthor:
        bookPageTitle = bookPageTitle+"-Tusi"
elif "Nuʿmānī" in bookPageAuthor:
        bookPageTitle = bookPageTitle+"-Numani"
hadithsArray=[]
counter = 1
chapterName = ""
for hadithlink in bookPageResults.find_all('a'):
    hadithPage = requests.get(hadithlink.get('href'))
    if hadithlink.find('span') != None:
        chapterName = hadithlink.find('span').get_text().strip() #retrieves the chapter name if stored in <span>
    if hadithlink.find('strong') != None:
        chapterName = hadithlink.find('strong').get_text().strip() #retrieves the chapter name if stored in <strong>
    hadithPageSoup = BeautifulSoup(hadithPage.content, "html.parser")
    hadithPageResults = hadithPageSoup.find_all("div",class_="card text-center") #returns an array containing all the hadiths of this particular chapter. Could be 1 hadith, or many.
    for hadith in hadithPageResults: 
        englishText = hadith.find_all("p", class_="card-texts text-start")[0].get_text() #this takes a hadith, finds all elements 'p' with particular class (english text), and gets the text for that element
        arabicText = hadith.find_all("p", class_="card-texts text-end libAr")[0].get_text()
        pElement = hadith.find_all('p') #this simply gets all 'p' elements for any particular hadith
        majlisiGrading = ""
        behdudiGrading = ""
        mohseniGrading = ""
        for element in pElement:
            if "Allamah Baqir al-Majlisi:" in element.get_text(): #if a majlisi grading is found, store it in variable.
                majlisiGrading = element.get_text()
            if "Shaykh Baqir al-Behbudi:" in element.get_text(): #if a behdudi grading is found, store it in a variable.
                behdudiGrading = element.get_text()
            if "Shaykh Asif al-Mohseni:" in element.get_text(): #if a mohseni grading is found, store it in a variable.
                mohseniGrading = element.get_text()
        hadithPageUrl = hadith.find_all('a', class_="btn btn-primary")[0].get('href')
        hadithObject = {
            "id" : counter,
            "book" : bookPageTitle,
            "chapter" : chapterName,
            "author": author,
            "translator": translator,
            "englishText" : englishText,
            "arabicText" : arabicText,
            "majlisiGrading" : majlisiGrading,
            "behdudiGrading" : behdudiGrading,
            "mohseniGrading" : mohseniGrading,
            "URL" : hadithPageUrl
        }
        counter += 1
        hadithsArray.append(hadithObject)
with open(bookPageTitle+".json", 'w', encoding='utf8') as json_file:
    json.dump(hadithsArray, json_file, ensure_ascii=False)














