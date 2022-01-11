from flask import Flask,render_template,request,redirect,url_for,flash,abort,session,jsonify
from flask_bootstrap import Bootstrap
import json
import os.path

app = Flask(__name__) 
app.secret_key='akbradabra' 
bootstarp=Bootstrap(app)
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500
@app.route('/')
def hello():
    return render_template('index.html',codes=session.keys())

@app.route('/your-url',methods=['POST','GET'])
def your_url():
    if request.method=='POST':
        urls={}
        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls=json.load(urls_file)
        if request.form['code'] in urls.keys():
            flash("That short name has already been taken. Please use another name")
            return redirect(url_for('hello')) 
        urls[request.form['code']]={'url':request.form['url']}
        with open('urls.json','w') as url_file:
            json.dump(urls,url_file)
            session[request.form['code']]=True

        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('hello'))
        
@app.route('/<string:userenter>')   
def redirect_to_url(userenter):
    urls={}
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls=json.load(urls_file)
            
        if userenter in urls.keys():
            if 'url' in urls[userenter].keys():
                return redirect(urls[userenter]['url'])
    return abort (404)

@app.route('/api')
def session_api():
   return  jsonify(list(session.keys()))
    


#app.run()