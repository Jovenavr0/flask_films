import os
from flask import render_template, redirect, url_for, request
from werkzeug.utils import secure_filename

from . import app, db
from .models import Movie, Review
from .forms import ReviewForm, MovieForm


@app.route('/')
def index():
    movies = Movie.query.order_by(Movie.id.desc()).all()
    return render_template('index.html',
                           movies=movies)



@app.route('/movie/<int:id>', methods=['GET', 'POST'])
def movie_detail(id: int):
    movie = Movie.query.get(id)
    if movie.reviews:
        avg_score = round(sum(review.score \
            for review in movie.reviews) /
                          len(movie.reviews), 2)
    else:
        avg_score = 0
    form = ReviewForm(score=10)
    if form.validate_on_submit():
        review = Review()
        review.name = form.name.data
        review.text = form.text.data
        review.score = form.score.data
        review.movie_id = movie.id
        db.session.add(review)
        db.session.commit()
        return redirect(url_for('movie_detail', id=movie.id))
    return render_template('movie.html',
                           movie=movie,
                           avg_score=avg_score,
                           form=form)


@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie()
        movie.title = form.title.data
        movie.description = form.description.data
        file = request.files['image']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            movie.image = form.image.data.filename
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('movie_detail', id=movie.id))
    return render_template('add_movie.html',
                           form=form)


@app.route('/reviews')
def reviews():
    reviews = Review.query.order_by(Review.id.desc()).all()
    return render_template('reviews.html',
                           reviews=reviews)


@app.route('/detete_reviews/<int:id>')
def delete_review(id):
    Review.query.filter(Review.id == id).delete()
    db.session.commit()
    return redirect(url_for('reviews'))

@app.route('/delete_movies/<int:id>')
def delete_movies(id):
    Movie.query.filter(Movie.id == id).delete()
    Review.query.filter(Review.movie_id == id).delete()
    db.session.commit()
