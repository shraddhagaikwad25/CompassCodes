from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
    
    
)
from bson.regex import Regex
import pandas as pd
from flask import Flask,json
from datetime import datetime
from pandas.io.json import json_normalize
import pandas as pd
import pycountry
import numpy as np
from flask_cors import CORS
from geolite2 import geolite2
import time
from datetime import timedelta
import pymongo
from pymongo import MongoClient
from pprint import pprint
import urllib.parse
from pandas import DataFrame
from bson.objectid import ObjectId
import datetime
import dateutil.parser
from datetime import date
import calendar
import re
from sort_dataframeby_monthorweek import *
from pytz import timezone
from six.moves import urllib

app = Flask(__name__)
CORS(app)


# from flask_login import logout_user
class User:
    def __init__(self, id, username, password,name):
        self.id = id
        self.username = username
        self.password = password
        self.name = name

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='admin@innerexplorer.org', password='datateam2020',name='Admin'))
users.append(User(id=2, username='mituser', password='M!t_@2o20$',name='MIT'))


app = Flask(__name__)
app.secret_key = 'cap4g2020version10date8272020'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
        

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('Parents_Analytics'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/homepage')
def homepage():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('homepage.html')

@app.route('/Executive_Dashboard')
def Executive_Dashboard():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('Executive_Dashboard.html')


@app.route('/School_Analytics')
def School_Analytics():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('School_Analytics.html')

@app.route('/Family_School_Search')
def Family_School_Search():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('Family_School_Search.html')

@app.route('/School_Search')
def School_Search():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('School_Search.html')



@app.route('/Practice_Analytics')
def Practice_Analytics():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('Practice_Analytics.html')


@app.route('/Subscription_Expired')
def Subscription_Expired():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('Subscription_Expired.html')


@app.route('/feedback_Analyitcs')
def feedback_Analyitcs():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('feedback_Analyitcs.html')


@app.route('/feedback_Trends')
def feedback_Trends():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('feedback_Trends.html')


@app.route('/aws')
def aws():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('aws.html')


@app.route('/Upcoming_Renewals')
def Upcoming_Renewals():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('Upcoming_Renewals.html')

@app.route('/IOS_Analytics')
def IOS_Analytics():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('IOS_Analytics.html')

@app.route('/Android_analytics')
def Android_analytics():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('Android_analytics.html')

@app.route('/Sms_analytics')
def Sms_analytics():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('Sms_analytics.html')

@app.route('/District_level_view_SKILLMAN')
def District_level_view_SKILLMAN():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('District_level_view_SKILLMAN.html')

@app.route('/Parents_map_view')
def Parents_map_view():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('Parents_map_view.html')

@app.route('/Transaction_Reporting')
def Transaction_Reporting():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('Transaction_Reporting.html')

@app.route('/Progarm_wise_Analytics')
def Progarm_wise_Analytics():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('Progarm_wise_Analytics.html')

@app.route('/Family_practice_analytics')
def Family_practice_analytics():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('Family_practice_analytics.html')

@app.route('/Familyapp_school')
def Familyapp_school():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('Familyapp_school.html')

@app.route('/District_level_Parent_view')
def District_level_Parent_view():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('District_level_Parent_view.html')


@app.route('/Parents_Analytics')
def Parents_Analytics():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('Parents_Analytics.html')

@app.route('/District_level_view_RUSD')
def District_level_view_RUSD():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('District_level_view_RUSD.html')

@app.route('/District_level_view_HILLSBOROUGH')
def District_level_view_HILLSBOROUGH():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('District_level_view_HILLSBOROUGH.html')

@app.route('/District_level_view_FAIRFIELD')
def District_level_view_FAIRFIELD():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('District_level_view_FAIRFIELD.html')

@app.route('/District_level_view_LAUSD')
def District_level_view_LAUSD():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('District_level_view_LAUSD.html')
@app.route('/District_level_view_Search')
def District_level_view_Search():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('District_level_view_Search.html')

@app.route('/District_level_view_BROWARD')
def District_level_view_BROWARD():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('District_level_view_BROWARD.html')

@app.route('/District_level_view_SARASOTA')
def District_level_view_SARASOTA():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('District_level_view_SARASOTA.html')


@app.route('/District_level_view_youngstown')
def District_level_view_youngstown():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('District_level_view_youngstown.html')

@app.route('/District_level_view_Englewood')
def District_level_view_Englewood():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('District_level_view_Englewood.html')

@app.route('/Schoolsearch_Email')
def Schoolsearch_Email():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('Schoolsearch_Email.html')

@app.route('/Journey_score', methods=['GET', 'POST'])
def popup1():
    if request.method == 'POST':
        try:
                
            editorname = request.form['NAME']
        except:
            pass
        try:    
            statename = request.form['myBrowser1']
        except:
            pass
        try:
            cityname = request.form['myBrowser']
        except:
            pass
        try:

            email = request.form['email']
        except:
            pass
        try:

            district = request.form['myBrowser3']
        except:
            pass
        try:
                
            partner = request.form['myBrowser4']
        except:
            pass




@app.route('/mitcount')
def mitcount():


    username = urllib.parse.quote_plus('admin')
    password = urllib.parse.quote_plus('F5tMazRj47cYqm33e')
    client = MongoClient("mongodb://%s:%s@35.88.43.45:27017/" % (username, password))

    db=client.compass
    collection = db.user_master
    collection2 = db.audio_track_master

    dateStr = "2020-03-17T00:00:00.000Z"
    myDatetime = dateutil.parser.parse(dateStr)


    df = DataFrame(list(collection.aggregate([
        {"$match":{'ROLE_ID.ROLE_ID' :3, 
                   "IS_DISABLED":{"$ne":"Y"},
                   "INCOMPLETE_SIGNUP":{"$ne":"Y"},
                   "EMAIL_ID":{'$not':{'$regex':'test', '$options':'i'}},
                   'USER_TYPE':{"$regex":'mit','$options':'i'}, 
                   "EMAIL_ID":{"$ne": "Null"},
                   "EMAIL_ID":{"$not":{"$regex" : '1gen'}},
                   "USER_NAME":{'$not':{'$regex':'test', '$options':'i'}},
                   "CREATED_DATE":{"$gt": myDatetime}}},
        {"$group":{"_id":{}, 'distinct':{"$addToSet":'$_id'}}},
        {"$project":{"_id":0, 'Total_parents':{'$size':'$distinct'}}}])))




    total_parents = df['Total_parents'][0]
    total_downloads=round(total_parents*.95)
    downloadper=round((total_downloads/total_parents)*100)
    ios=round(total_downloads*0.60)
    android=round(total_downloads*0.40)

    temp={"download":[str(total_downloads)],"downloadper":[str(downloadper)],"android":[str(android)],"ios":[str(ios)],'totalparents':[str(total_parents)]}
    return json.dumps(temp)

@app.route('/newcardmit')
def mitpracticedatacard():
    


    username = urllib.parse.quote_plus('admin')
    password = urllib.parse.quote_plus('F5tMazRj47cYqm33e')
    client = MongoClient("mongodb://%s:%s@35.88.43.45:27017/" % (username, password))

    db=client.compass
    collection = db.audio_track_master
    query=[
        {"$match":{"$and":[{'USER_ID.ROLE_ID.ROLE_ID':{"$eq":3}},                  
                {'USER_ID.EMAIL_ID':{"$not":{"$regex":'test','$options':'i'}}},
                {'USER_ID.USER_NAME':{"$not":{"$regex":'test','$options':'i'}}},
                {'USER_ID.IS_DISABLE':{"$ne":'Y'}},
                {'USER_ID.INCOMPLETE_SIGNUP':{"$ne":'Y'}},
                {'USER_ID.EMAIL_ID':{"$not":{"$regex":'1gen','$options':'i'}}},
                {'USER_ID.USER_TYPE':{"$regex":'MIT','$options':'i'}},
                {'USER_ID.EMAIL_ID':{'$ne':''}}
                ]}},
        {"$project":{'USER_ID':'$USER_ID.USER_ID','PROGRAM_AUDIO_ID.AUDIO_ID':1,
            'PROGRAM_AUDIO_ID.PROGRAM_ID.PROGRAM_ID':1,
            'AGE_GROUP':'$PROGRAM_AUDIO_ID.PROGRAM_ID.AGE_GROUP',
            'AUDIO_NAME':1,'AUDIO_LENGTH':1,
            'IS_DONE':1,'PROGRAM_AUDIO_ID.AUDIO_DAY':1,'PROGRAM_AUDIO_ID.AUDIO_LENGTH':1,
            'Mindful_Minutes':{"$round":[{"$divide":[{"$subtract":['$CURSOR_END','$cursorStart']},60]},2]},        
            'PlayBack_Time_Percent':{"$round":[{"$divide":[{"$subtract":
                ['$CURSOR_END','$cursorStart']},'$PROGRAM_AUDIO_ID.AUDIO_LENGTH']},2]}}}       

                ]
    Overall=list(collection.aggregate(query))
    Overall_df=pd.DataFrame(Overall)
    card_df=pd.DataFrame({'engaged':len(set(Overall_df.USER_ID.tolist())),
                'active':len(set(Overall_df[Overall_df['PlayBack_Time_Percent']>=.5]['USER_ID'].tolist())),
                'passive':len(set(Overall_df.USER_ID.tolist()))-
                        len(set(Overall_df[Overall_df['PlayBack_Time_Percent']>=.5]['USER_ID'].tolist())),
                'playbackpractice':len(Overall_df),
                'minutespractice':Overall_df.Mindful_Minutes.sum().round()
                },index=[0]).reset_index(drop=True)
    temp2={}        
    for j in range(len(card_df.columns)):
        key = card_df.columns[j]
        value = [str(card_df[card_df.columns[j]].iloc[0])]
        temp2.update({key:value})
    return json.dumps(temp2)

@app.route('/mitsignupsnew')
def miitsignupnew():    
    username = urllib.parse.quote_plus('admin')
    password = urllib.parse.quote_plus('F5tMazRj47cYqm33e')
    client = MongoClient("mongodb://%s:%s@35.88.43.45:27017/" % (username, password))

    db = client.compass
    collection = db.user_master
    dateStr = "2020-03-17T00:00:00.000Z"
    myDatetime = dateutil.parser.parse(dateStr)
    query=[
    {"$match":{'ROLE_ID._id':ObjectId("5f155b8a3b6800007900da2b"), 
        "IS_DISABLED":{"$ne":"Y"},
        "INCOMPLETE_SIGNUP":{"$ne":"Y"},
        "EMAIL_ID":{'$not':{'$regex':'test', '$options':'i'}},
        'USER_TYPE':{"$regex":'mit','$options':'i'}, 
        "EMAIL_ID":{"$ne": ""},
        "EMAIL_ID":{'$not':{'$regex':'1gen', '$options':'i'}},
        "USER_NAME":{'$not':{'$regex':'test', '$options':'i'}},
        "CREATED_DATE":{"$gt":myDatetime}}},
        {"$group":{"_id":"$_id","CREATED_DATE":{"$first": "$CREATED_DATE"}}},
    {"$project":{"_id":0,'sign_up':{"$dateToString":{"format": "%Y-%m-%d","date":'$CREATED_DATE'}}}}
    ]
    df1=pd.DataFrame(list(collection.aggregate(query)))
    df1['sign_upn'] = pd.to_datetime(df1['sign_up']) 
    df2 = df1.groupby([df1['sign_upn'].dt.date]).count()

    cdate=[]
    for i in df2.index:
        x=i.strftime('%S')
        cdate.append(float(x)*1000)
    count=[]
    for i in df2['sign_up'] :
        count.append(i)
    count1=np.cumsum(count)
    df3 = pd.DataFrame(list(zip(cdate,count)), 
                    columns =['date', 'count']) 
    df4 = pd.DataFrame(list(zip(cdate,count1)), 
                    columns =['date', 'count'])
    data = df3.values.tolist()
    data1 = df4.values.tolist()
    return json.dumps({"bar":data,"line":data1})


@app.route('/mitsignupdaycompp')

def mitsignupdaycomp211():


    username = urllib.parse.quote_plus('admin')
    password = urllib.parse.quote_plus('F5tMazRj47cYqm33e')
    client = MongoClient("mongodb://%s:%s@35.88.43.45:27017/" % (username, password))

    db=client.compass
    collection = db.user_master
    dateStr = "2020-03-17T00:00:00.000Z"
    myDatetime = dateutil.parser.parse(dateStr)
    ##################### TODAY ###########################
    df = DataFrame(list(collection.aggregate([
        {"$match":{'ROLE_ID.ROLE_ID' :3, 
                "IS_DISTABLED":{"$ne":"Y"},
                "INCOMPLETE_SIGNUP":{"$ne":"Y"},
                "EMAIL_ID":{"$not":{"$regex" : 'test'}},
                'USER_TYPE':{"$regex":'mit','$options':'i'}, 
                "EMAIL_ID":{"$ne": ""},
                "EMAIL_ID":{"$not":{"$regex" : '1gen'}},
                "USER_NAME":{"$not":{"$regex" : 'test'}},
                "CREATED_DATE":{"$gt": myDatetime}}},
        {"$group":{"_id":{"$dateToString": {"date":'$CREATED_DATE'}}, 'distinct':{"$addToSet":'$_id'}}},
        {"$project":{"_id":1, 'Total_parents':{'$size':'$distinct'}}},
        { '$sort': { '_id': 1 }}])))
    df= df.rename(columns={"_id": "sign_up"})
    df1=df.dropna()
    df1['sign_up'] = pd.to_datetime(df1['sign_up'], errors = 'coerce')
    df1['sign_upn'] = pd.to_datetime(df1['sign_up']) - timedelta(hours=4)
    df1['date']=df1['sign_upn'].apply(lambda x: x.strftime("%Y-%m-%d"))
    from datetime import datetime
    from pytz import timezone
    tz = timezone('US/Eastern')
    date=datetime.now(tz)
    yesterday=pd.to_datetime(date)-timedelta(days=1)
    todaydate=date.strftime("%Y-%m-%d")
    yesterdaydate=yesterday.strftime("%Y-%m-%d")
    dfyes=df1[df1['date']==yesterdaydate]
    dftod=df1[df1['date']==todaydate]
    data = pd.DataFrame({'hour':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],'count':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]} )
    times = pd.to_datetime(dfyes.sign_upn)
    times['hour'] = times.map( lambda x: pd.to_datetime(x).hour )
    timedfyes=times.groupby(['hour']).size().to_frame('count').reindex(data['hour']).fillna(0)
    times2 = pd.to_datetime(dftod.sign_upn)
    times2['hour'] = times2.map( lambda x: pd.to_datetime(x).hour )
    timedftod=times2.groupby(['hour']).size().to_frame('count').reindex(data['hour']).fillna(0)
    timedfyes = timedfyes.astype(int)
    hour=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
    count=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    dftest = pd.DataFrame({'hour':hour,'count':count})
    result = pd.merge(timedfyes , dftest,how='right', on='hour')
    result=result.fillna(0)
    result= result.astype(int)
    result = result.sort_values(["hour", "count_x"], ascending = (True,False))
    #yesterday count
    yescount=list(result['count_x'])
    timedftod = timedftod.astype(int)
    result12 = pd.merge(timedftod, dftest,how='right', on='hour')
    result12=result12.fillna(0)
    result12= result12.astype(int)
    result12 = result12.sort_values(["hour", "count_x"], ascending = (True,False))
    #todays count
    todcount=list(result12['count_x'])
    totaly=sum(yescount)
    totalt=sum(todcount)
    temp={"tod":todcount,"yes":yescount,"totaly":[str(totaly)],"totalt":[str(totalt)]}
    return json.dumps(temp)


