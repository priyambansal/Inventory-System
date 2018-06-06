import os

from flask import Flask, render_template,request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= "mysql://priyamb:Pass=1234@localhost/FlaskInventory"
engine = create_engine("mysql://priyamb:Pass=1234@localhost/FlaskInventory", pool_pre_ping=True)
connection = engine.connect()
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
Base = declarative_base()
db = SQLAlchemy(app)

class Item(db.Model):
    
    itemid = db.Column(db.Integer, primary_key=True)
    itemname = db.Column(db.String(20), nullable=False)
    itemqty = db.Column(db.Integer, nullable=False)
    itemtype = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(150))
    itemasgn = db.relationship('Assignment',backref = 'itemasgnto')

    def __init__(self, itemname,itemqty,itemtype,price,description):
        self.itemname=itemname
        self.itemqty=itemqty
        self.itemtype=itemtype
        self.price=price
        self.description=description

    
class Employee(db.Model):
    
    empid = db.Column(db.Integer, primary_key=True)
    empname = db.Column(db.String(20), nullable=False)
    doj = db.Column(db.Date(), nullable=False)
    active = db.Column(db.String(1), nullable=False)
    doe = db.Column(db.Date())
    empasgn = db.relationship('Assignment', backref = 'empasgnto')

    def __init__(self, empname, doj, active, doe, empassign):
        self.empname=empname
        self.doj-doj
        self.active=active
        self.doe=doe
        self.empassign=empassign

class Assignment(db.Model):
    
    asgnid = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.empid'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.itemid'), nullable=False)
    qtyasgn = db.Column(db.Integer, nullable = False)
    fromdate = db.Column(db.Date(), nullable=False)
    todate = db.Column(db.Date())

    def __init__(self,qtyasgn,fromdate,todate):
        self.qtyasgn=qtyasgn
        self.fromdate=fromdate
        self.todate=todate

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_items', methods=('POST','GET'))
def add_items():
    if request.method=='POST':
        itemname=request.form['itemname']
        itemqty=request.form['itemqty']
        itemtype=request.form['itemtype']
        price=request.form['price']
        description=request.form['description']

        error= None

        if not itemname or not itemqty or not itemtype or not price:
            error='Fill the required fields'
        else:
            new_item = Item(itemname,itemqty,itemtype,price,description)

            db.session.add(item)
            db.session.commit()
            return redirect(url_for('index'))

        flash(error)

    return render_template('items.html')

