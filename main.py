from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)

# create table
with app.app_context():
    class Movie(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(250), unique=True, nullable=False)
        year = db.Column(db.String(250), nullable=False)
        description = db.Column(db.String(250), nullable=False)
        rating = db.Column(db.Float, nullable=False)
        ranking = db.Column(db.Integer, nullable=False)
        review = db.Column(db.String(250), nullable=False)
        img_url = db.Column(db.String(250), nullable=False)

    db.create_all()


# create form
class RateMovieForm(FlaskForm):
    rating = StringField("Your rating out of 10")
    review = StringField("Your review")
    submit = SubmitField("Done")


@app.route("/")
def home():
    movies_list = db.session.query(Movie).all()
    return render_template("index.html", movies=movies_list)


# without WTForms
# @app.route("/edit", methods=['GET', 'POST'])
# def edit():
#     if request.method == "POST":
#         movie_id = request.args.get('id')
#         movie_to_update = Movie.query.get(movie_id)
#         movie_to_update.rating = request.form['new_rating']
#         movie_to_update.review = request.form['new_review']
#         db.session.commit()
#
#         return redirect(url_for('home'))
#
#     movie_id = request.args.get('id')
#     movie_selected = Movie.query.get(movie_id)
#
#     return render_template('edit.html', movie=movie_selected)

# with WTForms
@app.route("/edit", methods=['GET', 'POST'])
def rate_movie():
    form = RateMovieForm()
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('edit.html', movie=movie, form=form)


@app.route('/delete')
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)