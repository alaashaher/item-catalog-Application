import random
import string
import httplib2
import json
import requests
from flask import Flask, flash
from flask import render_template, request
from flask import jsonify, redirect
from flask import url_for
from flask import session as lhe_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from DataBase import Item
from DataBase_operation import database_operations
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response

app = Flask(__name__)

db = database_operations()

id_Client = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


@app.route('/catalog_page/JSON/')
def catalog_pageJSON():
    categories = db.GetAllCategoryBy()
    return jsonify(categories=[cat.serialize for cat in categories])


@app.route('/catalog_page/<int:category_id>/items/JSON/')
def itemsJSON(category_id):
    items = db.GetItemBy(category_id)
    return jsonify(items=[item.serialize for item in items])


# connect google+ to login

@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != lhe_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != id_Client:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = lhe_session.get('access_token')
    stored_gplus_id = lhe_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
    lhe_session['access_token'] = credentials.access_token
    lhe_session['gplus_id'] = gplus_id
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    lhe_session['userName'] = data['name']
    lhe_session['img_user'] = data['picture']
    lhe_session['email'] = data['email']
    lhe_session['user_id'] = db.GetUserBy(lhe_session).id
    show_output = ''
    show_output += '<br/>'
    show_output += '<h1>Welcome, '
    show_output += lhe_session['userName']
    show_output += '!</h1>'
    show_output += '<img src="'
    show_output += lhe_session['img_user']
    show_output += ' " class="user_img" >'
    show_output += '<br/>'
    return show_output


@app.route('/login')
def showLogin():
    categories = db.GetAllCategoryBy()
    latestItems = db.Get_last_item()
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    lhe_session['state'] = state
    # return "The current session state is %s" % lhe_session['state']
    return render_template('login.html',
                           STATE=state,
                           categories=categories,
                           items=latestItems)


@app.route('/')
@app.route('/catalog_page')
def show_items_for_category():
    if 'userName' not in lhe_session:
        return redirect(url_for('showLogin'))
    else:
        categories = db.GetAllCategoryBy()
        latestItems = db.Get_last_item()
        return render_template('categoires.html',
                               categories=categories,
                               items=latestItems,
                               user_id=lhe_session['user_id'])


@app.route('/catalog_page/<int:cat_id>/')
def show_items_for_category_with_id(cat_id):
    categories = db.GetAllCategoryBy()
    cat = db.GetCategoryBy(cat_id)
    items = db.GetItemBy(cat_id)
    return render_template('catogray.html',
                           myCategory=cat,
                           categories=categories,
                           items=items,
                           user_id=lhe_session['user_id'])


@app.route('/catalog/<int:cat_id>/item/<int:item_id>/')
def showItem(cat_id, item_id):
    cat = db.GetCategoryBy(cat_id)
    i = db.GetOneItemBy(item_id)
    return render_template('itemShow.html',
                           myCategory=cat,
                           myItem=i,
                           user_id=lhe_session['user_id'])


@app.route('/catalog_page/<int:cat_id>/addItem', methods=['GET', 'POST'])
def addItemCat(cat_id):
    if 'userName' not in lhe_session:
        return redirect(url_for('show_items_for_category'))
    else:
        cat = db.GetCategoryBy(cat_id)
        if request.method == 'POST':
            new_item = Item(name=request.form['name'],
                            description=request.form['description'],
                            cat_id=cat.id,
                            user_id=lhe_session['user_id'])
            db.addDatabase(new_item)
            return redirect(url_for('show_items_for_category', cat_id=cat.id))

        else:
            return render_template('addItem.html',
                                   cat=cat)


@app.route('/catalog_page/<int:cat_id>/edit/<int:item_id>/',
           methods=['GET', 'POST'])
def editItem(cat_id, item_id):
    if 'userName' not in lhe_session:
        return redirect(url_for('login'))
    else:
        categories = db.GetAllCategoryBy()
        item = db.GetOneItemBy(item_id)
        if request.method == 'POST':
            if lhe_session['user_id'] != int(request.form['ID']):
                return make_response('Invalid authorization paramaters.', 401)
            if request.form['name']:
                item.name = request.form['name']
            if request.form['description']:
                item.description = request.form['description']
            if request.form['Catalog_page']:
                item.cat_id = request.form['Catalog_page']
            db.addDatabase(item)
            return redirect(url_for('show_items_for_category_with_id',
                                    cat_id=item.cat_id,
                                    item_id=item.id))
        else:
            return render_template('edite_item.html',
                                   categories=categories,
                                   item=item)


@app.route('/catalog/<int:cat_id>/delete/<int:item_id>/',
           methods=['GET', 'POST'])
def deleteItem(cat_id, item_id):
    if 'userName' not in lhe_session:
        return redirect(url_for('show_items_for_category'))
    else:
        categories = db.GetAllCategoryBy()
        item = db.GetOneItemBy(item_id)
        if request.method == 'POST':
            if lhe_session['user_id'] != int(request.form['ID']):
                return make_response('Invalid authorization paramaters.', 401)
            db.deleteDatabase(item)
            return redirect(url_for('show_items_for_category'))
        else:
            return render_template('delete_item.html',
                                   categories=categories,
                                   item=item)


# disconnect google+ to login

@app.route('/gdisconnect')
def gdisconnect():
    access_token = lhe_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print lhe_session['userName']
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % lhe_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del lhe_session['access_token']
        del lhe_session['gplus_id']
        del lhe_session['userName']
        del lhe_session['email']
        del lhe_session['img_user']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/login')
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
