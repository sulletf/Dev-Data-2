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
    return render_template('index.html', name=Facade.get_name())

@app.route("/hotels")
def hotels():
    return render_template('hotels.html', hotel_list=Hotel.get_hotels(conn))

@app.route("/reservations")
def reservations():
    return render_template('reservations.html', hotel_list=Hotel.get_hotels(conn))

@app.route("/find_room", methods=['GET', 'POST'])
def find_room():
    # help : request.args.get('email') returns the email field value of the web form
    hotel_id = request.args.get('hotel_id')
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')
    num_persons = request.args.get('num_persons')
    email = request.args.get('email')

    room_number = Reservation.find_room(conn, hotel_id, check_in, num_persons)

    if room_number is None:
      return render_template('room_notfound.html', check_in=check_in)
    else:
      resa = Reservation(email, hotel_id, room_number, check_in, check_out, num_persons)
      resa.load(conn)
      conn.commit()
      return render_template('room_found.html', check_in=check_in, check_out=check_out, email=email)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
