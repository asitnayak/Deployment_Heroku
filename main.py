from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

app=Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/review')
def review():
    try:
        p_name=request.args.get('p_name').replace(' ','')
        flipkart_url = "https://www.flipkart.com/search?q=" + p_name
        response = urlopen(flipkart_url)
        flipkart_page = response.read()
        response.close()
        flipkart_html = bs(flipkart_page , "html.parser")
        bigboxes = flipkart_html.findAll('div' , class_='_1AtVbE col-12-12')
        del bigboxes[0:3]
        box = bigboxes[0]
        p_link = "https://www.flipkart.com" + box.div.div.div.a['href']
        p_response = requests.get(p_link)
        #prodRes.encoding = 'utf-8'
        p_html = bs(p_response.text , 'html.parser')

        data = p_html.findAll('div', class_='_16PBlm')
        reviews=[]
        for d in data:
            doctor={}
            try:
                name = d.find('p', class_='_2sc7ZR _2V5EHH').text
            except:
                name='Verified Buyer'

            try:
                rating = d.find('div', class_='_3LWZlK _1BLPMq').text
            except:
                rating = 'Unrated'

            try:
                heading = d.find('p', class_='_2-N8zT').text
            except:
                heading='No heading'

            try:
                comment = d.find('div', class_='t-ZTKy').div.div.text
            except:
                comment='No comments'

            doctor['name']=name
            doctor['rating'] = rating
            doctor['heading'] = heading
            doctor['comment'] = comment
            doctor['p_name']=p_name

            reviews.append(doctor)
    except Exception as e:
        print('The exception message is : ',e)
        return 'Something went wrong'


    return render_template('result.html' , reviews=reviews[:len(reviews)-1])




if __name__ == "__main__" :
    app.run(debug=True)