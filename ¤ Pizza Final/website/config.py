import os
import secrets

"""
I am not sure if this is the right way to generate a secret key, so if i am doing it wrong please inform me.
I also did not figure out how to use this setting:  SQLALCHEMY_DATABASE_URI = 'sqlite:///myDataBase.db together with my sampleData.py file.
"""

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(24)