@app.route('/mitsignupweek')
def mitsignupweek():
    username = urllib.parse.quote_plus('admin')
    password = urllib.parse.quote_plus('F5tMazRj47cYqm33e')
    client = MongoClient("mongodb://%s:%s@35.88.43.45:27017/" % (username, password))

    db=client.compass
    collection = db.user_master

    dateStr = "2020-03-17T00:00:00.000Z"
    myDatetime = dateutil.parser.parse(dateStr)

    ##### HOURLY #################

    df1 = DataFrame(list(collection.aggregate([
        {"$match":{'ROLE_ID._id':ObjectId("5f155b8a3b6800007900da2b"), 
                "IS_DISABLED":{"$ne":"Y"},
                "INCOMPLETE_SIGNUP":{"$ne":"Y"},
                "EMAIL_ID":{'$not':{'$regex':'test', '$options':'i'}},
                'USER_TYPE':{"$regex":'mit','$options':'i'}, 
                "EMAIL_ID":{"$ne": ""},
                "EMAIL_ID":{'$not':{'$regex':'1gen', '$options':'i'}},
                "USER_NAME":{'$not':{'$regex':'test', '$options':'i'}},
                "CREATED_DATE":{"$gt": myDatetime}}},
        {"$group":{"_id":{"DATE": "$CREATED_DATE"}, 'distinct':{"$addToSet":'$_id'}}},
        {"$project":{"_id":0,"sign_up":"$_id.DATE"}}])))
    df1['sign_upn'] = pd.to_datetime(df1['sign_up']) - timedelta(hours=4)
    df2 = df1.groupby([df1['sign_upn'].dt.date]).count()

    cdate=[]
    for i in df2.index:
        x=i.strftime('%S')
        cdate.append(float(x)*1000)
    count=[]
    for i in df2['sign_up'] :
        count.append(i)
    count1=np.cumsum(count)
    df3 = pd.DataFrame(list(zip(cdate,count)), 
                        columns =['date', 'count']) 
    df4 = pd.DataFrame(list(zip(cdate,count1)), 
                        columns =['date', 'count'])
    data = df3.values.tolist()
    data1 = df4.values.tolist()


    ##### hourly graph

    times = pd.to_datetime(df1.sign_upn)
    times['hour'] = times.map( lambda x: pd.to_datetime(x).hour )
    timedf=times.groupby(['hour']).size().to_frame('count').reset_index()
    timedata0={"hour":timedf['hour'].tolist(),"count":timedf['count'].tolist()}
    timedata1=pd.DataFrame(timedata0)
    hour=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
    df10 = pd.DataFrame(hour,columns =['hour'])
    timedata2 = pd.merge(timedata1 , df10,how='right', on='hour').fillna(0)
    timedata3=timedata2.sort_values('hour')
    timedata={"hour":timedata3['hour'].tolist(),"count":timedata3['count'].tolist()}

    ###### week data
    df_data = pd.to_datetime(df1['sign_upn'], format='%Y%m%d')
    day=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday']
    week_df= df_data.groupby(df1['sign_upn'].dt.day_name()).count().reindex(day).fillna(0) 


    weekdata={"day":['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'],"count":[str(week_df['Monday']),str(week_df['Tuesday']),str(week_df['Wednesday']),str(week_df['Thursday']),str(week_df['Friday']),str(week_df['Saturday']),str(week_df['Sunday'])]}
    temp={"weekdata":weekdata,"timedata":timedata}
    return json.dumps(temp)



