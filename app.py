from flask import Flask, session, render_template, request, jsonify, url_for, redirect, g, make_response
# from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Boolean, Integer, String, DateTime
from datetime import datetime
from os.path import dirname, join, realpath


app = Flask(__name__, static_folder="static")


# tell app we in dev mode
app.config["DEBUG"] = True


# secret ket to encode wt token
app.config['SECRET KEY'] = 'beredevtestkey'
# CONNECTING TO A DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


# creating my tabes in db
class Car(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    price = Column(Integer)
    model = Column(String(50))
    fuel = Column(String(50))
    mileage = Column(String(50))
    transmission = Column(String(50))
    image_one = Column(String)
    image_two = Column(String)
    image_three = Column(String)
    image_four = Column(String)
    image_five = Column(String)
    created = DateTime()

    def __repr__(self):
        return '<Car {}>'.format(self.model)


class User(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    email = Column(String(50))
    role = Column(Integer)
    password = Column(String(50))

    def __repr__(self):
        return '<User {}>'.format(self.name)


@app.route('/')
def home():
    cars = Car.query.limit(6).all()

    return render_template('index.html', cars=cars)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.route('/car/<int:postID>')
def show_car(postID):
    car = Car.query.filter_by(id=postID).first_or_404()
    return render_template('car.html', car=car)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/cars', methods=['GET'])
def cars():
    cars = Car.query.all()
    return render_template('cars.html', cars=cars)


@app.route('/upload', methods=['POST', 'GET'])
def upload():

    if request.method == 'POST':

        name = request.form.get('name')
        model = request.form.get('model')
        price = request.form.get('price')
        mileage = request.form.get('mileage')
        fuel = request.form.get('fuel')
        transmission = request.form.get('trans')
        created = datetime.now()
        image_one = request.form.get('image1')
        image_two = request.form.get('image2')
        image_three = request.form.get('image3')
        image_four = request.form.get('image4')
        image_five = request.form.get('image5')

        newCar = Car(name=name, model=model, price=price, mileage=mileage, fuel=fuel, transmission=transmission,
                     created=created, image_one=image_one, image_two=image_two, image_three=image_three, image_four=image_four, image_five=image_five)
        db.session.add(newCar)
        db.session.commit()

        return render_template('upload.html', message="Done uploading")

    return render_template('upload.html')


if __name__ == "__main__":
    db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)
