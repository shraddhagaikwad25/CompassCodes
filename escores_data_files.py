import pymongo
from pymongo import MongoClient
from pprint import pprint
import urllib.parse
import pandas as pd
import numpy as np
from pandas import DataFrame
from bson.objectid import ObjectId
import datetime
import json
import urllib
import dateutil
# import timdelta
from flask import Flask,json
from flask_cors import CORS
app = Flask(__name__)
from pytz import timezone
import seaborn as sns
import missingno as msno
import pandas_profiling
from datetime import timedelta
app = Flask(__name__)
import calendar
import requests
from pandas import Timestamp
CORS(app)
from dateutil.relativedelta import relativedelta

#  new libraries to be imported 

from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
from sklearn.preprocessing import StandardScaler
import collections
import math
import os
from numpy import nan

def csy_first_date():
        date_today =datetime.date.today()
    #     print(date_today)
    #     date_today='2024-07-01'
    #     day_end=datetime.datetime.strptime(date_today, '%Y-%m-%d').date()
        initial_date='2020-08-01'
        day1=datetime.datetime.strptime(initial_date, '%Y-%m-%d').date()
        # Check if leap year in the calculation
        if ((day1.year+1) % 4) == 0:
            if ((day1.year+1) % 100) == 0:
                if ((day1.year+1) % 400) == 0:
                    days_diff=1
                else:
                    days_diff=1
            else:
                days_diff=1
        else:
            days_diff=0
        if ((date_today-day1).days<(365+days_diff)):
            day_1=day1
        else:
            day1=day1+timedelta(days=(365+days_diff))
            day_1=day1

        csy_date=datetime.datetime.strptime((day_1.strftime('%Y-%m-%d')), '%Y-%m-%d')


        return csy_date


def LSY_Date():

    LSY_Date=csy_first_date()-relativedelta(years=1)
    return LSY_Date

# live server credentials    
client_live= MongoClient('mongodb://admin:F5tMazRj47cYqm33e@54.202.61.130:27017/')
db_live=client_live.compass   


@app.route('/escoresdownloads/')


def escore_downloadsss():     
    
    def escore_overall_downloads(trackid):
        # live server credentials    
        client_live= MongoClient('mongodb://admin:F5tMazRj47cYqm33e@54.202.61.130:27017/')
        db_live=client_live.compass   
        pd.options.mode.chained_assignment = None
        def escore_school_downloads(trackid):
            schoolcond_um={'schoolId._id':ObjectId(trackid)}
            school_name_list=list(db_live.school_master.find({'_id':ObjectId(trackid)}))
            school_name=school_name_list[0].get('NAME')

            user_master_df=pd.DataFrame(list(db_live.user_master.aggregate(
            [{"$match":{'$and':[{ 'USER_NAME':{"$not":{"$regex":"test",'$options':'i'}}},
                            {'EMAIL_ID':{"$not":{"$regex":"test",'$options':'i'}}},
                                {'EMAIL_ID':{"$not":{"$regex":"1gen",'$options':'i'}}},
                    {'INCOMPLETE_SIGNUP':{"$ne":'Y'}},
                    {'IS_DISABLED':{"$ne":'Y'}},
                    {'IS_BLOCKED':{"$ne":'Y'}},
                    {'schoolId.NAME':{'$not':{"$regex":'Blocked','$options':'i'}}},
                    {'ROLE_ID._id':{'$ne':ObjectId("5f155b8a3b6800007900da2b")}},
                    {'schoolId.BLOCKED_BY_CAP':{'$exists':0}},
                                schoolcond_um
                            ]}},
                {'$project':{
                    '_id':0,
                    'USER_ID':'$_id',
                    'USER_NAME':'$USER_NAME',
                    'EMAIL_ID':'$EMAIL_ID',
                    'SIGNUP_DATE':'$CREATED_DATE',
                    'SCHOOL_ID':'$schoolId._id',
                    'SCHOOL_NAME':'$schoolId.NAME',
                    'ROLE_ID':'$ROLE_ID.ROLE_ID'
                    }}

                ])))

            if user_master_df.empty:
                score_output={
                'SCHOOL_ID':trackid,
                'SCHOOL_NAME':school_name,        
                'ACTIVE_USER_SCORE_SCHOOL':float(0),
                        'USAGE_SCORE_SCHOOL':float(0),
                        'CWP_SCORE_SCHOOL':float(0),
                        'RE_SCORE_SCHOOL':float(0),
                        'E_SCORE_SCHOOL':float(0),
                        'ACTIVE_SCHOOL':float(0)
                }

                return score_output

            audio_track_master_df=pd.DataFrame(list(db_live.audio_track_master.aggregate(
            [{"$match":{
                    '$and':[{ 'USER_ID.USER_NAME':{"$not":{"$regex":"test",'$options':'i'}}},
                            {'USER_ID.EMAIL_ID':{"$not":{"$regex":"test",'$options':'i'}}},
                                {'USER_ID.EMAIL_ID':{"$not":{"$regex":"1gen",'$options':'i'}}},
                    {'USER_ID.INCOMPLETE_SIGNUP':{"$ne":'Y'}},
                    {'USER_ID.IS_DISABLED':{"$ne":'Y'}},
                    {'USER_ID.IS_BLOCKED':{"$ne":'Y'}},
                    {'USER_ID.schoolId.NAME':{'$not':{"$regex":'Blocked','$options':'i'}}},
                    {'USER_ID.schoolId.BLOCKED_BY_CAP':{'$exists':0}},
                    {'cursorStart':{'$exists':1}},
                    {'CURSOR_END':{'$exists':1}},
                    {'USER_ID._id':{'$in':user_master_df['USER_ID'].tolist()}}       
                    ]}},          
                    {'$project':{
                        '_id':0,
                        'USER_ID':'$USER_ID._id',
                        'PRACTICE_DATE':'$MODIFIED_DATE',
                        'CURSOR_START':'$cursorStart',
                        'CURSOR_END':'$CURSOR_END'
                        }}             

                    ])))

            

            # <<<<<<<<<<<<<<<<<<<<<<-----------------------------USAGE SCORE----------------->>>>>>>>>>>>>>>>>>>>>>>>>>

            if audio_track_master_df.empty:
                score_output={
                'SCHOOL_ID':trackid,
                'SCHOOL_NAME':school_name,        
                'ACTIVE_USER_SCORE_SCHOOL':float(0),
                        'USAGE_SCORE_SCHOOL':float(0),
                        'CWP_SCORE_SCHOOL':float(0),
                        'RE_SCORE_SCHOOL':float(0),
                        'E_SCORE_SCHOOL':float(0),
                        'ACTIVE_SCHOOL':float(0)
                }

                return score_output

            audio_track_master_df['PRACTICE_DATE']=pd.to_datetime(audio_track_master_df['PRACTICE_DATE']).dt.date

            practising_dates=audio_track_master_df.groupby('USER_ID')['PRACTICE_DATE'].apply(list).reset_index().rename(columns={'PRACTICE_DATE':'DATES_OF_PRACTICING'})

            audio_track_master_df1=audio_track_master_df.groupby(['USER_ID']).agg({'PRACTICE_DATE':['min','max']
                                                                                }).rename(columns={'min':'FIRST_PRAC_DATE','max':'LAST_PRAC_DATE'}).droplevel(axis=1, level=0).reset_index()



            audio_track_master_df2=audio_track_master_df1.merge(practising_dates,how='left',on='USER_ID')

            for i in range(len(audio_track_master_df2)):
                new_value=list(set(audio_track_master_df2['DATES_OF_PRACTICING'][i]))
                audio_track_master_df2['DATES_OF_PRACTICING'][i]=new_value

            us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())

            BUSINESS_DAYS=[]
            for i in range(len(audio_track_master_df2['FIRST_PRAC_DATE'])):
                business_days=list(pd.date_range(start=audio_track_master_df2['FIRST_PRAC_DATE'][i],end=datetime.datetime.now().date(), freq=us_bd))
                bd=[]
                for j in range(len(business_days)):
                    bd.append(business_days[j].date())
                BUSINESS_DAYS.append(bd)



            audio_track_master_df2['BUSINESS_DAYS']=BUSINESS_DAYS

            audio_track_master_df2['POSSIBLE_PRACTISING_DAYS']=''
            for k in range(len(audio_track_master_df2['BUSINESS_DAYS'])):
                possible_prac_dates=len(audio_track_master_df2['BUSINESS_DAYS'][k])
                audio_track_master_df2['POSSIBLE_PRACTISING_DAYS'][k]=possible_prac_dates

            audio_track_master_df2['TOTAL_PRACTICE_DAYS']=''
            for l in range(len(audio_track_master_df2['DATES_OF_PRACTICING'])):
                dys=len(list(set(audio_track_master_df2['DATES_OF_PRACTICING'][l]).intersection(audio_track_master_df2['BUSINESS_DAYS'][l])))
                audio_track_master_df2['TOTAL_PRACTICE_DAYS'][l]=dys


            final_data1=audio_track_master_df2 
            
            final_data1['USAGE_METRIC']=''
            for i in range(len(final_data1)):
                if final_data1['POSSIBLE_PRACTISING_DAYS'][i]==0:
                    final_data1['USAGE_METRIC'][i]=0
                else:
                    final_data1['USAGE_METRIC'][i]=final_data1['TOTAL_PRACTICE_DAYS'][i]/final_data1['POSSIBLE_PRACTISING_DAYS'][i]
                    
                    

    #         final_data1['USAGE_METRIC']=final_data1['TOTAL_PRACTICE_DAYS']/final_data1['POSSIBLE_PRACTISING_DAYS']
            
            final_data1['USAGE_METRIC_STANDARDISATION']=''
            for kk in range(len(final_data1['USAGE_METRIC'])):
                if math.isnan(final_data1['USAGE_METRIC'].std()):                    
                    svalue=0
                else:                    
                    svalue=(final_data1['USAGE_METRIC'][kk] - final_data1['USAGE_METRIC'].mean())/final_data1['USAGE_METRIC'].std()
                
                final_data1['USAGE_METRIC_STANDARDISATION'][kk]=svalue
                


    #         final_data1['USAGE_METRIC_STANDARDISATION'] = StandardScaler().fit_transform(final_data1['USAGE_METRIC'])

            final_data1['USAGE_SCORE']=''
            for i in range(len(final_data1['USAGE_METRIC_STANDARDISATION'])):
                if final_data1['USAGE_METRIC_STANDARDISATION'][i]>0:                                
                    uscore=(0.5+(final_data1['USAGE_METRIC_STANDARDISATION'][i]/max(final_data1['USAGE_METRIC_STANDARDISATION'])))/2*100
                    final_data1['USAGE_SCORE'][i]=round(uscore,0)*10

                elif (final_data1['USAGE_METRIC_STANDARDISATION'][i]==0):                                
                    final_data1['USAGE_SCORE'][i]=0*10
                else:                    
                    uscore=((1-final_data1['USAGE_METRIC_STANDARDISATION'][i]/min(final_data1['USAGE_METRIC_STANDARDISATION']))/2)*100
                    final_data1['USAGE_SCORE'][i]=round(uscore,0)*10
