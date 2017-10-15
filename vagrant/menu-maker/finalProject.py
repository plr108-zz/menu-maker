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


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    restaurantToEdit = getRestaurant(restaurant_id)
    response = 'Restaurant not found'
    if restaurantToEdit is None:
        return response
    else:
        return render_template(
            'editrestaurant.html', restaurant=restaurantToEdit)


@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    restaurantToDelete = getRestaurant(restaurant_id)
    response = 'Restaurant not found'
    if restaurantToDelete is None:
        return response
    else:
        return render_template(
            'deleterestaurant.html', restaurant=restaurantToDelete)


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    targetRestaurant = getRestaurant(restaurant_id)
    response = 'Restaurant not found'
    if targetRestaurant is None:
        return response
    else:
        return render_template(
            'menu.html', restaurant=targetRestaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
    targetRestaurant = getRestaurant(restaurant_id)
    response = 'Restaurant not found'
    if targetRestaurant is None:
        return response
    else:
        return render_template(
            'newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    target_restaurant = getRestaurant(restaurant_id)
    no_restaurant = 'Restaurant not found'
    if target_restaurant is None:
        return no_restaurant
    else:
        target_item = get_menu_item(menu_id)
        no_menu_item = 'Menu Item not found'
        if target_item is None:
            return no_menu_item
        else:
            return render_template('editmenuitem.html',
                                   restaurant_id=restaurant_id,
                                   menu_id=menu_id,
                                   item=target_item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    target_restaurant = getRestaurant(restaurant_id)
    no_restaurant = 'Restaurant not found'
    if target_restaurant is None:
        return no_restaurant
    else:
        target_item = get_menu_item(menu_id)
        no_menu_item = 'Menu Item not found'
        if target_item is None:
            return no_menu_item
        else:
            return render_template('deletemenuitem.html', item=target_item)


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
