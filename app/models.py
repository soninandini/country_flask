
from app import db
from datetime import datetime, timezone

class Country(db.Model):
    __tablename__ = 'countries'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cca = db.Column(db.String(3), nullable=False)
    currency_code = db.Column(db.String(10), nullable=True)
    currency = db.Column(db.String(50), nullable=True)
    capital = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(100), nullable=True)
    subregion = db.Column(db.String(100), nullable=True)
    area = db.Column(db.BigInteger, nullable=False)
    map_url = db.Column(db.String(255), nullable=True)
    population = db.Column(db.BigInteger, nullable=True)
    flag_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    neighbours = db.relationship('CountryNeighbour', backref='country', lazy=True)

class CountryNeighbour(db.Model):
    __tablename__ = 'country_neighbours'

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    neighbour_country_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