#                     10 should be multiplied


            # <<<<<<<<<<<<<<<<<<<<<<<<------------------CONSISTENT WEEKLY PRACTICE SCORE---------------------->>>>>>>>>>>>>>>>>>>>>>>>>

            final_data2=final_data1

            final_data2['WEEK_SINCE_FIRST_PRACTICE']=np.ceil(round((datetime.datetime.now().date()-final_data2['FIRST_PRAC_DATE'])/np.timedelta64(1,'W'),3))

            PRACTISING_WEEK=[]
            for i in range(len(final_data2)):
                pw=[]
                for j in range(len(final_data2['DATES_OF_PRACTICING'][i])):
                    week=np.ceil(round((final_data2['DATES_OF_PRACTICING'][i][j]-final_data2['FIRST_PRAC_DATE'][i])/datetime.timedelta(days=7),3))
                    if week==0:
                        week=week+1
                    else:
                        week=week
                    pw.append(week)
                PRACTISING_WEEK.append(pw)


            WEEK_PRAC_FREQ=[]
            UNIQUE_WEEK_PRACTISED=[]
            for i in range(len(PRACTISING_WEEK)):
                WEEK_PRAC_FREQ.append(list(collections.Counter(PRACTISING_WEEK[i]).values()))
                UNIQUE_WEEK_PRACTISED.append(list(collections.Counter(PRACTISING_WEEK[i]).keys()))


            GAINED_POINTS=[]
            for i in range(len(WEEK_PRAC_FREQ)):
                points=[]
                for j in range(len(WEEK_PRAC_FREQ[i])):
                    if WEEK_PRAC_FREQ[i][j]==1:
                        point=1*WEEK_PRAC_FREQ[i][j]
                    elif WEEK_PRAC_FREQ[i][j]==2:
                        point=3*WEEK_PRAC_FREQ[i][j]
                    elif WEEK_PRAC_FREQ[i][j]==3:
                        point=10*WEEK_PRAC_FREQ[i][j]
                    elif WEEK_PRAC_FREQ[i][j]==4:
                        point=15*WEEK_PRAC_FREQ[i][j]
                    else:
                        point=20*WEEK_PRAC_FREQ[i][j]
                    points.append(point)
                GAINED_POINTS.append(sum(points))


            final_data2['PRACTISING_WEEK']=PRACTISING_WEEK
            final_data2['UNIQUE_WEEK_PRACTISED']=UNIQUE_WEEK_PRACTISED
            final_data2['WEEK_PRAC_FREQ']=WEEK_PRAC_FREQ
            final_data2['GAINED_POINTS']=GAINED_POINTS
            final_data2['CWP_SCORE']=round((final_data2['GAINED_POINTS']/(20*final_data2['WEEK_SINCE_FIRST_PRACTICE']))*100,0)*10
            final_data2.loc[(final_data2['CWP_SCORE']>100),'CWP_SCORE'] = 100*10
            #                     10 should be multiplied



            # <<<<<<<<<<<<<<<<<<<<-------------------RECENT ENGAGEMENT SCORE------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>

            final_data3=final_data2

            user_master_df['SIGNUP_DATE']=pd.to_datetime(user_master_df['SIGNUP_DATE']).dt.date

            final_data3=user_master_df[['USER_ID','SIGNUP_DATE']].merge(final_data3,how='inner',on='USER_ID').reset_index(drop=True)

            _30_day_data=[]
            points_30_day=[]

            _60_day_data=[]
            points_60_day=[]

            _180_day_data=[]
            points_180_day=[]

            _365_day_data=[]
            points_365_day=[]

            CSY_data=[]
            points_csy_day=[]

            Lifetime=[]
            points_Lifetime=[]


            for i in range(len(final_data3)):
                if (datetime.datetime.now().date()-final_data3['SIGNUP_DATE'][i]).days>=30:
                    dates30=list(pd.date_range(start=datetime.datetime.now().date()-timedelta(days=30),end=datetime.datetime.now().date(), freq=us_bd))
                    dates30=[j.date() for j in dates30]
                    _30_days=len(list(set(final_data3['DATES_OF_PRACTICING'][i]).intersection(dates30)))
                    if (_30_days>0) and (_30_days<len(dates30)/6):
                        points30=1
                    elif (_30_days==0):
                        points30=0
                    else:
                        points30=2
                else:
                    _30_days='not eligible'
                    points30='not eligible'
                _30_day_data.append(_30_days)
                points_30_day.append(points30)



            for i in range(len(final_data3)):
                if (datetime.datetime.now().date()-final_data3['SIGNUP_DATE'][i]).days>=60:
                    dates60=list(pd.date_range(start=datetime.datetime.now().date()-timedelta(days=60),end=datetime.datetime.now().date(), freq=us_bd))
                    dates60=[j.date() for j in dates60]
                    _60_days=len(list(set(final_data3['DATES_OF_PRACTICING'][i]).intersection(dates60)))
                    if (_60_days>0) and (_60_days<len(dates60)/6):
                        points60=1
                    elif (_60_days==0):
                        points60=0
                    else:
                        points60=2
                else:
                    _60_days='not eligible'
                    points60='not eligible'        
                _60_day_data.append(_60_days)
                points_60_day.append(points60)



            for i in range(len(final_data3)):
                if (datetime.datetime.now().date()-final_data3['SIGNUP_DATE'][i]).days>=180:
                    dates180=list(pd.date_range(start=datetime.datetime.now().date()-timedelta(days=180),end=datetime.datetime.now().date(), freq=us_bd))
                    dates180=[j.date() for j in dates180]
                    _180_days=len(list(set(final_data3['DATES_OF_PRACTICING'][i]).intersection(dates180)))
                    if (_180_days>0) and (_180_days<len(dates180)/6):
                        points180=1
                    elif (_180_days==0):
                        points180=0
                    else:
                        points180=2

                else:
                    _180_days='not eligible'
                    points180='not eligible'

                _180_day_data.append(_180_days)
                points_180_day.append(points180)



            for i in range(len(final_data3)):
                if (datetime.datetime.now().date()-final_data3['SIGNUP_DATE'][i]).days>=365:
                    dates365=list(pd.date_range(start=datetime.datetime.now().date()-timedelta(days=365),end=datetime.datetime.now().date(), freq=us_bd))
                    dates365=[j.date() for j in dates365]
                    _365_days=len(list(set(final_data3['DATES_OF_PRACTICING'][i]).intersection(dates365)))
                    if (_365_days>0) and (_365_days<len(dates365)/6):
                        points365=1
                    elif (_365_days==0):
                        points365=0
                    else:
                        points365=2
                else:
                    _365_days='not eligible'
                    points365='not eligible'

                _365_day_data.append(_365_days)
                points_365_day.append(points365)


            for i in range(len(final_data3)):
                dates_csy=list(pd.date_range(start=csy_first_date().date(),end=datetime.datetime.now().date(), freq=us_bd))
                dates_csy=[j.date() for j in dates_csy]
                csy_days=len(list(set(final_data3['DATES_OF_PRACTICING'][i]).intersection(dates_csy)))
                if (csy_days>0) and (csy_days<len(dates_csy)/6):
                    points_csy=1
                elif (csy_days==0):
                    points_csy=0
                else:
                    points_csy=2
                CSY_data.append(csy_days)
                points_csy_day.append(points_csy)





            for i in range(len(final_data3)):
                dates_lifetime=list(pd.date_range(start=final_data3['SIGNUP_DATE'][i],end=datetime.datetime.now().date(), freq=us_bd))
                dates_lifetime=[j.date() for j in dates_lifetime]
                lifetime_days=len(list(set(final_data3['DATES_OF_PRACTICING'][i]).intersection(dates_lifetime)))
                if (lifetime_days>0) and (lifetime_days<len(dates_lifetime)/6):
                    points_lifetime=1
                elif (lifetime_days==0):
                    points_lifetime=0
                else:
                    points_lifetime=2

                Lifetime.append(lifetime_days)
                points_Lifetime.append(points_lifetime)




            mergedata=[]
            for m,n,o,p,q,r in zip(points_30_day,points_60_day,points_180_day,points_365_day,points_csy_day,points_Lifetime):
                mergedata.append([m,n,o,p,q,r])


            final_data3['RE_SCORE']=''
            for i in range(len(mergedata)):
                xs=[s for s,val in enumerate(mergedata[i]) if val!='not eligible']
                check=len(xs)
                if check>0:
                    re_score=(sum([mergedata[i][q] for q in xs])/(2*check))*100
                else:
                    re_score=0
                final_data3['RE_SCORE'][i]=round(re_score,0)*10
                #                     10 should be multiplied


            # <<<<<<<<<<<<<<<<------------------------------ACTIVE USER SCORE------------------------>>>>>>>>>>>>>>>>>>>>>>>>>

            days_since_signup=[]
            for i in range(len(final_data3)):
                d_snup=(datetime.datetime.now().date()-final_data3['SIGNUP_DATE'][i]).days
                days_since_signup.append(d_snup)


            ACTIVE_USER=[]
            for i in range(len(days_since_signup)):
                p_days=len(final_data3['DATES_OF_PRACTICING'][i])
                if days_since_signup[i]>60:        
                    if p_days>=20:
                        active_user=1
                    else:
                        active_user=0
                else:
                    if p_days>=round((days_since_signup[i]/60)*20,0):
                        active_user=1
                    else:
                        active_user=0

                ACTIVE_USER.append(active_user)


            final_data3['ACTIVE_USER']=ACTIVE_USER
            #                     10 should be multiplied


            ACTIVE_USER_SCORE_SCHOOL=round((len(final_data3[final_data3['ACTIVE_USER']>0])/len(user_master_df))*100,0)*10

            USAGE_SCORE_SCHOOL=round(final_data3['USAGE_SCORE'].mean(),0)

            CWP_SCORE_SCHOOL=round(final_data3['CWP_SCORE'].mean(),0)

            RE_SCORE_SCHOOL=round(final_data3['RE_SCORE'].mean(),0)

            E_SCORE_SCHOOL=round((ACTIVE_USER_SCORE_SCHOOL+USAGE_SCORE_SCHOOL+CWP_SCORE_SCHOOL+RE_SCORE_SCHOOL)/4,0)

            if len(audio_track_master_df)>=5*len(user_master_df):

                ACTIVE_SCHOOL=1
            else:
                ACTIVE_SCHOOL=0

            score_output={
                'SCHOOL_ID':trackid,
                'SCHOOL_NAME':school_name,        
                'ACTIVE_USER_SCORE_SCHOOL':ACTIVE_USER_SCORE_SCHOOL,
                        'USAGE_SCORE_SCHOOL':USAGE_SCORE_SCHOOL,
                        'CWP_SCORE_SCHOOL':CWP_SCORE_SCHOOL,
                        'RE_SCORE_SCHOOL':RE_SCORE_SCHOOL,
                        'E_SCORE_SCHOOL':E_SCORE_SCHOOL,
                        'ACTIVE_SCHOOL':ACTIVE_SCHOOL  


                        }

            return score_output

        if len(list(db_live.district_master.find({'_id':ObjectId(str(trackid))})))>0:
            district_id=trackid
            districtinfo={
                '5f2609807a1c0000950bb45a':'LAUSD',
                '5f2609807a1c0000950bb45c':'Comox Valley School District'
            }
            
            if district_id in list(districtinfo):
                district_name=districtinfo[district_id]
            
    #         if district_id=='5f2609807a1c0000950bb45a':
    #             district_name='LAUSD'
            else:
                districtname=list(db_live.district_master.find({'_id':ObjectId(district_id)}))
                district_name=districtname[0].get('DISTRICT_NAME')
                
    #         districtname=list(db_live.district_master.find({'_id':ObjectId(district_id)}))
            
            schoolids=db_live.user_master.distinct('schoolId._id',
                                                
                                                {'schoolId._id':{'$in':db_live.school_master.distinct('_id',                                               
                                                {'CATEGORY':{'$regex':district_name,'$options':'i'}})}
                                                })
            df_s=[]
            for ii in range(len(schoolids)):
                schls= escore_school_downloads(str(schoolids[ii]))
                df_s.append(schls)
            schools_df=pd.DataFrame(df_s)
            
            schools_df['SCORE_TYPE']=''

            for i in range(len(schools_df)):
                if schools_df['E_SCORE_SCHOOL'][i]<=250:
                    schools_df['SCORE_TYPE'][i]='0-250'
                elif schools_df['E_SCORE_SCHOOL'][i]<=500:
                    schools_df['SCORE_TYPE'][i]='251-500'
                elif schools_df['E_SCORE_SCHOOL'][i]<=750:
                    schools_df['SCORE_TYPE'][i]='501-750'
                else:
                    schools_df['SCORE_TYPE'][i]='751-1000'
                    
                    
            if len(schools_df)>0:                
                file_name = str(trackid)+'_school_e_scores.csv'
                if(os.path.exists(file_name) and os.path.isfile(file_name)):
                    os.remove(file_name)
                    
                    


                schools_df.to_csv(str(trackid)+'_school_e_scores.csv',index=False)
                    
            else:
                pass
    
            #                     10 should be multiplied
            ACTIVE_SCHOOL_SCORE=round(sum(schools_df['ACTIVE_SCHOOL'])/len(set(schoolids))*100,0)*10
            E_SCORE=round((schools_df['ACTIVE_USER_SCORE_SCHOOL'].mean()+schools_df['USAGE_SCORE_SCHOOL'].mean()+schools_df['CWP_SCORE_SCHOOL'].mean()+schools_df['RE_SCORE_SCHOOL'].mean()+ACTIVE_SCHOOL_SCORE)/5)
            temp={
                'CREATED_DATE':datetime.datetime.now().date().strftime('%Y-%m-%d'),
                'DISTRICT_ID':trackid,
                'DISTRICT_NAME':district_name,
                'ACTIVE_USER_SCORE':round(schools_df['ACTIVE_USER_SCORE_SCHOOL'].mean(),0),
                'USAGE_SCORE':round(schools_df['USAGE_SCORE_SCHOOL'].mean(),0),
                'CWP_SCORE':round(schools_df['CWP_SCORE_SCHOOL'].mean(),0),
                'RE_SCORE':round(schools_df['RE_SCORE_SCHOOL'].mean(),0),
                'ACTIVE_SCHOOL_SCORE':ACTIVE_SCHOOL_SCORE,
                'E_SCORE':E_SCORE,
    #               'columchart':{'axis':new_schools_df1['SCORE_TYPE'].tolist(),
    #                            'schoolcount':new_schools_df1['School_Count'].tolist()
    #               '0-25':new_schools_df1[new_schools_df1['SCORE_TYPE']=='0-25'].reset_index()['School_Count'][0],
    #               '26-50':new_schools_df1[new_schools_df1['SCORE_TYPE']=='26-50'].reset_index()['School_Count'][0],
    #               '51-75':new_schools_df1[new_schools_df1['SCORE_TYPE']=='51-75'].reset_index()['School_Count'][0],
    #               '76-100':new_schools_df1[new_schools_df1['SCORE_TYPE']=='76-100'].reset_index()['School_Count'][0],
                
    #                             }
            }
            
            E_score_df=pd.DataFrame([temp])
            E_score_df.to_csv(str(trackid)+'_E_SCORE_DATA.csv',index=False)
            
            
            
            
            
            # <<<<<<<<<<<<<<<<<<<<-------------code for monthwise e-score of district:----------------------->>>>>>>>>>>>>>>>>>>>>


            def escore_mothwise(trackid,dateinlist):
                
                # live server credentials    
                client_live= MongoClient('mongodb://admin:F5tMazRj47cYqm33e@54.202.61.130:27017/')
                db_live=client_live.compass   
                pd.options.mode.chained_assignment = None
                def escore_school_monthwise(trackid):
                    schoolcond_um={'schoolId._id':ObjectId(trackid)}
                    school_name_list=list(db_live.school_master.find({'_id':ObjectId(trackid)}))
                    school_name=school_name_list[0].get('NAME')

                    user_master_df=pd.DataFrame(list(db_live.user_master.aggregate(
                    [{"$match":{'$and':[{ 'USER_NAME':{"$not":{"$regex":"test",'$options':'i'}}},
                                    {'EMAIL_ID':{"$not":{"$regex":"test",'$options':'i'}}},
                                        {'EMAIL_ID':{"$not":{"$regex":"1gen",'$options':'i'}}},
                            {'INCOMPLETE_SIGNUP':{"$ne":'Y'}},
                            {'IS_DISABLED':{"$ne":'Y'}},
                            {'IS_BLOCKED':{"$ne":'Y'}},
                            {'schoolId.NAME':{'$not':{"$regex":'Blocked','$options':'i'}}},
                            {'ROLE_ID._id':{'$ne':ObjectId("5f155b8a3b6800007900da2b")}},
                            {'schoolId.BLOCKED_BY_CAP':{'$exists':0}},
                                        schoolcond_um,

                                        {'CREATED_DATE':{'$lte':dateinlist}}

                                    ]}},
                        {'$project':{
                            '_id':0,
                            'USER_ID':'$_id',
                            'USER_NAME':'$USER_NAME',
                            'EMAIL_ID':'$EMAIL_ID',
                            'SIGNUP_DATE':'$CREATED_DATE',
                            'SCHOOL_ID':'$schoolId._id',
                            'SCHOOL_NAME':'$schoolId.NAME',
                            'ROLE_ID':'$ROLE_ID.ROLE_ID'
                            }}

                        ])))

                    if user_master_df.empty:
                        score_output={
                        'SCHOOL_ID':trackid,
                        'SCHOOL_NAME':school_name,        
                        'ACTIVE_USER_SCORE_SCHOOL':float(0),
                                'USAGE_SCORE_SCHOOL':float(0),
                                'CWP_SCORE_SCHOOL':float(0),
                                'RE_SCORE_SCHOOL':float(0),
                                'E_SCORE_SCHOOL':float(0),
                                'ACTIVE_SCHOOL':float(0)
                        }

                        return score_output

                    audio_track_master_df=pd.DataFrame(list(db_live.audio_track_master.aggregate(
                    [{"$match":{
                            '$and':[{ 'USER_ID.USER_NAME':{"$not":{"$regex":"test",'$options':'i'}}},
                                    {'USER_ID.EMAIL_ID':{"$not":{"$regex":"test",'$options':'i'}}},
                                        {'USER_ID.EMAIL_ID':{"$not":{"$regex":"1gen",'$options':'i'}}},
                            {'USER_ID.INCOMPLETE_SIGNUP':{"$ne":'Y'}},
                            {'USER_ID.IS_DISABLED':{"$ne":'Y'}},
                            {'USER_ID.IS_BLOCKED':{"$ne":'Y'}},
                            {'USER_ID.schoolId.NAME':{'$not':{"$regex":'Blocked','$options':'i'}}},
                            {'USER_ID.schoolId.BLOCKED_BY_CAP':{'$exists':0}},
                            {'cursorStart':{'$exists':1}},
                            {'CURSOR_END':{'$exists':1}},
                            {'USER_ID._id':{'$in':user_master_df['USER_ID'].tolist()}},
                                    {'MODIFIED_DATE':{'$lte':dateinlist}}
                            ]}},          
                            {'$project':{
                                '_id':0,
                                'USER_ID':'$USER_ID._id',
                                'PRACTICE_DATE':'$MODIFIED_DATE',
                                'CURSOR_START':'$cursorStart',
                                'CURSOR_END':'$CURSOR_END'
                                }}             

                            ])))



                    # <<<<<<<<<<<<<<<<<<<<<<-----------------------------USAGE SCORE----------------->>>>>>>>>>>>>>>>>>>>>>>>>>

                    if audio_track_master_df.empty:
                        score_output={
                        'SCHOOL_ID':trackid,
                        'SCHOOL_NAME':school_name,        
                        'ACTIVE_USER_SCORE_SCHOOL':float(0),
                                'USAGE_SCORE_SCHOOL':float(0),
                                'CWP_SCORE_SCHOOL':float(0),
                                'RE_SCORE_SCHOOL':float(0),
                                'E_SCORE_SCHOOL':float(0),
                                'ACTIVE_SCHOOL':float(0)
                        }

                        return score_output

                    audio_track_master_df['PRACTICE_DATE']=pd.to_datetime(audio_track_master_df['PRACTICE_DATE']).dt.date

                    practising_dates=audio_track_master_df.groupby('USER_ID')['PRACTICE_DATE'].apply(list).reset_index().rename(columns={'PRACTICE_DATE':'DATES_OF_PRACTICING'})

                    audio_track_master_df1=audio_track_master_df.groupby(['USER_ID']).agg({'PRACTICE_DATE':['min','max']
                                                                                        }).rename(columns={'min':'FIRST_PRAC_DATE','max':'LAST_PRAC_DATE'}).droplevel(axis=1, level=0).reset_index()



                    audio_track_master_df2=audio_track_master_df1.merge(practising_dates,how='left',on='USER_ID')

                    for i in range(len(audio_track_master_df2)):
                        new_value=list(set(audio_track_master_df2['DATES_OF_PRACTICING'][i]))
                        audio_track_master_df2['DATES_OF_PRACTICING'][i]=new_value

                    us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())

                    BUSINESS_DAYS=[]
                    for i in range(len(audio_track_master_df2['FIRST_PRAC_DATE'])):
                        business_days=list(pd.date_range(start=audio_track_master_df2['FIRST_PRAC_DATE'][i],end=datetime.datetime.now().date(), freq=us_bd))
                        bd=[]
                        for j in range(len(business_days)):
                            bd.append(business_days[j].date())
                        BUSINESS_DAYS.append(bd)



                    audio_track_master_df2['BUSINESS_DAYS']=BUSINESS_DAYS

                    audio_track_master_df2['POSSIBLE_PRACTISING_DAYS']=''
                    for k in range(len(audio_track_master_df2['BUSINESS_DAYS'])):
                        possible_prac_dates=len(audio_track_master_df2['BUSINESS_DAYS'][k])
                        audio_track_master_df2['POSSIBLE_PRACTISING_DAYS'][k]=possible_prac_dates

                    audio_track_master_df2['TOTAL_PRACTICE_DAYS']=''
                    for l in range(len(audio_track_master_df2['DATES_OF_PRACTICING'])):
                        dys=len(list(set(audio_track_master_df2['DATES_OF_PRACTICING'][l]).intersection(audio_track_master_df2['BUSINESS_DAYS'][l])))
                        audio_track_master_df2['TOTAL_PRACTICE_DAYS'][l]=dys


                    final_data1=audio_track_master_df2 

                    final_data1['USAGE_METRIC']=''
                    for i in range(len(final_data1)):
                        if final_data1['POSSIBLE_PRACTISING_DAYS'][i]==0:
                            final_data1['USAGE_METRIC'][i]=0
                        else:
                            final_data1['USAGE_METRIC'][i]=final_data1['TOTAL_PRACTICE_DAYS'][i]/final_data1['POSSIBLE_PRACTISING_DAYS'][i]



            #         final_data1['USAGE_METRIC']=final_data1['TOTAL_PRACTICE_DAYS']/final_data1['POSSIBLE_PRACTISING_DAYS']

                    final_data1['USAGE_METRIC_STANDARDISATION']=''
                    for kk in range(len(final_data1['USAGE_METRIC'])):
                        if math.isnan(final_data1['USAGE_METRIC'].std()):                    
                            svalue=0
                        else:                    
                            svalue=(final_data1['USAGE_METRIC'][kk] - final_data1['USAGE_METRIC'].mean())/final_data1['USAGE_METRIC'].std()

                        final_data1['USAGE_METRIC_STANDARDISATION'][kk]=svalue



            #         final_data1['USAGE_METRIC_STANDARDISATION'] = StandardScaler().fit_transform(final_data1['USAGE_METRIC'])