@app.route('/mitpracnew')
def mitpracnew():

    username = urllib.parse.quote_plus('admin')
    password = urllib.parse.quote_plus('F5tMazRj47cYqm33e')
    client = MongoClient("mongodb://%s:%s@35.88.43.45:27017/" % (username, password))

    db=client.compass
    collection = db.audio_track_master

    dateStr = "2020-03-17T00:00:00.000Z"
    myDatetime = dateutil.parser.parse(dateStr)


    x =list(collection.aggregate([
        {"$match":{"$and":[{'USER_ID.ROLE_ID._id':{"$eq":ObjectId("5f155b8a3b6800007900da2b")}},                  
                {'USER_ID.EMAIL_ID':{"$not":{"$regex":'test','$options':'i'}}},
                {'USER_ID.USER_NAME':{"$not":{"$regex":'test','$options':'i'}}},
                {'USER_ID.IS_DISABLE':{"$ne":'Y'}},
                {'USER_ID.INCOMPLETE_SIGNUP':{"$ne":'Y'}},
                {'USER_ID.EMAIL_ID':{"$not":{"$regex":'1gen','$options':'i'}}},
                {'USER_ID.USER_TYPE':{"$regex":'MIT','$options':'i'}},
                {'USER_ID.EMAIL_ID':{'$ne':''}}
                ]}},
        {"$group":{"_id":{"$dateToString": {"format": "%Y-%m-%d","date":'$CREATED_DATE'}},
                'Count':{"$sum":1}}},
        {"$project":{"_id":1, 'Parents_Practice':'$Count'}}]))
    res = [] 
    for idx, sub in enumerate(x, start = 0): 
        if idx == 0: 
    #         res.append(list(sub.keys())) 
            res.append(list(sub.values())) 
        else: 
            res.append(list(sub.values())) 
    df = pd.DataFrame(res, columns = ['date', 'count'])
    df['date'] = pd.to_datetime(df['date'], errors = 'coerce')
    df['date'] = pd.to_datetime(df['date']) - timedelta(hours=4)
    df2 = df.groupby([df['date'].dt.date]).sum()
    cdate=[]
    for i in df2.index:
        x=i.strftime('%S')
        cdate.append(float(x)*1000)
    count=[]
    for i in df2['count'] :
        count.append(i)
    count1=np.cumsum(count)
    df3 = pd.DataFrame(list(zip(cdate,count)), 
                    columns =['date', 'count']) 
    df4 = pd.DataFrame(list(zip(cdate,count1)), 
                    columns =['date', 'count'])
    data = df3.values.tolist()
    data1 = df4.values.tolist()
    return json.dumps({"bar":data,"line":data1})


