from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key_here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///restaurant.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgres://'):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace('postgres://', 'postgresql://', 1)

db = SQLAlchemy(app)

# Models
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default="Hexa Restaurant")
    tables = db.relationship('Table', backref='restaurant', lazy=True)

class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    reservations = db.relationship('Reservation', backref='table', lazy=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    party_size = db.Column(db.Integer, nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reserve', methods=['GET', 'POST'])
def reserve():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        party_size = int(request.form.get('party_size'))
        
        # Convert string to datetime
        reservation_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        reservation_time = datetime.strptime(time_str, '%H:%M').time()
        
        # Check if the date is not in the past
        if reservation_date < date.today():
            flash('Please select a future date for your reservation.', 'error')
            return redirect(url_for('reserve'))
        
        # Find available table
        available_tables = Table.query.filter(
            Table.capacity >= party_size
        ).all()
        
        if available_tables:
            # Create reservation
            reservation = Reservation(
                customer_name=name,
                customer_email=email,
                date=reservation_date,
                time=reservation_time,
                party_size=party_size,
                table_id=available_tables[0].id
            )
            db.session.add(reservation)
            db.session.commit()
            flash('Your reservation at Hexa Restaurant has been confirmed!', 'success')
            return redirect(url_for('index'))
        
        flash('Sorry, no tables are available for that party size at the selected time.', 'error')
        return redirect(url_for('reserve'))
    
    return render_template('reserve.html', today=date.today().strftime('%Y-%m-%d'))

@app.route('/reservations')
def reservations():
    reservations = Reservation.query.order_by(Reservation.date, Reservation.time).all()
    return render_template('reservations.html', reservations=reservations)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