#                     10 should be multiplied
                    final_data1['USAGE_SCORE']=''
                    for i in range(len(final_data1['USAGE_METRIC_STANDARDISATION'])):
                        if final_data1['USAGE_METRIC_STANDARDISATION'][i]>0:                                
                            uscore=(0.5+(final_data1['USAGE_METRIC_STANDARDISATION'][i]/max(final_data1['USAGE_METRIC_STANDARDISATION'])))/2*100
                            final_data1['USAGE_SCORE'][i]=round(uscore,0)*10

                        elif (final_data1['USAGE_METRIC_STANDARDISATION'][i]==0):                                
                            final_data1['USAGE_SCORE'][i]=0*10
                        else:                    
                            uscore=((1-final_data1['USAGE_METRIC_STANDARDISATION'][i]/min(final_data1['USAGE_METRIC_STANDARDISATION']))/2)*100
                            final_data1['USAGE_SCORE'][i]=round(uscore,0)*10


                    # <<<<<<<<<<<<<<<<<<<<<<<<------------------CONSISTENT WEEKLY PRACTICE SCORE---------------------->>>>>>>>>>>>>>>>>>>>>>>>>

                    final_data2=final_data1

                    final_data2['WEEK_SINCE_FIRST_PRACTICE']=np.ceil(round((datetime.datetime.now().date()-final_data2['FIRST_PRAC_DATE'])/np.timedelta64(1,'W'),3))

                    PRACTISING_WEEK=[]
                    for i in range(len(final_data2)):
                        pw=[]
                        for j in range(len(final_data2['DATES_OF_PRACTICING'][i])):
                            week=np.ceil(round((final_data2['DATES_OF_PRACTICING'][i][j]-final_data2['FIRST_PRAC_DATE'][i])/datetime.timedelta(days=7),3))
                            if week==0:
                                week=week+1
                            else:
                                week=week
                            pw.append(week)
                        PRACTISING_WEEK.append(pw)


                    WEEK_PRAC_FREQ=[]
                    UNIQUE_WEEK_PRACTISED=[]
                    for i in range(len(PRACTISING_WEEK)):
                        WEEK_PRAC_FREQ.append(list(collections.Counter(PRACTISING_WEEK[i]).values()))
                        UNIQUE_WEEK_PRACTISED.append(list(collections.Counter(PRACTISING_WEEK[i]).keys()))


                    GAINED_POINTS=[]
                    for i in range(len(WEEK_PRAC_FREQ)):
                        points=[]
                        for j in range(len(WEEK_PRAC_FREQ[i])):
                            if WEEK_PRAC_FREQ[i][j]==1:
                                point=1*WEEK_PRAC_FREQ[i][j]
                            elif WEEK_PRAC_FREQ[i][j]==2:
                                point=3*WEEK_PRAC_FREQ[i][j]
                            elif WEEK_PRAC_FREQ[i][j]==3:
                                point=10*WEEK_PRAC_FREQ[i][j]
                            elif WEEK_PRAC_FREQ[i][j]==4:
                                point=15*WEEK_PRAC_FREQ[i][j]
                            else:
                                point=20*WEEK_PRAC_FREQ[i][j]
                            points.append(point)
                        GAINED_POINTS.append(sum(points))

