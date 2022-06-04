from flask_sqlalchemy import SQLAlchemy
from app import db
# db = SQLAlchemy(app)


class Artist(db.Model):

    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(150), nullable=False)
    state = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(150), nullable=False)
    genres = db.Column(db.String(150), nullable=False)
    facebook_link = db.Column(db.String(300))
    image_link = db.Column(db.String(1000))

    website_link = db.Column(db.String(150))
    looking_for_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(150), nullable=False)

    shows = db.relationship('Show', backref='artists', lazy=True, cascade="all")

    def __init__(self, name,  city, state, phone,genres,facebook_link, image_link, website_link,
                 looking_for_venue=False, seeking_description=""):
        self.name = name
        self.city = city
        self.state = state
        self.phone = phone
        self.genres = genres
        self.image_link = image_link

        self.website_link = website_link
        self.facebook_link = facebook_link
        self.seeking_description = seeking_description
        self.looking_for_venue = looking_for_venue


    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(150),nullable=False)
    state = db.Column(db.String(150),nullable=False)
    address = db.Column(db.String(150),nullable=False)
    phone = db.Column(db.String(150),nullable=False)
    genres = db.Column(db.String(150),nullable=False)
    facebook_link = db.Column(db.String(300))

    image_link = db.Column(db.String(1000))
    website_link = db.Column(db.String(150))
    looking_for_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(150), nullable=False)

    shows = db.relationship('Show', backref=('venues'))



    def __init__(self, name,  city, state, address,phone,genres,facebook_link, image_link, website_link,
                 looking_for_talent=False, seeking_description=""):
        self.name = name
        self.city = city
        self.state = state
        self.address = address

        self.phone = phone
        self.genres = genres
        self.image_link = image_link

        self.website_link = website_link
        self.facebook_link = facebook_link
        self.seeking_description = seeking_description
        self.looking_for_talent = looking_for_talent

    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
