from flask import Flask, render_template, request
from wtforms import Form
from flask_wtf import FlaskForm

import psycopg2

import Facade
from Hotel import Hotel
from Reservation import Reservation

conn = Facade.get_connection()

app = Flask(__name__)

@app.route("/")
def home():
    #revois du html avec des valeur réel
    return render_template('index.html', name=Facade.get_name())

@app.route("/hotels")
def hotels():
    return render_template('hotels.html', hotel_list=Hotel.get_hotels(conn))

@app.route("/reservations")
def reservations():
    return render_template('reservations.html', hotel_list=Reservation.find_room(conn))

@app.route("/find_room", methods=['GET', 'POST'])
def find_room():
    pass
    # help : request.args.get('email') returns the email field value of the web form
    #room_number = Reservation.find_room(...)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
