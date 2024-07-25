import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///telemedconnect.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "@mefgaed2024demsoge#"
    JWT_ACCESS_TOKEN_EXPIRES = 604800  # 7days