@app.route('/mitpracweek')
def mitpracweek():
    


    username = urllib.parse.quote_plus('admin')
    password = urllib.parse.quote_plus('F5tMazRj47cYqm33e')
    client = MongoClient("mongodb://%s:%s@35.88.43.45:27017/" % (username, password))

    db=client.compass
    collection = db.audio_track_master

    dateStr = "2020-03-17T00:00:00.000Z"
    myDatetime = dateutil.parser.parse(dateStr)


    ############# DAY WISE #####################

    df = DataFrame(list(collection.aggregate([
        {"$match":{'USER_ID.USER_NAME':{"$not": {'$regex' : 'test', '$options' : 'i'}},
                 'USER_ID.IS_DISABLED':{"$ne":'Y'},'USER_ID.INCOMPLETE_SIGNUP':{"$ne":'Y'},
                 'USER_ID.USER_TYPE':{"$regex":'mit','$options':'i'}, 
                 'USER_ID.EMAIL_ID':{"$not": {'$regex' : 'test', '$options' : 'i'}},
                 'USER_ID.EMAIL_ID':{"$not": {'$regex' : '1gen', '$options' : 'i'}},
                 'USER_ID.EMAIL_ID':{"$ne":""},
                 'USER_ID.CREATED_DATE':{"$gt":myDatetime},
                 'USER_ID.ROLE_ID.ROLE_ID':{"$eq":3}}},
        {"$group":{"_id":{'DayOfWeek':{'$dayOfWeek':'$MODIFIED_DATE'}},
                 'Count':{"$sum":1}}},
        {"$project":{"_id":1, 'Parents_Practice':'$Count'}}])))

    df['DayOfWeek'] = pd.json_normalize(df['_id'])
    del df["_id"]
    weekdata={"day":['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday', 'Sunday'],"count":[str(df['Parents_Practice'][0]),str(df['Parents_Practice'][2]),
                                                                                                            str(df['Parents_Practice'][4]),str(df['Parents_Practice'][1]),
                                                                                                            str(df['Parents_Practice'][5]),str(df['Parents_Practice'][6]),str(df['Parents_Practice'][3])]}


    ############### HOURLY ########################################



    df_hour = DataFrame(list(collection.aggregate([
        {"$match":{'USER_ID.USER_NAME':{"$not": {'$regex' : 'test', '$options' : 'i'}},
                 'USER_ID.IS_DISABLED':{"$ne":'Y'},'USER_ID.INCOMPLETE_SIGNUP':{"$ne":'Y'},
                 'USER_ID.USER_TYPE':{"$regex":'mit','$options':'i'}, 
                 'USER_ID.EMAIL_ID':{"$not": {'$regex' : 'test', '$options' : 'i'}},
                 'USER_ID.EMAIL_ID':{"$not": {'$regex' : '1gen', '$options' : 'i'}},
                 'USER_ID.EMAIL_ID':{"$ne":""},
                 'USER_ID.CREATED_DATE':{"$gt":myDatetime},
                 'USER_ID.ROLE_ID.ROLE_ID':{"$eq":3}}},
        {"$group":{"_id":{"hour": {"$hour": "$MODIFIED_DATE"}},'Count':{"$sum":1}}},
        {"$project":{"_id":1, 'Parents_Practice':'$Count'}}])))

    df_hour['hour'] = pd.json_normalize(df_hour['_id'])
    del df_hour["_id"]
    df1_hour=df_hour.sort_values(by = ["hour"])
    timedata={"hour":df1_hour['hour'].tolist(),"count":df1_hour['Parents_Practice'].tolist()}



    temp={"weekdata":weekdata,"timedata":timedata}
    return json.dumps(temp)

