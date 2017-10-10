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
    response = 'This page will show all my restaurants'
    return response


@app.route('/restaurants/new/')
def newRestaurant():
    response = 'This page will be for making a new restaurant'
    return response


@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    response = 'This page will be for editing restaurant %s' % restaurant_id
    return response


@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    response = 'This page will be for deleting restaurant %s' % restaurant_id
    return response


@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    response = 'This page is the menu for restaurant %s' % restaurant_id
    return response


@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
    response = 'This page is for making a new menu item for restaurant '
    response += '%s' % restaurant_id
    return response


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    response = 'This page is for editing menu item %s ' % menu_id
    response += ' for restaurant %s' % restaurant_id
    return response


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
