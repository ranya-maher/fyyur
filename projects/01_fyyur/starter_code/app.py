#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(50)))
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(200))
    creation_date = db.Column('creation_date', db.DateTime(), default=datetime.now())

    shows = db.relationship('Show', backref='venue', lazy=True)

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(50)))
    seeking_venue = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(200))
    creation_date = db.Column('creation_date', db.DateTime(), default=datetime.now())

    shows = db.relationship('Show', backref='artist', lazy=True)

class Show(db.Model):
    __tablename__ = 'shows'

    artist_id = db.Column('artist_id', db.Integer(), db.ForeignKey('artists.id'), primary_key=True)
    venue_id = db.Column('venue_id', db.Integer(), db.ForeignKey('venues.id'), primary_key=True)
    start_time = db.Column('start_time', db.DateTime(), primary_key=True)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  venues=Venue.query.order_by(desc(Venue.creation_date), desc(Venue.id)).limit(10).all()
  artists=Artist.query.order_by(desc(Artist.creation_date), desc(Artist.id)).limit(10).all()
  return render_template('pages/home.html', venues=venues, artists=artists)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = [location.__dict__ for location in Venue.query.distinct(Venue.city, Venue.state).all()]
  for location in data:
      location["venues"] = [{
        "id": venue.id,
        "name": venue.name
      } for venue in Venue.query.filter_by(city=location['city']).all()]

  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form['search_term']
  venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%'))
  response = {}
  response['count'] = venues.count()
  response['data'] = venues
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  data = Venue.query.get(venue_id).__dict__
  past_shows = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time <= datetime.now()).all()
  upcoming_shows = Show.query.filter_by(venue_id=venue_id).filter(Show.start_time > datetime.now()).all()
  data['past_shows'] = [{
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      'start_time': format_datetime(str(show.start_time), 'full')
      } for show in past_shows]
  data['upcoming_shows'] = [{
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      'start_time': format_datetime(str(show.start_time), 'full')
      } for show in upcoming_shows]
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = request.form
  error = False

  try:
      venue = Venue(
          name = form['name'],
          city = form['city'],
          state = form['state'],
          address = form['address'],
          phone = form['phone'],
          genres = form.getlist('genres'),
          facebook_link = form['facebook_link'],
          website = form['website'],
          image_link = form['image_link'],
          seeking_talent = False if form['seeking_description'] == '' else True,
          seeking_description = form['seeking_description']
      )
      db.session.add(venue)
      db.session.commit()

  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()
  if not error:
      flash('Venue ' + form['name'] + ' was successfully listed!')
  else:
      flash('An error occurred. Venue ' + form['name'] + ' could not be listed.')
  return redirect(url_for('index'))


@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue(venue_id):
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error = False
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

  # clicking that button delete it from the db then redirect the user to the homepage
    if not error:
        flash('Venue ' + venue_id + ' was successfully deleted!')
    else:
        flash('An error occurred. Venue ' + venue_id + ' could not be deleted.')

    return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  data = Artist.query.order_by('id').all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form['search_term']
  artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%'))
  response = {}
  response['count'] = artists.count()
  response['data'] = artists
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  data = Artist.query.get(artist_id).__dict__
  past_shows = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time <= datetime.now()).all()
  upcoming_shows = Show.query.filter_by(artist_id=artist_id).filter(Show.start_time > datetime.now()).all()
  data['past_shows'] = [{
      'venue_id': show.venue_id,
      'venue_name': show.venue.name,
      'venue_image_link': show.venue.image_link,
      'start_time': format_datetime(str(show.start_time), 'full')
      } for show in past_shows]
  data['upcoming_shows'] = [{
      'venue_id': show.venue_id,
      'venue_name': show.venue.name,
      'venue_image_link': show.venue.image_link,
      'start_time': format_datetime(str(show.start_time), 'full')
      } for show in upcoming_shows]
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # artist record with ID <artist_id> using the new attributes
  error = False
  form = request.form
  artist = Artist.query.get(artist_id)
  try:
      artist.name = form['name'],
      artist.city = form['city'],
      artist.state = form['state'],
      artist.phone = form['phone'],
      artist.genres = form.getlist('genres'),
      artist.facebook_link = form['facebook_link'],
      artist.website = form['website'],
      artist.image_link = form['image_link'],
      artist.seeking_venue = False if form['seeking_description'] == '' else True,
      artist.seeking_description = form['seeking_description']

      db.session.commit()

  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()
  if not error:
      flash('Artist ' + form['name'] + ' was successfully updated!')
  else:
      flash('An error occurred. Artist ' + form['name'] + ' could not be updated.')
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # venue record with ID <venue_id> using the new attributes
  form = request.form
  error = False

  venue = Venue.query.get(venue_id)
  try:
      venue.name = form['name'],
      venue.city = form['city'],
      venue.state = form['state'],
      venue.address = form['address'],
      venue.phone = form['phone'],
      venue.genres = form.getlist('genres'),
      venue.facebook_link = form['facebook_link'],
      venue.website = form['website'],
      venue.image_link = form['image_link'],
      venue.seeking_talent = False if form['seeking_description'] == '' else True,
      venue.seeking_description = form['seeking_description']

      db.session.commit()

  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()
  if not error:
      flash('Venue ' + form['name'] + ' was successfully updated!')
  else:
      flash('An error occurred. Venue ' + form['name'] + ' could not be updated.')
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  form = request.form
  error = False

  try:
      artist = Artist(
          name = form['name'],
          city = form['city'],
          state = form['state'],
          phone = form['phone'],
          genres = form.getlist('genres'),
          facebook_link = form['facebook_link'],
          website = form['website'],
          image_link = form['image_link'],
          seeking_venue = False if form['seeking_description'] == '' else True,
          seeking_description = form['seeking_description']
      )
      db.session.add(artist)
      db.session.commit()

  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()
  if not error:
      flash('Artist ' + form['name'] + ' was successfully listed!')
  else:
      flash('An error occurred. Artist ' + form['name'] + ' could not be listed.')
  return redirect(url_for('index'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = db.session.query(Show).join(Artist).join(Venue).all()
  data = [{
      'venue_id': show.venue_id,
      'venue_name': show.venue.name,
      'artist_id': show.artist.id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': format_datetime(str(show.start_time), 'full')
      } for show in shows]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  error = False

  try:
      form = request.form
      show = Show(
        venue_id = form['venue_id'],
        artist_id = form['artist_id'],
        start_time = form['start_time']
      )
      db.session.add(show)
      db.session.commit()

  except:
      error = True
      db.session.rollback()
      print(sys.exc_info())

  finally:
      db.session.close()
  if not error:
      flash('Show was successfully listed!')
  else:
      flash('An error occurred. Show could not be listed.')
  return redirect(url_for('index'))


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
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
