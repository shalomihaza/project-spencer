from app import db


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
    looking_for_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(150))

    shows = db.relationship('Show', backref='artists',
                            lazy=True, cascade="all")

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(150), nullable=False)
    state = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(150), nullable=False)
    genres = db.Column(db.String(150), nullable=False)
    facebook_link = db.Column(db.String(300))

    image_link = db.Column(db.String(1000))
    website_link = db.Column(db.String(150))
    looking_for_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(150))

    shows = db.relationship('Show', backref=('venues'))

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

    def __repr__(self):
        return f'<Venue {self.id} {self.artist_id} {self.venue_id}>'