#                     10 should be multiplied
                    final_data2['PRACTISING_WEEK']=PRACTISING_WEEK
                    final_data2['UNIQUE_WEEK_PRACTISED']=UNIQUE_WEEK_PRACTISED
                    final_data2['WEEK_PRAC_FREQ']=WEEK_PRAC_FREQ
                    final_data2['GAINED_POINTS']=GAINED_POINTS
                    final_data2['CWP_SCORE']=round((final_data2['GAINED_POINTS']/(20*final_data2['WEEK_SINCE_FIRST_PRACTICE']))*100,0)*10
                    final_data2.loc[(final_data2['CWP_SCORE']>100),'CWP_SCORE'] = 100*10



                    # <<<<<<<<<<<<<<<<<<<<-------------------RECENT ENGAGEMENT SCORE------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>

                    final_data3=final_data2

                    user_master_df['SIGNUP_DATE']=pd.to_datetime(user_master_df['SIGNUP_DATE']).dt.date

                    final_data3=user_master_df[['USER_ID','SIGNUP_DATE']].merge(final_data3,how='inner',on='USER_ID').reset_index(drop=True)

                    _30_day_data=[]
                    points_30_day=[]

                    _60_day_data=[]
                    points_60_day=[]

                    _180_day_data=[]
                    points_180_day=[]

                    _365_day_data=[]
                    points_365_day=[]

                    CSY_data=[]
                    points_csy_day=[]

                    Lifetime=[]
                    points_Lifetime=[]


                    for i in range(len(final_data3)):
                        if (datetime.datetime.now().date()-final_data3['SIGNUP_DATE'][i]).days>=30:
                            dates30=list(pd.date_range(start=datetime.datetime.now().date()-timedelta(days=30),end=datetime.datetime.now().date(), freq=us_bd))
                            dates30=[j.date() for j in dates30]
                            _30_days=len(list(set(final_data3['DATES_OF_PRACTICING'][i]).intersection(dates30)))
                            if (_30_days>0) and (_30_days<len(dates30)/6):
                                points30=1
                            elif (_30_days==0):
                                points30=0
                            else:
                                points30=2
                        else:
                            _30_days='not eligible'
                            points30='not eligible'
                        _30_day_data.append(_30_days)
                        points_30_day.append(points30)



                    for i in range(len(final_data3)):
                        if (datetime.datetime.now().date()-final_data3['SIGNUP_DATE'][i]).days>=60:
                            dates60=list(pd.date_range(start=datetime.datetime.now().date()-timedelta(days=60),end=datetime.datetime.now().date(), freq=us_bd))
                            dates60=[j.date() for j in dates60]
                            _60_days=len(list(set(final_data3['DATES_OF_PRACTICING'][i]).intersection(dates60)))
                            if (_60_days>0) and (_60_days<len(dates60)/6):
                                points60=1
                            elif (_60_days==0):
                                points60=0
                            else:
                                points60=2
                        else:
                            _60_days='not eligible'
                            points60='not eligible'        
                        _60_day_data.append(_60_days)
                        points_60_day.append(points60)



                    for i in range(len(final_data3)):
                        if (datetime.datetime.now().date()-final_data3['SIGNUP_DATE'][i]).days>=180:
                            dates180=list(pd.date_range(start=datetime.datetime.now().date()-timedelta(days=180),end=datetime.datetime.now().date(), freq=us_bd))
                            dates180=[j.date() for j in dates180]
                            _180_days=len(list(set(final_data3['DATES_OF_PRACTICING'][i]).intersection(dates180)))
                            if (_180_days>0) and (_180_days<len(dates180)/6):
                                points180=1
                            elif (_180_days==0):
                                points180=0
                            else:
                                points180=2

                        else:
                            _180_days='not eligible'
                            points180='not eligible'

                        _180_day_data.append(_180_days)
                        points_180_day.append(points180)



                    for i in range(len(final_data3)):
                        if (datetime.datetime.now().date()-final_data3['SIGNUP_DATE'][i]).days>=365:
                            dates365=list(pd.date_range(start=datetime.datetime.now().date()-timedelta(days=365),end=datetime.datetime.now().date(), freq=us_bd))
                            dates365=[j.date() for j in dates365]
                            _365_days=len(list(set(final_data3['DATES_OF_PRACTICING'][i]).intersection(dates365)))
                            if (_365_days>0) and (_365_days<len(dates365)/6):
                                points365=1
                            elif (_365_days==0):
                                points365=0
                            else:
                                points365=2
                        else:
                            _365_days='not eligible'
                            points365='not eligible'

                        _365_day_data.append(_365_days)
                        points_365_day.append(points365)


                    for i in range(len(final_data3)):
                        dates_csy=list(pd.date_range(start=csy_first_date().date(),end=datetime.datetime.now().date(), freq=us_bd))
                        dates_csy=[j.date() for j in dates_csy]
                        csy_days=len(list(set(final_data3['DATES_OF_PRACTICING'][i]).intersection(dates_csy)))
                        if (csy_days>0) and (csy_days<len(dates_csy)/6):
                            points_csy=1
                        elif (csy_days==0):
                            points_csy=0
                        else:
                            points_csy=2
                        CSY_data.append(csy_days)
                        points_csy_day.append(points_csy)





                    for i in range(len(final_data3)):
                        dates_lifetime=list(pd.date_range(start=final_data3['SIGNUP_DATE'][i],end=datetime.datetime.now().date(), freq=us_bd))
                        dates_lifetime=[j.date() for j in dates_lifetime]
                        lifetime_days=len(list(set(final_data3['DATES_OF_PRACTICING'][i]).intersection(dates_lifetime)))
                        if (lifetime_days>0) and (lifetime_days<len(dates_lifetime)/6):
                            points_lifetime=1
                        elif (lifetime_days==0):
                            points_lifetime=0
                        else:
                            points_lifetime=2

                        Lifetime.append(lifetime_days)
                        points_Lifetime.append(points_lifetime)




                    mergedata=[]
                    for m,n,o,p,q,r in zip(points_30_day,points_60_day,points_180_day,points_365_day,points_csy_day,points_Lifetime):
                        mergedata.append([m,n,o,p,q,r])
