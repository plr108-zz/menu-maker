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


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
