from flask import Flask, jsonify, request,  render_template
from flask_pymongo import PyMongo
import json
import cgi
import re
import crawler  
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
import datetime
from datetime import tzinfo,timedelta,timezone




app = Flask(__name__, static_url_path='')

app.config['MONGO_DBNAME'] = 'Menu'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Menu'



mongo = PyMongo(app)


#app = Flask(__name__, static_url_path='')
#@app.route("/")
#def index():


@app.route('/',methods=['GET'])
def AllDishes():
    framework = mongo.db.hotel


    output = []
    for q in framework.find():
        output.append(
            {
                'Category' : q['Category'],
                'Dish' : q['Dish'],
                'Description' : q['Description'],
                'Price' : q['Price'],
                'Restaurant' : q['Restaurant']
            }
        )



    return render_template('index.html', output=output)

@app.route('/search',methods=['POST'])
def Search():
    form = cgi.FieldStorage()
    searchbox = request.form['searchbox']

    item = []


    framework = mongo.db.hotel

    for q in framework.find():


        if re.search(searchbox,q['Dish'],re.IGNORECASE):
            item.append(q)

    return render_template('articles.html',item=item)

@app.route('/update',methods=['POST'])
def Update():  
    output = [] 
    ut = []
    
    updatedTime = datetime.datetime.now(timezone.utc)

    dailyFresh='https://www.dailyfresh-chemnitz.de/'
    ganesha='https://www.ganeshaindischespezialitaeten.de/menu/'
    maharani='https://www.maharanihohndorf.de'

    Rname=[dailyFresh,ganesha,maharani]

    class Menu:
        def __init__(self,Cat,Dish,Desc,Price,Rest):
            self.Category=Cat
            self.Dish=Dish
            self.Description=Desc
            self.Price=Price
            self.Restaurant=Rest

        def __repr__(self):
            return "Category :" + str(self.Category)  + "\nDish :" + str(self.Dish) + "\nDescription :" + str(self.Description) + "\nPrice :" + str(self.Price) + "\nRestaurant :" + str(self.Restaurant)


    try:
        conn = MongoClient()
        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")

    db = conn.Menu
    
    timework = mongo.db.time
    if db.time.count() == 0 :
            
            ut = {
                'updatedTime':updatedTime
            }
            db.time.insert_one(ut)
            db.hotel.drop()
            collection = db.hotel
            

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

            framework = mongo.db.hotel

            
            for q in framework.find():
                output.append(
                    {
                        'Category' : q['Category'],
                        'Dish' : q['Dish'],
                        'Description' : q['Description'],
                        'Price' : q['Price'],
                        'Restaurant' : q['Restaurant']
                    }
                )
    else:


        for i in timework.find():
            c=updatedTime-i['updatedTime']
            if c>timedelta(hours=24):
                db.time.drop()

                ut.append( 
                    {
                    'updatedTime':updatedTime
                    }
                )

                db.time.insert_one(ut)
                db.hotel.drop()
                collection = db.hotel
                

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

                framework = mongo.db.hotel

                
                for q in framework.find():
                    output.append(
                        {
                            'Category' : q['Category'],
                            'Dish' : q['Dish'],
                            'Description' : q['Description'],
                            'Price' : q['Price'],
                            'Restaurant' : q['Restaurant']
                        }
                    )
                
            else:
                framework = mongo.db.hotel        
                for q in framework.find():
                    output.append(
                                {
                                    'Category' : q['Category'],
                                    'Dish' : q['Dish'],
                                    'Description' : q['Description'],
                                    'Price' : q['Price'],
                                    'Restaurant' : q['Restaurant']
                                }
                            )  
                

     
    return render_template('index.html', output=output)

    

if __name__ == '__main__':
    app.run(debug = True)
