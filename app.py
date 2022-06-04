#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import distinct
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:001postgresqlmega@localhost:5432/fyyur'

db = SQLAlchemy(app)
# db.init_app(app)
# migrate = Migrate(app, db)

from models import Artist, Show, Venue
db.create_all()
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  data = []

  try:
    venue_data = db.session.query(distinct(Venue.city), Venue.state).all()

    for event in venue_data:

      event_data = {"city": event[0], "state": event[1], "venues": []}

      venues_array = Venue.query.filter_by(city=event[0], state=event[1]).all()

      for venue in venues_array:

        upcoming_shows = (
          Show.query.filter_by(venue_id=venue.id)
            .filter(Show.start_time > datetime.now())
            .all()
        )

        venue_dict = {
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": len(upcoming_shows),
        }

        event_data["venues"].append(venue_dict)
        print(event_data)
      data.append(event_data)
    return render_template("pages/venues.html", areas=data)
  except:
        db.session.rollback()
        print(sys.exc_info())
        print("Error. Please try again also.")
        return render_template("pages/home.html")

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get("search_term", "")

  # response = {"total": 0, "data": []}

  venue_results = (
    db.session.query(Venue)
      .filter(Venue.name.ilike(f"%{search_term}%"))
      .all()
  )

  # response["total"] = len(venue_results)
  result_item=[]
  for result in venue_results:
    item = {
      "id": result.id,
      "name": result.name,
    }
    result_item.append(item)

  return render_template(
    "pages/search_venues.html",
    results={'total':len(venue_results),result_item:result_item},
    search_term=search_term,
  )

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  data={}
  try:
    venue = Venue.query.get(venue_id)
    shows = Show.query.filter_by(venue_id=venue_id)

    past_shows_list = shows.filter(Show.start_time < datetime.now()).all()
    past_shows_data = []
    for show in past_shows_list:
      artist = Artist.query.get(show.artist_id)
      # show_data = {
      #   "artist_id": artist.id,
      #   "artist_name": artist.name,
      #   "artist_image_link": artist.image_link,
      #   "start_time": str(show.start_time),
      # }
      past_shows_data.append({
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": str(show.start_time),
      })

    upcoming_shows_list = shows.filter(Show.start_time >= datetime.now()).all()
    upcoming_shows = []
    for show in upcoming_shows_list:
      artist = Artist.query.get(show.artist_id)
      # show_data = {
      #   "artist_id": artist.id,
      #   "artist_name": artist.name,
      #   "artist_image_link": artist.image_link,
      #   "start_time": str(show.start_time),
      # }
      upcoming_shows.append({
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": str(show.start_time),
      })

    data = {
      "id": venue.id,
      "name": venue.name,
      "genres": venue.genres,
      "address": venue.address,
      "city": venue.city,
      "state": venue.state,
      "phone": venue.phone,
      "website": venue.website_link,
      "facebook_link": venue.facebook_link,
      "seeking_talent": venue.looking_for_talent,
      "image_link": venue.image_link,
      "past_shows": past_shows_data,
      "upcoming_shows": upcoming_shows,
      "past_shows_count": len(past_shows_data),
      "upcoming_shows_count": len(upcoming_shows),
    }

  except:
    print(sys.exc_info())
    flash("Something went wrong. Please try again.")

  # finally:
  #   db.session.close()

  return render_template("pages/show_venue.html", venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():


  try:
    # Create model
    venue = Venue(
      name=request.form['name'],
      city=request.form['city'],
      state=request.form['state'],
      address=request.form['state'],
      genres=request.form.getlist('genres'),

      phone=request.form['phone'],
      image_link=request.form['image_link'],
      facebook_link=request.form['facebook_link'],
      website_link=request.form['website'],
      looking_for_talent=True if 'seeking_talent' in request.form else False,
      seeking_description=request.form['seeking_description'],
    )
    db.session.add(venue)
    db.session.commit()
    flash(
      'Venue '
      + request.form['name']
      + ' was successfully listed!',
      'success'
    )
  except:

    db.session.rollback()
    print(sys.exc_info())
    flash(
      'Venue '
      + request.form['name']
      + ' could not be listed.',
      'danger'
    )
  finally:
    db.session.close()

  return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
    venue = Venue.query.get(venue_id)

    db.session.delete(venue)
    db.session.commit()

    flash('Delete Successful')
  except:
    db.session.rollback()
    flash('An error occured and Venue was not deleted', 'danger')

  finally:
    db.session.close()

  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.all()

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term')
  result_list = Artist.query.filter(
    Artist.name.ilike(
      '%{}%'.format(search_term))).all()  # search results by ilike matching partern to match every search term
  count=len(result_list)
  data=result_list
  response = {
    "count":count,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):


  artist = Artist.query.get(artist_id)
  shows_list = Show.query.filter_by(artist_id=artist_id).all()
  past_shows = []
  upcoming_shows = []


  for show in shows_list:
    venue = Venue.query.get(show.venue_id)
    data = {
      "venue_id": venue.id,
      "venue_name": venue.name,
      "venue_image_link":venue.image_link,
      "start_time": str(show.start_time)
    }
    if show.start_time > datetime.now():
      upcoming_shows.append(data)
    else:
      past_shows.append(data)

  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  artist = Artist.query.get(artist_id)

  form = ArtistForm()


  data = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "facebook_link": artist.facebook_link,
    "image_link": artist.image_link,
    "website": artist.website_link,

    "seeking_venue": artist.looking_for_venue,
    "seeking_description":artist.seeking_description,
  }

  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  try:
    artist = Artist.query.get(artist_id)

    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone =  request.form['phone']
    artist.genres = request.form.getlist('genres')
    artist.image_link = request.form['image_link']
    artist.facebook_link = request.form['facebook_link']
    artist.website_link =  request.form['website']
    artist.looking_for_venue = True if 'seeking_venue' in request.form else False
    artist.seeking_description = request.form['seeking_description']

    db.session.add(artist)
    db.session.commit()

    db.session.refresh(artist)
    flash("Edit was successfully completed!")

  except:
    db.session.rollback()
    print(sys.exc_info())
    flash(
      "An error occurred. Please try again "
    )

  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  venue = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "image_link": venue.image_link,

    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.looking_for_talent,
    "seeking_description": venue.seeking_description,
  }
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  try:
    venue = Venue.query.get(venue_id)

    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.phone =  request.form['phone']
    venue.genres = request.form.getlist('genres')
    venue.image_link = request.form['image_link']
    venue.facebook_link = request.form['facebook_link']
    venue.website_link =  request.form['website']
    venue.looking_for_talent = True if 'seeking_talent' in request.form else False
    venue.seeking_description = request.form['seeking_description']

    db.session.add(venue)
    db.session.commit()

    # db.session.refresh(venue)
    flash("Edit was successfully completed!")

  except:
    db.session.rollback()
    print(sys.exc_info())
    flash(
      "An error occurred. Please try again "
    )

  finally:
    db.session.close()
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:

    artist = Artist(
      name=request.form['name'],
      city=request.form['city'],
      state=request.form['state'],
      address=request.form['state'],
      genres=request.form.getlist('genres'),

      phone=request.form['phone'],
      image_link=request.form['image_link'],
      facebook_link=request.form['facebook_link'],
      website_link=request.form['website'],
      looking_for_venue=True if 'seeking_venue' in request.form else False,
      seeking_description=request.form['seeking_description'],
    )
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:

    db.session.rollback()
    print(sys.exc_info())
    flash(
      'Artist '
      + request.form['name']
      + ' could not be listed.',
      'danger'
    )
  finally:
    db.session.close()

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  shows = Show.query.all()

  data = []
  for show in shows:
    artist = Artist.query.get(show.artist_id)
    venue= Venue.query.get(show.venue_id)
    data.append({
      'venue_id': show.venue.id,
      'venue_name': venue.name,
      'artist_id': show.artist.id,
      'artist_name': artist.name,
      'artist_image_link':artist.image_link,
      'start_time': str(show.start_time())
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:

    db.session.add(Show(
      artist_id=request.form['artist_id'],
      venue_id=request.form['venue_id'],
      start_time=request.form['start_time'],
    ))
    db.session.commit()
    flash('Show was successfully listed')
  except Exception:
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
    print(sys.exc_info())
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug= True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
