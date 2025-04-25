import os

class Config:
    SECRET_KEY = 'your_secret_key' 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///D:/IITM/NEW/Chatgpt2/code/site.db'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