#                     10 should be multiplied

                    final_data3['RE_SCORE']=''
                    for i in range(len(mergedata)):
                        xs=[s for s,val in enumerate(mergedata[i]) if val!='not eligible']
                        check=len(xs)
                        if check>0:
                            re_score=(sum([mergedata[i][q] for q in xs])/(2*check))*100
                        else:
                            re_score=0
                        final_data3['RE_SCORE'][i]=round(re_score,0)*10


                    # <<<<<<<<<<<<<<<<------------------------------ACTIVE USER SCORE------------------------>>>>>>>>>>>>>>>>>>>>>>>>>

                    days_since_signup=[]
                    for i in range(len(final_data3)):
                        d_snup=(datetime.datetime.now().date()-final_data3['SIGNUP_DATE'][i]).days
                        days_since_signup.append(d_snup)


                    ACTIVE_USER=[]
                    for i in range(len(days_since_signup)):
                        p_days=len(final_data3['DATES_OF_PRACTICING'][i])
                        if days_since_signup[i]>60:        
                            if p_days>=20:
                                active_user=1
                            else:
                                active_user=0
                        else:
                            if p_days>=round((days_since_signup[i]/60)*20,0):
                                active_user=1
                            else:
                                active_user=0

                        ACTIVE_USER.append(active_user)


                    final_data3['ACTIVE_USER']=ACTIVE_USER
