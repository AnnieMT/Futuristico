from flask import Flask,render_template,request,url_for
from urllib2 import Request, urlopen, URLError
import json
import sys
import datetime
import locale
import re
from py4j.java_gateway import JavaGateway
from pymongo import MongoClient
app = Flask(__name__)
connection = MongoClient('ds047800.mongolab.com',47800)
db = connection.moviedb
db.authenticate("cmpe239", "cmpe239")

prodColl = db.topProdHouse
actorsColl = db.topActors
direColl = db.topDirectors
genreColl = db.genre

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/homepage')
def homepage():
    return render_template('homepage.html') 

@app.route('/charts')
def charts():
    return render_template('charts.html') 

@app.route('/about')
def about():
    return render_template('about.html')     

@app.route('/contact')
def contact():
    return render_template('contact.html')  

@app.route('/highchart_genre')
def highchart_genre():
    return render_template('highchart_genre.html')

@app.route('/highchart_wikistat')
def highchart_wikistat():
    return render_template('highchart_wikistat.html')     

@app.route('/highchart_imdb_rating')
def highchart_imdb_rating():
    return render_template('highchart_imdb_rating.html') 

@app.route('/highchart_tomatoUserMeter')
def highchart_tomatoUserMeter():
    return render_template('highchart_tomatoUserMeter.html') 

@app.route('/highchart_metascore')
def highchart_metascore():
    return render_template('highchart_metascore.html') 

@app.route('/highchart_productionHouse_avg')
def highchart_productionHouse_avg():
    return render_template('highchart_productionHouse_avg.html') 

@app.route('/highchart_productionHouse_max')
def highchart_productionHouse_max():
    return render_template('highchart_productionHouse_max.html') 

@app.route('/highchart_productionHouse_num')
def highchart_productionHouse_num():
    return render_template('highchart_productionHouse_num.html') 