@app.route('/mitpracdaycompp')
def mitsignupdaycomp12():
    username = urllib.parse.quote_plus('admin')
    password = urllib.parse.quote_plus('F5tMazRj47cYqm33e')
    client = MongoClient("mongodb://%s:%s@35.88.43.45:27017/" % (username, password))

    db=client.compass
    collection = db.audio_track_master
    dateStr = "2020-03-17T00:00:00.000Z"
    myDatetime = dateutil.parser.parse(dateStr)
    ##################### TODAY ###########################
    df = DataFrame(list(collection.aggregate([
            {"$match":{'USER_ID.USER_NAME':{"$not": {'$regex' : 'test', '$options' : 'i'}},
                    'USER_ID.IS_DISABLED':{"$ne":'Y'},'USER_ID.INCOMPLETE_SIGNUP':{"$ne":'Y'},
                    'USER_ID.USER_TYPE':{"$regex":'mit','$options':'i'}, 
                    'USER_ID.EMAIL_ID':{"$not": {'$regex' : 'test', '$options' : 'i'}},
                    'USER_ID.EMAIL_ID':{"$not": {'$regex' : '1gen', '$options' : 'i'}},
                    'USER_ID.EMAIL_ID':{"$ne":""},
                    'USER_ID.CREATED_DATE':{"$gt":myDatetime},
                    'USER_ID.ROLE_ID.ROLE_ID':{"$eq":3}}},
            {"$group":{"_id":{"$dateToString": {"date":'$MODIFIED_DATE'}},'Count':{"$sum":1}}},
            {"$project":{"_id":1, 'Parents_Practice':'$Count'}}])))
    df= df.rename(columns={"_id": "sign_up"})
    df1=df.dropna()
    df1['sign_up'] = pd.to_datetime(df1['sign_up'], errors = 'coerce')
    df1['sign_upn'] = pd.to_datetime(df1['sign_up']) - timedelta(hours=4)
    df1['date']=df1['sign_upn'].apply(lambda x: x.strftime("%Y-%m-%d"))
    from datetime import datetime
    from pytz import timezone
    tz = timezone('US/Eastern')
    date=datetime.now(tz)
    yesterday=pd.to_datetime(date)-timedelta(days=1)
    todaydate=date.strftime("%Y-%m-%d")
    yesterdaydate=yesterday.strftime("%Y-%m-%d")
    dfyes=df1[df1['date']==yesterdaydate]
    dftod=df1[df1['date']==todaydate]
    data = pd.DataFrame({'hour':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],'count':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]} )
    times = pd.to_datetime(dfyes.sign_upn)
    times['hour'] = times.map( lambda x: pd.to_datetime(x).hour )
    timedfyes=times.groupby(['hour']).size().to_frame('count').reindex(data['hour']).fillna(0)
    times2 = pd.to_datetime(dftod.sign_upn)
    times2['hour'] = times2.map( lambda x: pd.to_datetime(x).hour )
    timedftod=times2.groupby(['hour']).size().to_frame('count').reindex(data['hour']).fillna(0)
    timedfyes = timedfyes.astype(int)
    hour=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
    count=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    dftest = pd.DataFrame({'hour':hour,'count':count})
    result = pd.merge(timedfyes , dftest,how='right', on='hour')
    result=result.fillna(0)
    result= result.astype(int)
    result = result.sort_values(["hour", "count_x"], ascending = (True,False))
    #yesterday count
    yescount=list(result['count_x'])
    timedftod = timedftod.astype(int)
    result12 = pd.merge(timedftod, dftest,how='right', on='hour')
    result12=result12.fillna(0)
    result12= result12.astype(int)
    result12 = result12.sort_values(["hour", "count_x"], ascending = (True,False))
    #todays count
    todcount=list(result12['count_x'])
    totaly=sum(yescount)
    totalt=sum(todcount)
    temp={"tod":todcount,"yes":yescount,"totaly":[str(totaly)],"totalt":[str(totalt)]}
    
    
    return json.dumps(temp)



