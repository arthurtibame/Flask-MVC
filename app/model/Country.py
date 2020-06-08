from app import db

class Country(db.Model):
    __tablename__ = 'b_country'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=True)
    
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Country %r>' % self.name