@app.route('/movie', methods=['POST'])
def index():
    movie = request.form['movie']
    print movie
    imdbTitle =  movie.replace(" ","%20")
    link = 'http://www.omdbapi.com/?i=&t=' + imdbTitle +'&tomatoes=true'      
    linkRequest = Request(link)
    try:
        
        linkResponse = urlopen(linkRequest)
        j = json.load(linkResponse)    
        print j['Title']    
     
    except :
        pass
        return render_template('index.html',errMsg="Pls Enter Correct Movie")
    try:
        rd = j['Released']
        date_time = datetime.datetime.strptime(rd,"%d %b %Y")
        t1= datetime.datetime.strftime(date_time, "%Y-%m-%d")
        Dates = t1.split()  
        Year= Dates[0][0:4]
        Month = Dates[0][5:7]
        t = Year+Month 
        Dates = t1.split()  
        Day= Dates[0][8:10]
        Month = Dates[0][5:7]
        if Month == "09":
           Month = 9
        elif Month == "08":
          Month = 8
        elif Day == "09":
          Day = 9
        elif Day == "08":
         Day = 8
        Month = int(Month)
        Day = int(Day)
        d = (Month,Day)
        print d
        d1 = (01,9)
        d2 = (01,19)
        d3 = (02,06)
        d4 = (02,16)
        d5 = (05,15)
        d6 = (05,25)
        d7 = (06,24)
        d8 = (07,04)
        d9 = (8,28)
        d10 = (9,07)
        d11 = (10,02)
        d12 =(10,12)
        d13 = (10,21)
        d14= (10,31)
        d15 = (11,01)
        d16 = (11,11)
        d17 = (11,16)
        d18 = (11,26)
        d19 = (12,15)
        d20 = (12,31)
        d21 = (01,01)
     
        if (d1 <= d <= d2) or ( d3 <= d <= d4) or (d5<= d <= d6) or (d7 <= d <= d8) or (d9 <= d <= d10) or (d11<= d<= d12) or (d13<= d<=d14) or (d15<= d<= d16) or (d17 <= d <= d18) or (d19<= d<= d20) :
	        status = "1"
        else:
          if (d == d21)   :
             status = "1"
          else:
             status = "0";
        try:
            wiki_url = 'http://stats.grok.se/json/en/'+t+'/'+movie
            print wiki_url
            wiki_read = json.loads(urlopen(wiki_url).read())
            total_views = sum([count for count in wiki_read['daily_views'].values()])
            total_str =str(total_views)
            print total_str
        except :
            pass
                    
        imdb_genre = j['Genre'].replace(",","-")
        j['Title'] = j['Title'].replace(",","-")
        imdb_Actors = j['Actors'].replace(",","-") 
        imdb_Director = j['Director'].replace(",","-") 
        imdb_Awards = j['Awards'].replace(",","-") 
        imdb_Production = j['Production'].replace(",","-")   
        imdb_votes = j['imdbVotes'].replace(",","") 
        tomatoUserReviews = j['tomatoUserReviews'].replace(",","") 
        tomatoUserRating = j['tomatoUserRating'].replace(",","") 
        tomatoUserMeter = j['tomatoUserMeter'].replace(",","") 
        imdb_rating = j['imdbRating'].replace(",","")
        Rated = j['Rated'].replace(",","")
        Metascore = j['Metascore'].replace(",","")
        print "*********"
        if 'USA' in j['Country']:
            print "comin"
            resultant = j['Title'] +','+ imdb_genre +','+ imdb_Actors +','+imdb_Director +','+imdb_Awards+',' +imdb_Production+','+imdb_rating +',' + imdb_votes + ','+j['Released']+','+ tomatoUserReviews +','+tomatoUserRating+','+tomatoUserMeter                 
            print resultant   
        else:
            return render_template('index.html',errMsg="Pls Enter USA Movie")
    except:
            return render_template('index.html',errMsg="Pls Enter Correct Movie")
    try:
        genre=imdb_genre.strip()             
        query = {"genre":genre}
        colums = {"_id":1}
        doc = genreColl.find_one(query,colums)
        if doc is None:
            genreId=0 
        else:
            genreId = doc['_id']
        print "genre Id " + `genreId`
        
        topActorCount=0
        actors=imdb_Actors
        actorList = actors.split("-")
        for actors in actorList:
            actor = actors.strip()           
            query = {"actor":actor}
            colums = {"_id":1}
            doc = actorsColl.find_one(query,colums)
            if doc is None:
                print actor
            else:
                topActorCount = topActorCount+1
        print "topActorCount "+`topActorCount`
        
        topDirectorCount=0
        imdb_Director = j['Director'].replace(",","-") 
        dires=imdb_Director
        direList = dires.split("-")
        for directors in direList:
            director = directors.strip()           
            query = {"director":director}
            colums = {"_id":1}
            doc = direColl.find_one(query,colums)
            if doc is None:
                print director
            else:
                topDirectorCount = topDirectorCount+1
                
        print("topDirectorCount "+`topDirectorCount`)
        
        
         
        prod=imdb_Production
        prodList = prod.split("/")
        cnt = 0
           
        for prodHouse in prodList:
                cnt = cnt+ 1
                if (cnt == 1):
                    productioHouse = prodHouse.strip()
                    #print productioHouse
                    if "Screen Media" in productioHouse:
                        productioHouse="SMedia"
                    elif "Screen Gems" in productioHouse:
                        productioHouse="SGems"
                    elif "Open Road Films" in productioHouse:
                        productioHouse = "OpRd"
                    elif "Metro-Goldwyn-Mayer" in productioHouse:
                        productioHouse ="MGM"
                    elif  "FilmBuff" in productioHouse:
                        productioHouse = "Buff"
                    elif "Tribeca" in productioHouse:
                        productioHouse = "Tribecca"
                    elif "FilmDistrict" in productioHouse:
                        productioHouse="District"
                    elif "New Films" in productioHouse:
                        productioHouse = "NeFm"
                    elif "LD Entertainment"  in productioHouse:
                        productioHouse = "LDEnte"
                    elif "Vitagraph" in productioHouse:
                        productioHouse ="ViGrp"
                    elif "Area 23a"   in productioHouse:
                        productioHouse = "Area23A"
                    elif "Arc Entertainment"   in productioHouse:
                        productioHouse = "ArcEn"
                    elif "FilmDisctrict" in productioHouse:
                        productioHouse = "District"
                    elif "High Top" in productioHouse:
                        productioHouse="Hightop"
                    elif "Millennium"  in productioHouse:
                        productioHouse="Milennium"
                    elif "Radius-TWC" in productioHouse:
                        productioHouse="Radius"
                    elif "World Wide"in productioHouse:
                        productioHouse="WrlWid"
                    elif "First Independent Pictures" in productioHouse:
                        productioHouse = "FirInde"
                    elif "New Line Cinema" in productioHouse:
                        productioHouse = "Warner"
                    elif "TriStar" in productioHouse:
                        productioHouse = "Sony"
                    elif "Stage 6" in productioHouse:
                        productioHouse = "Sony"
                    elif "Touchstone Pictures" in productioHouse:
                        productioHouse = "Walt"
                    elif "Disneynature"in productioHouse:
                        productioHouse = "Walt"
                    elif "Focus Features"in productioHouse:
                        productioHouse = "Universal"
                    elif "Nickelodeon" in productioHouse:
                        productioHouse = "Paramount"
                    elif "Roadside" in productioHouse:
                        productioHouse = "Lionsgate"
                    elif "Dimension" in productioHouse:
                        productioHouse = "Weinstein"
                        
                    
                    doc = db.command("text", "topProdHouse",search=productioHouse, project={"_id": 1})
                    rs = doc['results']
                    #print rs
                    if rs == []:
                        
                        prodHouseId=0
                    else:
                        print productioHouse
                        prodHouseId=1
            
        print "prodHouseId "+`prodHouseId` 

    except:
            return render_template('index.html',errMsg="Error while transforming the data")
        
    gateway = JavaGateway() 
    predictionModel = gateway.entry_point

    #Genre Production Released Actor Director imdbRating Metascore Wikistats BoxOffice */
    output=predictionModel.boxOfficePre(str(genreId),str(prodHouseId),str(status),str(topActorCount),str(topDirectorCount),imdb_rating,Metascore,total_str)
    print "Hi "+`output`
    boxOfficeValue=""
    if output==0.0:
        boxOfficeValue="181--200000"
    elif output==1.0:
        boxOfficeValue="200000--5000000"
    elif output==2.0:
        boxOfficeValue="5000000--20000000"
    elif output==3.0:
        boxOfficeValue="20000000--40000000"
    elif output==4.0:
        boxOfficeValue="40000000--80000000"
    elif output==5.0:
        boxOfficeValue="80000000--760500000"
    parts = boxOfficeValue.split("--")	
    value1 = parts[0]
    value2 = parts[1]
    mid = (int(value1) + int(value2))/2
    if mid > 100000000:
       mid = 100000000
    return render_template('predict.html',boxOffice=boxOfficeValue,high_chart = mid, title = movie,plot = j['Plot'])
 
if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 9000)
