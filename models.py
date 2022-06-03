from flask_sqlalchemy import SQLAlchemy
from app import app
db = SQLAlchemy(app)


# Models.


class Artist(db.Model):

    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(150), nullable=False)
    state = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(150), nullable=False)
    genres = db.Column(db.String(150), nullable=False)
    website = db.Column(db.String(150), nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(300), nullable=False)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(150), nullable=False)

    # venues = db.relationship('Venue', secondary='shows')
    shows = db.relationship('Show', backref=('artists'))

    def to_dict(self):
        """ Returns a dictinary of artists """
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': self.genres.split(','),  # convert string to list
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
        }

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'


class Venue(db.Model):
    """ Venue Model """
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(150),nullable=False)
    state = db.Column(db.String(150),nullable=False)
    address = db.Column(db.String(150),nullable=False)
    phone = db.Column(db.String(150),nullable=False)
    genres = db.Column(db.String(150),nullable=False)
    image_link = db.Column(db.String(500),nullable=False)
    facebook_link = db.Column(db.String(300),nullable=False)
    website = db.Column(db.String(120),nullable=False)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120), nullable=False)

    # artists = db.relationship('Artist', secondary='shows')
    shows = db.relationship('Show', backref=('venues'))

    def to_dict(self):
        """ Returns a dictinary of vevenuesnues """
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'genres': self.genres.split(','),  # convert string to list
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
        }

    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'


class Show(db.Model):
    """ Show Model """
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    venue = db.relationship('Venue')
    artist = db.relationship('Artist')

    def show_artist(self):
        """ Returns a dictinary of artists for the show """
        return {
            'artist_id': self.artist_id,
            'artist_name': self.artist.name,
            'artist_image_link': self.artist.image_link,
            # convert datetime to string
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S')
        }

    def show_venue(self):
        """ Returns a dictinary of venues for the show """
        return {
            'venue_id': self.venue_id,
            'venue_name': self.venue.name,
            'venue_image_link': self.venue.image_link,
            # convert datetime to string
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S')
        }