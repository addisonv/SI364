# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, ValidationError
from wtforms.validators import Required, Length
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Shell # New

# Basic Flask application setup
basedir = os.path.abspath(os.path.dirname(__file__)) # In case we need to reference the base directory of the application
# To set up application and defaults for running
app = Flask(__name__)
app.debug = True
app.use_reloader = True

app.config['SECRET_KEY'] = 'hardtoguessstring'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://localhost/moviedirdb" # TODO: May need to change this, Windows users. Everyone will need to have created a db with exactly this name.
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Setup
manager = Manager(app) # In order to use manager
db = SQLAlchemy(app) # For database use

## Models
class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    director_id = db.Column(db.Integer,db.ForeignKey("directors.id"))

class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255))
    movies = db.relationship('Movie',backref='Director') # building the relationship -- one director, many movies

## Forms
class MovieForm(FlaskForm):
    name = StringField("Enter the name of a movie you like:", validators=[Required(),Length(1,64)])
    director_name = StringField("Enter the name of the movie's director:",validators=[Required()])
    submit = SubmitField()

## Routes
@app.route('/',methods=["GET","POST"])
def home():
    form = MovieForm()
    if form.validate_on_submit():
        movie_name = form.name.data
        movie_dir = form.director_name.data
        # Find out if that director exists already
        director = Director.query.filter_by(full_name=movie_dir).first() # None if no such one -- make sure to use the .first() so it's not just a BaseQuery object!!
        if not director: # If None
            # Create that director object
            director = Director(full_name=movie_dir)
            # And save it
            db.session.add(director) # Like adding in git...
            # That's all we want to add for now, can commit
            db.session.commit()
        # No matter what, in this case, should add the movie. (This does NOT check if a movie of the same name exists.)
        movie = Movie(name=movie_name,director_id=director.id) # Using the id from that director object above!
        # Now add and commit the movie
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('home'))
    # And if we didn't submit the form...
    return render_template('home.html',form=form)

@app.route('/movies')
def movies():
    movies = Movie.query.all()
    movies_directors = [(m, Director.query.filter_by(id=m.director_id).first()) for m in movies]
    return render_template('movies_fancy.html', movies=movies_directors)

if __name__ == "__main__":
    db.create_all()
    manager.run()