#                     10 should be multiplied

                    ACTIVE_USER_SCORE_SCHOOL=round((len(final_data3[final_data3['ACTIVE_USER']>0])/len(user_master_df))*100,0)*10

                    USAGE_SCORE_SCHOOL=round(final_data3['USAGE_SCORE'].mean(),0)

                    CWP_SCORE_SCHOOL=round(final_data3['CWP_SCORE'].mean(),0)

                    RE_SCORE_SCHOOL=round(final_data3['RE_SCORE'].mean(),0)

                    E_SCORE_SCHOOL=round((ACTIVE_USER_SCORE_SCHOOL+USAGE_SCORE_SCHOOL+CWP_SCORE_SCHOOL+RE_SCORE_SCHOOL)/4,0)

                    if len(audio_track_master_df)>=5*len(user_master_df):

                        ACTIVE_SCHOOL=1
                    else:
                        ACTIVE_SCHOOL=0

                    score_output={
                        'SCHOOL_ID':trackid,
                        'SCHOOL_NAME':school_name,        
                        'ACTIVE_USER_SCORE_SCHOOL':ACTIVE_USER_SCORE_SCHOOL,
                                'USAGE_SCORE_SCHOOL':USAGE_SCORE_SCHOOL,
                                'CWP_SCORE_SCHOOL':CWP_SCORE_SCHOOL,
                                'RE_SCORE_SCHOOL':RE_SCORE_SCHOOL,
                                'E_SCORE_SCHOOL':E_SCORE_SCHOOL,
                                'ACTIVE_SCHOOL':ACTIVE_SCHOOL  


                                }

                    return score_output

                if len(list(db_live.district_master.find({'_id':ObjectId(str(trackid))})))>0:
                    district_id=trackid
                    districtinfo={
                        '5f2609807a1c0000950bb45a':'LAUSD',
                        '5f2609807a1c0000950bb45c':'Comox Valley School District'
                    }

                    if district_id in list(districtinfo):
                        district_name=districtinfo[district_id]

            #         if district_id=='5f2609807a1c0000950bb45a':
            #             district_name='LAUSD'
                    else:
                        districtname=list(db_live.district_master.find({'_id':ObjectId(district_id)}))
                        district_name=districtname[0].get('DISTRICT_NAME')

            #         districtname=list(db_live.district_master.find({'_id':ObjectId(district_id)}))

                    schoolids=db_live.user_master.distinct('schoolId._id',

                                                        {'schoolId._id':{'$in':db_live.school_master.distinct('_id',                                               
                                                        {'CATEGORY':{'$regex':district_name,'$options':'i'}})}
                                                        })
                    df_s=[]
                    for ii in range(len(schoolids)):
                        schls= escore_school_monthwise(str(schoolids[ii]))
                        df_s.append(schls)
                    schools_df=pd.DataFrame(df_s)

                    schools_df['SCORE_TYPE']=''

                    for i in range(len(schools_df)):
                        if schools_df['E_SCORE_SCHOOL'][i]<=250:
                            schools_df['SCORE_TYPE'][i]='0-250'
                        elif schools_df['E_SCORE_SCHOOL'][i]<=500:
                            schools_df['SCORE_TYPE'][i]='251-500'
                        elif schools_df['E_SCORE_SCHOOL'][i]<=750:
                            schools_df['SCORE_TYPE'][i]='501-750'
                        else:
                            schools_df['SCORE_TYPE'][i]='751-100'


            #         file_name = str(trackid)+'_school_e_scores.csv'

            #         if(os.path.exists(file_name) and os.path.isfile(file_name)):
            #             os.remove(file_name)

            #         schools_df.to_csv(str(trackid)+'_school_e_scores.csv',index=False)



            #         new_schools_df=schools_df.groupby('SCORE_TYPE')['SCHOOL_ID'].count().reset_index().rename(columns={'SCHOOL_ID':'School_Count'})

            #         score_type=pd.DataFrame({'SCORE_TYPE':[
            #             '0-25','26-50','51-75','76-100'
            #         ]})




            #         new_schools_df1=score_type.merge(new_schools_df,how='left',on='SCORE_TYPE').fillna(0)

