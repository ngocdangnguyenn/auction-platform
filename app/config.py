import os
class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://nndng:Nguyen2016@localhost:3305/projetweb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
