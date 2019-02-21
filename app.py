from flask import Flask, render_template, request, make_response, url_for, abort 
import os
import json 
import requests 
from pprint import pprint

app = Flask(__name__)

#loading the json file into data object 
data = {}
with open('data.json') as f: 
	data = json.load(f) #loads the json file into python object 
pprint(data)

#path for API 
def _url(path):
    return 'https://hunter-todo-api.herokuapp.com/' + path

#index.html 
@app.route('/') 
def index():
    return render_template('index.html') 

#register.html 
@app.route("/register")
def register():
    return render_template('register.html')

#login.html
@app.route("/login")
def login():
    return render_template('login.html')


#create new user 
@app.route("/login/post", methods=['POST'])
def new_User():
    new_User = request.form['new_User']
    if (new_User == ""):
        return make_response("Please try again. Enter a user "'<a href="/login">Home</a>')
    requests.post(_url('user'), json={'username': new_User})
    r = make_response("Login has been successful! " '<a href="/login">Home</a>')
    return r 

#Authentication 
@app.route("/auth", methods=['POST'])
def authenticate_User():
    authenticate_User = request.form['authenticate_User']
    if (authenticate_User == ""):
        return make_response("Please try again. Enter a user"'<a href="/login">Home</a>')
    r = requests.post(_url('auth'), json={'username': authenticate_User})
    json_data = r.json()
    try:
        token = json_data['token']
    except:
        token = ""
    if (token == ""):
        return make_response("Error Username was not found. Try again. "'<a href="/">Home</a>')
    redirect_to_root = redirect('/')
    r = make_response("Login has been successful!" '<a href="/">Home</a>')
    r.set_cookie('sillyauth', value=token)
    return r

#submitting new item
@app.route("/new_item", methods=['POST'])
def new_item():
    cookies = request.cookies
    new_item = request.form['new_item']
    if (new_item == ""):
        return make_response("Input was not found. Try Again ")
    requests.post(
        _url('todo-item'), cookies=cookies, json={'content': new_item})
    return make_response("Creating a new item was successfull! " '<a href="/login">Home</a>')


#seeing all items of user 
@app.route("/all_items")
def all_items():
    cookies = request.cookies
    r = requests.get(_url('todo-item'), cookies=cookies)
    return r.text


#Changing data on an item 
@app.route("/change_item", methods=['POST'])
def change_item():
    cookies = request.cookies
    itemID = request.form['itemID']
    new_item = request.form['new_item']
    if (itemID == "" or newItem == ""):
        return make_response("Input was not found. Try Again"
                             '<a href="/">Home</a>')
    data = '{"content": "' + new_item + '"}'
    requests.put(_url('todo-item/') + itemID, cookies=cookies, data=data)
    return make_response("Changing item was successfull! " '<a href="/login">Home</a>')

#delete item 
@app.route("/delete_item", methods=['POST'])
def delete_item():
    cookies = request.cookies
    itemID = request.form['itemID']
    if (itemID == ""):
        return make_response("Empty input:please try again. "
                             '<a href="/">Home</a>')
    requests.delete(_url('todo-item/') + itemID, cookies=cookies)
    return make_response("Item successfully deleted. " '<a href="/">Home</a>')

@app.route('/delete/<id>')
def deleteitem(id):
	response = requests.delete('https://hunter-todo-api.herokuapp.com/todo-item/'+id, cookies=cookies)
	return redirect(url_for('todolist'))

#slashing the item 
@app.route("/complete_item", methods=['POST'])
def complete_item():
    cookies = request.cookies
    itemID = request.form['itemID']
    if (itemID == ""):
        return make_response("Empty input:please try again. "
                             '<a href="/">Home</a>')
    requests.put(
        _url('todo-item/') + itemID, cookies=cookies, json={'completed': True})
    return make_response("Item is completed! "
                         '<a href="/">Home</a>')
@app.route("/logout")
def logout():
    r = make_response("Logout has been successful. "
                        '<a href="/">Home</a>')
    r.set_cookie('sillyauth', expires=0)
    return r

#running on host 
if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host="0.0.0.0", port=port, threaded=True, debug=True)