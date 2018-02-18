
from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required, length
import requests 
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

weather_api_key = '5c418d2154f4ae76a9185ddf947e8b14'

@app.route('/')
def hello_world():
    return 'Hello World!'

class zipcode(FlaskForm):
	zip_code = StringField("Enter any US zip code:", validators = [ Required(), length(min = 5, max=5)])
	submit = SubmitField('Submit')

@app.route('/zipcode')
def zip_form():
	form = zipcode()
	return render_template('zipform.html', form = form)

@app.route('/zipcode_result', methods = ['POST', 'GET'])
def zip_result():
	form = zipcode()
	if form.validate_on_submit():
		baseurl = 'http://api.openweathermap.org/data/2.5/weather?id=524901&APPID=' + weather_api_key
		z = form.zip_code.data
		zipcode_param_dict = {}
		zipcode_param_dict["zip"] = z
		response = requests.get(baseurl, params=zipcode_param_dict)
		text = response.text
		text_json = json.loads(text)
		file_name = 'weather.txt'
		file = open(file_name, 'w')
		file.write(text) 
		file.close()
		zip_name = text_json['name']
		weather_description = text_json['weather'][0]['description']
		tempreture = text_json['main']['temp']
	return redirect('/zipcode')



if __name__ == "__main__":
    app.run(use_reloader=True,debug=True)