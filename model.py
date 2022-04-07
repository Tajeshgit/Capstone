import pandas as pd
import numpy as np
import pickle
import warnings
warnings.filterwarnings("ignore")
from flask import Flask, render_template



def top5(user_input):
    
    # loading the clean data 
    #df_file = pd.read_csv("updated_sample30.csv") 
    df_file = pd.read_csv("dataset/updated_sample30.csv") 
    # loading the word vectorizer
    vectorizer  = pickle.load(open("pickle/vector.pkl","rb")) 

    #load the user recommendation matrix
    rec_model = pickle.load(open('pickle/recommendation_model.pkl', 'rb')) 

    
    #get top 20 products for the user
    
    try:

        top_20 = rec_model.loc[user_input].sort_values(ascending=False)[0:20]

        #merge the top20 products with original DF
        df1 = pd.merge(top_20,df_file,left_on='name',right_on='name',how = 'left') 
    
        #load the sentiment classification model
        sent_model = pickle.load(open("pickle/sentiment_model_LR.pkl", "rb")) 
    
        # to get the sentiment select review from merged DF as X
        X=df1['reviews'] 

        #use word vectorizer to transform X
        X_trans = vectorizer.transform(X.tolist())

        #get the prediction 
        prediction = sent_model.predict(X_trans)

        #add the predicction to merge DF  
        df1['sent_predicated'] = prediction
        #get the overall sentiment for each product 
        df3 = df1.groupby('name').sent_predicated.mean() 
        # merge the overall sentiment predicted by user to top 20 data and sort by sentiment 
        df4= (pd.merge(top_20,df3,left_on='name',right_on='name',how = 'left').sort_values(by='sent_predicated',ascending=False))
        #convert the sentiment into percentage
        df4['sent_predicated'] = round(df4['sent_predicated']*100,2) 
        #convert into dataframe and select top 5 based on overall product sentiment percentage 
        df5 = pd.DataFrame(df4[:5]).reset_index()
        #select only product name from above DF and rename
        df6 = pd.DataFrame(df5['name']) 
        df6 = df6.rename(columns={"name": "Product Name"})

    
        return  df6

    except KeyError:
        message = 'User ' + user_input + ' Does not exist!!'
        msg_list = [message]
        df6 = pd.DataFrame(msg_list,columns=['message'])
        return df6

        