@app.route('/pracparents')
def pracparents_table():
    reader = geolite2.reader()

    username = urllib.parse.quote_plus('admin')
    password = urllib.parse.quote_plus('F5tMazRj47cYqm33e')
    client = MongoClient("mongodb://%s:%s@35.88.43.45:27017/" % (username, password))
    db=client.compass

    collection = db.user_master
    collection2 = db.audio_track_master

    dateStr = "2020-03-17T00:00:00.000Z"
    myDatetime = dateutil.parser.parse(dateStr)

    df = DataFrame(list(collection.aggregate([
        {"$match":{'ROLE_ID.ROLE_ID' :3, 
                   "IS_DISTABLED":{"$ne":"Y"},
                   "INCOMPLETE_SIGNUP":{"$ne":"Y"},
                   "EMAIL_ID":{"$ne": ""}}},
        {"$match":{"$and":[{"EMAIL_ID":{"$not":{"$regex":'1gen','$options':'i'}}},
                           {"USER_NAME":{"$not":{"$regex":'test','$options':'i'}}},
                          {"EMAIL_ID":{"$not":{"$regex":'test','$options':'i'}}}]}},
        {"$match":{"$and":[{"CREATED_DATE":{"$gt": myDatetime}}]}},
        {"$project":{"USER_ID":1,"USER_NAME":1,"EMAIL_ID":1,"CONTACT_NUMBER":1,"schoolId.CITY":1,
                     "schoolId.STATE":1,"schoolId.COUNTRY":1,
                     "schoolId.NAME":1,"schoolId.ADDRESS":1,"CREATED_DATE":1}}])))

    df1=df[['_id','schoolId']]
    df2 = df1.dropna()
    schoolId = list(df2['_id'])
    df2 = pd.json_normalize(df2['schoolId'])
    df2['schoolId'] = schoolId

    merge=pd.merge(df, df2, how='left', left_on=['_id'], right_on=['schoolId'])
    del merge['schoolId_x'], merge['schoolId_y']
    merge['CREATED_DATE'] = pd.to_datetime(merge['CREATED_DATE'])

    df_audio = DataFrame(list(collection2.aggregate([
                {"$match":{'USER_ID.IS_DISABLED':{"$ne":'Y'},
                'USER_ID.INCOMPLETE_SIGNUP':{"$ne":'Y'},
                'USER_ID.EMAIL_ID':{"$ne":""},
                'USER_ID.CREATED_DATE':{"$gt":myDatetime},
                'USER_ID.ROLE_ID.ROLE_ID':{"$eq":3}}},
                {"$match":{"$and":[
                {'USER_ID.EMAIL_ID':{"$not": {'$regex' : 'test', '$options' : 'i'}}},
                {'USER_ID.EMAIL_ID':{"$not": {'$regex' : '1gen', '$options' : 'i'}}},
                {'USER_ID.USER_NAME':{"$not": {'$regex' : 'test', '$options' : 'i'}}}]}},
                {"$group":{"_id":"$USER_ID._id","Last_Practice_Date":{"$max":"$MODIFIED_DATE"},'Count':{"$sum":1}, 
                           "EMAIL":{"$first":"USER_ID.EMAIL_ID"}}},
                {"$project":{"_id":1, 'Practice_Count':'$Count',"Last_Practice_Date":1}}])))


    final = pd.merge(merge, df_audio, how='left', left_on=['_id'], right_on=['_id'])

    del final['_id']

    final['Last_Practice_Date'] = pd.to_datetime(final['Last_Practice_Date'])


    final['Last_Practice_Date'].fillna("NO PRACTICE", inplace=True)
    #df['Last_Login_Date']=pd.to_datetime(df['Last_Login_Date'])
    #df['Last_Login_Date'].fillna("NO LOGIN", inplace=True)
    final['Practice_Count'].fillna("NO PRACTICE", inplace=True)
    final['CREATED_DATE']=pd.to_datetime(final['CREATED_DATE'])
    final['NAME'].fillna("NO SCHOOL INFO", inplace=True)
    final['ADDRESS'].fillna("NO ADDRESS INFO", inplace=True)
    final['COUNTRY'].fillna("NO COUNTRY INFO", inplace=True)
    final['STATE'].fillna("NO STATE INFO", inplace=True)
    final['CITY'].fillna("NO CITY INFO", inplace=True)

    def country1(i):
        location = reader.get(i)
        c=(location['country']['names']['en'])
        return c
    def state1(i):
        location = reader.get(i)
        s=(location['subdivisions'][0]['names']['en'])
        return s
    def city1(i):
        location = reader.get(i)
        city=location['city']['names']['en']
        return city
    def pn_country(i):
        import phonenumbers
        import pycountry
        from phonenumbers.phonenumberutil import (
        region_code_for_country_code,
        region_code_for_number,)
        pn = phonenumbers.parse('+'+i)   
        country = pycountry.countries.get(alpha_2=region_code_for_number(pn))
        con=country.name
        return con

    #ip=df['ip_address'].tolist()
    phone_number=final['CONTACT_NUMBER'].tolist()
    Parents_Name=final['USER_NAME'].tolist()
    Parents_Email=final['EMAIL_ID'].tolist()
    School_Name=final['NAME'].tolist()
    state=final['STATE'].tolist()
    country=final['COUNTRY'].tolist()
    city=final['CITY'].tolist()
    sign_up_date=final['CREATED_DATE'].tolist()
    last_prac_date=final['Last_Practice_Date'].tolist()
    #last_login_date=final['Last_Login_Date'].tolist()
    practice_count=final['Practice_Count'].tolist()
    #mindful_minutes=final['mindful_minutes'].tolist()
    print(final.columns)
    if "export" in request.args:
        try:
            df1=final[['NAME', 'COUNTRY', 'CITY', 'STATE','USER_NAME',  'EMAIL_ID', 'CREATED_DATE',
        'Last_Practice_Date','Practice_Count']]
            csv = df1.to_csv(index=False)
            return Response(
                csv,
                mimetype="text/csv",
                headers={"Content-disposition":
                        "attachment; filename=SchoolData.csv"})
        except:
            return jsonify("Unauthorized Access")   
    else:
        state12 =  [each_string.lower() for each_string in state]
        cv={'pnn':Parents_Name,'pe':Parents_Email,'co':country,'pn':phone_number,'sn':School_Name,'ct':city,
                                   'st':state12,'sp':sign_up_date,'lp':last_prac_date,'pc':practice_count}
        dftry = pd.DataFrame.from_dict(cv)
        dftry= dftry.drop("co", axis=1)
        return json.dumps({"data":dftry.values.tolist()})

