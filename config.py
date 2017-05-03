class Config():
    pass


class DevConfig():
    SECRET_KEY = 'SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Password@localhost:3306/Flaskr_data'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