#                     10 should be multiplied
                    ACTIVE_SCHOOL_SCORE=round(sum(schools_df['ACTIVE_SCHOOL'])/len(set(schoolids))*100,0)*10
                    E_SCORE=round((schools_df['ACTIVE_USER_SCORE_SCHOOL'].mean()+schools_df['USAGE_SCORE_SCHOOL'].mean()+schools_df['CWP_SCORE_SCHOOL'].mean()+schools_df['RE_SCORE_SCHOOL'].mean()+ACTIVE_SCHOOL_SCORE)/5)

                    temp={
                        'DISTRICT_ID':str(trackid),
                        'TIME_PERIOD':dateinlist.strftime('%b-%Y'),            
                        'ACTIVE_USER_SCORE':round(schools_df['ACTIVE_USER_SCORE_SCHOOL'].mean(),0),
                        'USAGE_SCORE':round(schools_df['USAGE_SCORE_SCHOOL'].mean(),0),
                        'CWP_SCORE':round(schools_df['CWP_SCORE_SCHOOL'].mean(),0),
                        'RE_SCORE':round(schools_df['RE_SCORE_SCHOOL'].mean(),0),
                        'ACTIVE_SCHOOL_SCORE':ACTIVE_SCHOOL_SCORE,
                        'E_SCORE':E_SCORE,

                                        }




                    return temp
            #         return new_schools_df1

                else:
                    df_single_s=[]        
                    schls= escore_school_monthwise(trackid)
                    df_single_s.append(schls)
                    schools_df=pd.DataFrame(df_single_s)
                    temp={'ACTIVE_USER_SCORE':schools_df['ACTIVE_USER_SCORE_SCHOOL'][0],
                        'USAGE_SCORE':schools_df['USAGE_SCORE_SCHOOL'][0],
                        'CWP_SCORE':schools_df['CWP_SCORE_SCHOOL'][0],
                        'RE_SCORE':schools_df['RE_SCORE_SCHOOL'][0],
                        'E_SCORE':schools_df['E_SCORE_SCHOOL'][0]
                        }


                return json.dumps(temp)




            lis=pd.date_range(str(csy_first_date().date()),str(datetime.datetime.now().date()), 
                    freq='MS').strftime("%Y-%m-%d").tolist()
            month_df=pd.DataFrame({'MONTH':
                                pd.date_range(str(csy_first_date().date()),str(csy_first_date().date()+relativedelta(years=1)-relativedelta(days=1)), 
                                                freq='MS').strftime("%b").tolist()})
            lis=[dateutil.parser.parse(i)+relativedelta(months=1)-relativedelta(days=1) for i in lis ]

            #code for monthwise E-Score 

            file_name = str(trackid)+'_monthwise_e_score.csv'
            if(os.path.exists(file_name) and os.path.isfile(file_name)):
                district_e_score=pd.read_csv(str(trackid)+"_monthwise_e_score.csv",sep=',')
                district_e_score_snap_dic=district_e_score.to_dict('records')

                if district_e_score['TIME_PERIOD'][len(district_e_score)-1]==datetime.datetime.now().date().strftime('%b-%Y'):            
                    val=escore_mothwise(trackid,lis[len(district_e_score)-1])
                    district_e_score_snap_dic[len(district_e_score_snap_dic)-1]=val
                    district_e_score_snap_dic_df=pd.DataFrame(district_e_score_snap_dic)        
                    district_e_score_snap_dic_df.to_csv(str(trackid)+"_monthwise_e_score.csv",index=False)
            #         district_e_score_snap=pd.read_csv(str(trackid)+"_monthwise_e_score.csv",sep=',')
            #         temps={'MONTH':district_e_score_snap['TIME_PERIOD'].tolist(),'E_SCORES':district_e_score_snap['E_SCORE'].tolist()}
            #         return json.dumps(temps)
                else:
                    val=escore_mothwise(trackid,datetime.datetime.now())
                    district_e_score_snap_dic.append(val)            
                    district_e_score_snap_dic_df=pd.DataFrame(district_e_score_snap_dic)        
                    district_e_score_snap_dic_df.to_csv(str(trackid)+"_monthwise_e_score.csv",index=False)
            #         district_e_score_snap=pd.read_csv(str(trackid)+"_monthwise_e_score.csv",sep=',')
            #         temps={'MONTH':district_e_score_snap['TIME_PERIOD'].tolist(),'E_SCORES':district_e_score_snap['E_SCORE'].tolist()}
            #         return json.dumps(temps)    

            else:
                val_=[]
                for i in range(len(lis)):
                    val=escore_mothwise(trackid,lis[i])
                    val_.append(val)
                escoredf=pd.DataFrame(val_)
                escoredf.to_csv(str(trackid)+"_monthwise_e_score.csv",index=False)
            #     district_e_score_snap=pd.read_csv(str(trackid)+"_monthwise_e_score.csv",sep=',')
            #     temps={'MONTH':district_e_score_snap['TIME_PERIOD'].tolist(),'E_SCORES':district_e_score_snap['E_SCORE'].tolist()}
            #     return json.dumps(temps)
        
    #<<<<<<<<<<<<<<<<<<<----------monthwise escore code ends here--------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            
            return json.dumps({'Status':'1','published':'Yes'})
            
        else:
            df_single_s=[]        
            schls= escore_school_downloads(trackid)
            df_single_s.append(schls)
            schools_df=pd.DataFrame(df_single_s)
            temp={'ACTIVE_USER_SCORE':schools_df['ACTIVE_USER_SCORE_SCHOOL'][0],
                'USAGE_SCORE':schools_df['USAGE_SCORE_SCHOOL'][0],
                'CWP_SCORE':schools_df['CWP_SCORE_SCHOOL'][0],
                'RE_SCORE':schools_df['RE_SCORE_SCHOOL'][0],
                'E_SCORE':schools_df['E_SCORE_SCHOOL'][0]
                }
            
            
        return json.dumps(temp)

    districtlist=[
        '6045e4d007ead7744b125848', 
        '616d2865c35ee7525fb145d9',
        '6167fe41282c502e1077c12f',
        '6045e4d707ead7744b125854',            
        '5f2609807a1c0000950bb475',
        '5f2609807a1c0000950bb481',
        '5f2609807a1c0000950bb47a',
        '5f2609807a1c0000950bb47b',
        '6045e4c907ead7744b12583d',
        '619268dd81f00a4319a65a52',
        '789',
        '6045e4d707ead7744b125855',
        '5f2609807a1c0000950bb463',
        '5f59e4836451a9089d7d4007',
        '6045e4d107ead7744b125849',
        '5fe2e25d4d0ca68d7baf889d',
        '6045e4ca07ead7744b12583e',
        '6045e4d107ead7744b12584a',
        '6045e4c807ead7744b12583b',
        '6023a6d79e8e623753fc305c',
        '60f7bf747cc8db72d772e465',
        '5f2609807a1c0000950bb46d',
        '617949a0fc72b63e0d1dc7d3',
        '6045e4ca07ead7744b12583f',
        '60473f8823e88e242074ebd2',
        '6045e4d907ead7744b125858',
        '5f2609807a1c0000950bb46c',
        '5ffd8176469a86e28635f512',
        '5f2609807a1c0000950bb460',
        '6045e4d907ead7744b125857',
        '5f2609807a1c0000950bb47f',
        '5f2609807a1c0000950bb45c',
        '5f2609807a1c0000950bb480',
        '6045e4da07ead7744b125859',
        '6045e4cb07ead7744b125840',
        '5f2609807a1c0000950bb46e',
        '5f7413ef9387fd71ce6387cb',
        '6045e4c707ead7744b12583a',
        '5f895191609e08b76029f641',
        '5f2609807a1c0000950bb462',
        '5f2609807a1c0000950bb461',
        '5f2609807a1c0000950bb464',
        '6045e4cc07ead7744b125841',
        '5f2609807a1c0000950bb45e',
        '6045e4cd07ead7744b125843',
        '6045e4da07ead7744b12585a',
        '5f2609807a1c0000950bb47d',
        '6023a7269e8e623753fc305e',
        '5f2609807a1c0000950bb46b',
        '617fae53ccd2dd76541ed5e7',
        '6045e4d207ead7744b12584b',
        '5f2609807a1c0000950bb450',
        '6045e4cd07ead7744b125844',
        '5f2609807a1c0000950bb474',
        '5f2609807a1c0000950bb45f',
        '60cb8971c5b0e89ed7ac0aa1',
        '5f9aa5e526edbed399d56c92',
        '6045e4c707ead7744b125839',
        '5f2609807a1c0000950bb47c',
        '6045e4ce07ead7744b125845',
        '61af3b75870dba387bcd86cd',
        '61aa08a4afeab44256f54074',
        '6045e4db07ead7744b12585b',
        '5f2609807a1c0000950bb476',
        '6045e4db07ead7744b12585c',
        '6045e4cc07ead7744b125842',
        '60b872ce826cab06ebdf044e',
        '6045e4dc07ead7744b12585d',
        '6045e4d307ead7744b12584d',
        '5f2609807a1c0000950bb455',
        '5f2609807a1c0000950bb47e',
        '6045e4cf07ead7744b125846',
        '5f2609807a1c0000950bb45a',
        '5f2609807a1c0000950bb467',
        '6045e4dc07ead7744b12585e',
        '5fe2e1ee4d0ca68d7baf889c',
        '6023a7499e8e623753fc305f',
        '5f2609807a1c0000950bb482',
        '6077e1b5eaa8bae0e2e04a64',
        '6023a7019e8e623753fc305d',
        '5f2609807a1c0000950bb465',
        '6045e4d407ead7744b12584f',
        '6045e4d307ead7744b12584e',
        '610d0837931db8cfdf500fef',
        '5fb4efce4139b9d4c5a86a69',
        '6045e4cf07ead7744b125847',
        '5fbcdf0ba84e48a64412a798',
        '5f2609807a1c0000950bb459',
        '6045e4c907ead7744b12583c',
        '5f7c01fa9387fd71ce6387cc',
        '5fd704da04a848e368de5dc6',
        '5f6994386451a9089d7d4009',
        '5f2609807a1c0000950bb472',
        '6017ab3043ca9c39151838d4',
        '6045e4dd07ead7744b12585f',
        '60913aaea5fd4b56a4bafa70',
        '5f2609807a1c0000950bb479',
        '5f2609807a1c0000950bb46f',
        '5f8fcd33609e08b76029f644',
        '6045e4de07ead7744b125860',
        '6177e72d108b6ebefcfc1014',
        '5f2609807a1c0000950bb466',
        '5f2609807a1c0000950bb471',
        '6045e4d507ead7744b125850',
        '5f6d7cbce6452eb06384db20',
        '5f2609807a1c0000950bb478',
        '6045e4d507ead7744b125851',
        '6023a76f9e8e623753fc3060',
        '5f2609807a1c0000950bb470',
        '6045e4df07ead7744b125862',
        '6045e4df07ead7744b125863',
        '5f2609807a1c0000950bb477',
        '602e60e567d3e6c0a4eb4d99',
        '6045e4d807ead7744b125856',
        '6045e4de07ead7744b125861',
        '5f2609807a1c0000950bb473',
        '617fc552ccd2dd76541ed5eb',
        '123',
        '6045e4e007ead7744b125864',
        '60eea965ae7de54f57abf234',
        '5f2609807a1c0000950bb46a',
        '5f2609807a1c0000950bb46a',
        '6045e4e007ead7744b125865',
        '6045e4e107ead7744b125866',
        '60a7b03831afdba383052726',
        '6045e4d607ead7744b125852',
        '5f2609807a1c0000950bb468',
        '456',
        '6023a7949e8e623753fc3061',
        '6045e4e207ead7744b125867',
        '5f698b826451a9089d7d4008',
        '6045e4d607ead7744b125853',
        '5f2609807a1c0000950bb45b',
        '6045e4e207ead7744b125868',
        '6045e4d207ead7744b12584c',
        '5f2609807a1c0000950bb368',
        '5f2609807a1c0000950bb45d']



    for i in range(len(districtlist)):
        
        try:
            escore_overall_downloads(districtlist[i])
        except:
            pass


    return json.dumps({'Status':'1','Published':'Yes'})

if __name__=='__main__':
    
    app.run(host='172.31.58.47',port=5002)