# pracparents_table()


@app.route('/paroverall')
def parents_table():
    reader = geolite2.reader()
    username = urllib.parse.quote_plus('admin')
    password = urllib.parse.quote_plus('F5tMazRj47cYqm33e')
    client = MongoClient("mongodb://%s:%s@35.88.43.45:27017/" % (username, password))
    db = client.compass

    collection = db.user_master
    collection2 = db.audio_track_master

    dateStr = "2020-03-17T00:00:00.000Z"
    myDatetime = dateutil.parser.parse(dateStr)

    df = DataFrame(list(collection.aggregate([
        {"$match":{'ROLE_ID.ROLE_ID' :3, 
                   "IS_DISTABLED":{"$ne":"Y"},
                   "INCOMPLETE_SIGNUP":{"$ne":"Y"},
                   "EMAIL_ID":{"$ne": ""}}},
        {"$match":{"$and":[{"EMAIL_ID":{"$not":{"$regex":'1gen','$options':'i'}}},
                           {"USER_NAME":{"$not":{"$regex":'test','$options':'i'}}},
                          {"EMAIL_ID":{"$not":{"$regex":'test','$options':'i'}}}]}},
        {"$match":{"$and":[{"CREATED_DATE":{"$gt": myDatetime}}]}},
        {"$project":{"USER_ID":1,"USER_NAME":1,"EMAIL_ID":1,"CONTACT_NUMBER":1,"schoolId.CITY":1,
                     "schoolId.STATE":1,"schoolId.COUNTRY":1,
                     "schoolId.NAME":1,"schoolId.ADDRESS":1,"CREATED_DATE":1}}])))

    df1=df[['_id','schoolId']]
    df2 = df1.dropna()
    schoolId = list(df2['_id'])
    df2 = pd.json_normalize(df2['schoolId'])
    df2['schoolId'] = schoolId

    merge=pd.merge(df, df2, how='left', left_on=['_id'], right_on=['schoolId'])
    del merge['schoolId_x'], merge['schoolId_y']
    merge['CREATED_DATE'] = pd.to_datetime(merge['CREATED_DATE'])

    df_audio = DataFrame(list(collection2.aggregate([
                {"$match":{'USER_ID.IS_DISABLED':{"$ne":'Y'},
                'USER_ID.INCOMPLETE_SIGNUP':{"$ne":'Y'},
                'USER_ID.EMAIL_ID':{"$ne":""},
                'USER_ID.CREATED_DATE':{"$gt":myDatetime},
                'USER_ID.ROLE_ID.ROLE_ID':{"$eq":3}}},
                {"$match":{"$and":[
                {'USER_ID.EMAIL_ID':{"$not": {'$regex' : 'test', '$options' : 'i'}}},
                {'USER_ID.EMAIL_ID':{"$not": {'$regex' : '1gen', '$options' : 'i'}}},
                {'USER_ID.USER_NAME':{"$not": {'$regex' : 'test', '$options' : 'i'}}}]}},
                {"$group":{"_id":"$USER_ID._id","Last_Practice_Date":{"$max":"$MODIFIED_DATE"},'Count':{"$sum":1}, 
                           "EMAIL":{"$first":"USER_ID.EMAIL_ID"}}},
                {"$project":{"_id":1, 'Practice_Count':'$Count',"Last_Practice_Date":1}}])))


    final = pd.merge(merge, df_audio, how='left', left_on=['_id'], right_on=['_id'])

    del final['_id']

    final['Last_Practice_Date'] = pd.to_datetime(final['Last_Practice_Date'])


    final['Last_Practice_Date'].fillna("NO PRACTICE", inplace=True)
    #df['Last_Login_Date']=pd.to_datetime(df['Last_Login_Date'])
    #df['Last_Login_Date'].fillna("NO LOGIN", inplace=True)
    final['Practice_Count'].fillna("NO PRACTICE", inplace=True)
    final['CREATED_DATE']=pd.to_datetime(final['CREATED_DATE'])
    final['NAME'].fillna("NO SCHOOL INFO", inplace=True)
    final['ADDRESS'].fillna("NO ADDRESS INFO", inplace=True)
    final['COUNTRY'].fillna("NO COUNTRY INFO", inplace=True)
    final['STATE'].fillna("NO STATE INFO", inplace=True)
    final['CITY'].fillna("NO CITY INFO", inplace=True)

    def country1(i):
        location = reader.get(i)
        c=(location['country']['names']['en'])
        return c
    def state1(i):
        location = reader.get(i)
        s=(location['subdivisions'][0]['names']['en'])
        return s
    def city1(i):
        location = reader.get(i)
        city=location['city']['names']['en']
        return city
    def pn_country(i):
        import phonenumbers
        import pycountry
        from phonenumbers.phonenumberutil import (
        region_code_for_country_code,
        region_code_for_number,)
        pn = phonenumbers.parse('+'+i)   
        country = pycountry.countries.get(alpha_2=region_code_for_number(pn))
        con=country.name
        return con

    #ip=df['ip_address'].tolist()
    phone_number=final['CONTACT_NUMBER'].tolist()
    Parents_Name=final['USER_NAME'].tolist()
    Parents_Email=final['EMAIL_ID'].tolist()
    School_Name=final['NAME'].tolist()
    state=final['STATE'].tolist()
    country=final['COUNTRY'].tolist()
    city=final['CITY'].tolist()
    sign_up_date=final['CREATED_DATE'].tolist()
    last_prac_date=final['Last_Practice_Date'].tolist()
    #last_login_date=final['Last_Login_Date'].tolist()
    practice_count=final['Practice_Count'].tolist()
    #mindful_minutes=final['mindful_minutes'].tolist()
    
    if "export" in request.args:
        try:
            df1=final[['NAME', 'COUNTRY', 'CITY', 'STATE','USER_NAME',  'EMAIL_ID', 'CREATED_DATE',
        'Last_Practice_Date','Practice_Count']]
            csv = df1.to_csv(index=False)
            return Response(
                csv,
                mimetype="text/csv",
                headers={"Content-disposition":
                        "attachment; filename=SchoolData.csv"})
        except:
            return jsonify("Unauthorized Access")   
    else:
        state12 =  [each_string.lower() for each_string in state]
        cv={'pnn':Parents_Name,'pe':Parents_Email,'co':country,'pn':phone_number,'sn':School_Name,'ct':city,
                                   'st':state12,'sp':sign_up_date,'lp':last_prac_date,'pc':practice_count}
        dftry = pd.DataFrame.from_dict(cv)
        dftry= dftry.drop("co", axis=1)
        return json.dumps({"data":dftry.values.tolist()})

# parents_table()


#==============================================================================================================

@app.route('/Family_SURVEY')
def Family_SURVEY():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('Family_SURVEY.html')

@app.route('/Bill_later')
def Bill_later():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('Bill_later.html')

@app.route('/feedback_Analyitcs_family')
def feedbackfamily():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('feedback_Analyitcs_family.html')

@app.route('/familycard')
def Journey_score2():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('familycard.html')

@app.route('/Journey_score')
def reportcard():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template('Journey_score.html')

@app.route("/logout")
def logout():
    session.pop('user_id', None)
    return render_template('login.html')


# if __name__ == '__main__':
#     app.run()
# if __name__ == '__main__':
#     app.run(host='172.31.58.47',port=5001)
if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
