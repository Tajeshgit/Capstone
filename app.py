# This is basically the heart of my flask 

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import model


app = Flask(__name__)  # intitialize the flaks app  # common 


@app.route('/', methods=['GET', 'POST'])
def home():
    """ Session control"""
    return render_template('index.html')


@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    if request.method == 'GET':
        return render_template('index.html')  
    else:
        user_input = request.form['username']  
        df6 = model.top5(user_input)

        return  render_template('view.html',tables=[df6.to_html(classes='recommendation')], titles = ['Top 5 Recommendations for User'])



# Any HTML template in Flask App render_template

if __name__ == '__main__' :
    app.run(debug=True )  # this command will enable the run of your flask app or api
    
    #,host="0.0.0.0")