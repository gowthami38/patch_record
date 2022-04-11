import psycopg2
from flask import Flask, request
from flask_restful import Api
from sqlalchemy import Column, String, Integer, Date, BOOLEAN, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os


app = Flask(__name__)
api = Api(app)
Base = declarative_base()
database_url = "postgresql://postgres:1234@localhost:5432/postgres"
engine = create_engine(database_url, echo=True, poolclass=NullPool)
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

class ProductEnquiry(Base):
    """ Product enquiry form model which has all details -table names & columns"""
    __tablename__ = "productenquiry"
    createdDate = Column("createddate", String)
    dealerCode = Column("dealercode", String)
    customerName = Column("customername", String)
    mobileNumber = Column("mobilenumber", Integer, primary_key=True)
    emailId = Column("emailid", String)
    vehicleModel = Column("vehiclemodel", String)
    state = Column("state", String)
    district = Column("distric", String)
    city = Column("city", String)
    existingVehicle = Column("exstingvehicle", String)
    wantTestDrive = Column("wanttestdrive", BOOLEAN)
    dealerState = Column("dealerstate", String)
    dealerTown = Column("dealertown", String)
    dealer = Column("dealer", String)
    briefAboutEnquery = Column("briefaboutenquery", String)
    expectedDateOfPurchase = Column("expecteddateofpurchase", String)
    gender = Column("gender", String)
    age = Column("age", Integer)
    occupation = Column("occupation", String)
    intendedUsage = Column("intendedusage", String)


    

class Dealer(Base):
    __tablename__ = "dealer"
    dealerName = Column("dealer_name", String, primary_key=True)
    dealerCode = Column("dealer_code", String)

@app.route('/insert_records', methods=['POST'])
def home1():
    request_body = request.get_json(force=True)

    for item in request_body:
        record = ProductEnquiry(customerName=item["customername"],
                                gender=item["gender"],
                                age=item["age"],
                                occupation=item["occupation"],
                                mobileNumber=item["mobilenumber"],
                                emailId =item["emailid"],
                                state=item["state"])

        session.add_all([record])
    session.commit()
    return "data inserted"




@app.route('/patch_record', methods=['PATCH'])
def patch_record():
    print("parameter is {}".format(request.args))
    cust_name = request.args.get("customername")
    try:
        result = session.query(ProductEnquiry).filter(ProductEnquiry.customerName == cust_name) \
            .update({"customerName": 'gowthami'})
        session.commit()
        return "data updated"
    finally:
        session.close()        

 


app.run(debug=False)

