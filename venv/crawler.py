from bs4 import BeautifulSoup
import requests
import json
from pymongo import MongoClient


dailyFresh='https://www.dailyfresh-chemnitz.de/'
ganesha='https://www.ganeshaindischespezialitaeten.de/menu/'
maharani='https://www.maharanihohndorf.de'

Rname=[dailyFresh,ganesha,maharani]

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")



    # Created or Switched to collection names:
db = conn.Menu
db.hotel.drop()
collection = db.hotel

class Menu:
    def __init__(self,Cat,Dish,Desc,Price,Rest):
        self.Category=Cat
        self.Dish=Dish
        self.Description=Desc
        self.Price=Price
        self.Restaurant=Rest

    def __repr__(self):
        return "Category :" + str(self.Category)  + "\nDish :" + str(self.Dish) + "\nDescription :" + str(self.Description) + "\nPrice :" + str(self.Price) + "\nRestaurant :" + str(self.Restaurant)


for RestName in Rname:
    source =requests.get(RestName).text 

    soup = BeautifulSoup(source,'lxml')

    r=[]
    count = 0  #Count for no. of categories
    order = 0

    for search1 in soup.find_all(class_='menucat'):
        order = order + 1
        if(order<2):
            continue
        semi = search1.text.split('\n')
        length = len(semi)
        length = int(length/10)
        n=0
        if(count==2):
            break
        while(length>0):
           # if(semi[7]!=''):
            z=semi[1]
            #else:
             #   break
            a=semi[n+9]
            b=semi[n+11]
            c=semi[n+7]
            if(RestName is dailyFresh):
                d='Daily Fresh'
            elif(RestName is ganesha):
                d='Ganesha Indische Spezialitäten'
            elif(RestName is maharani):
                d='Maharani'
            r.append(Menu(z,a,b,c,d))

            n=n+10
            length=length-1
            if(length==0):
                count = count + 1


    i=0
    for j in range(len(r)):

        details = {
            'Category':r[i].Category,
            'Dish':r[i].Dish,
            'Description':r[i].Description,
            'Price':r[i].Price,
            'Restaurant':r[i].Restaurant
            }
        i=i+1
        collection.insert_one(details)


    
    
