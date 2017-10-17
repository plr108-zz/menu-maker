import sys
from flask import Flask
from flask import render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


app = Flask(__name__)
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurants/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(
        Restaurants=[restaurant.serialize for restaurant in restaurants])


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    try:
        restaurantToEdit = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
    except:
        response = 'Restaurant not found'
        print sys.exc_info()[0]
        return response
    else:
        if request.method == 'POST':
            if request.form['name']:
                restaurantToEdit.name = request.form['name']
                return redirect(url_for('showRestaurants'))
        else:
            return render_template(
                'editrestaurant.html', restaurant=restaurantToEdit)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    try:
        restaurantToDelete = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
    except:
        response = 'Restaurant not found'
        print sys.exc_info()[0]
        return response
    else:
        if request.method == 'POST':
            session.delete(restaurantToDelete)
            session.commit()
            return redirect(
                url_for('showRestaurants', restaurant_id=restaurant_id))
        else:
            return render_template(
                'deleterestaurant.html', restaurant=restaurantToDelete)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    try:
        restaurant = session.query(
            Restaurant).filter_by(id=restaurant_id).one()
        items = session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id).all()
    except:
        response = 'Restaurant not found'
        print sys.exc_info()[0]
        return response
    else:
        return render_template(
            'menu.html', restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/new/',
           methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'],
                           description=request.form['description'],
                           price=request.form['price'],
                           course=request.form['course'],
                           restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id,
                               item=editedItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deleteMenuItem.html',
                               restaurant_id=restaurant_id,
                               item=itemToDelete)


def get_menu_item(menu_id):
    target_item = None
    for item in items:
        if int(item['id']) == menu_id:
            target_item = item
    return target_item


def getRestaurant(restaurant_id):
    targetRestaurant = None
    for restaurant in restaurants:
        if int(restaurant['id']) == restaurant_id:
            targetRestaurant = restaurant
    return targetRestaurant


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
