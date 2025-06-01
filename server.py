from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config["SECRET_KEY"] = "my super secret key that no one is supposed to know"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movie-collection.db"
db = SQLAlchemy(app)

class Movie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    year: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)
    ranking: Mapped[int] = mapped_column(nullable=False)
    review: Mapped[str] = mapped_column(String(250), nullable=False)
    image_url: Mapped[str] = mapped_column(nullable=False)


class Edit(FlaskForm):
    rating = StringField("Rate from 1 to 10: ", validators=[DataRequired()])
    review = StringField("Update the review (optional):")
    submit = SubmitField("Update")

class Add(FlaskForm):
    movie = StringField("Enter the name of the movie: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/')
def home():
    movies = db.session.query(Movie).all()
    return render_template("index.html", movies=movies)

@app.route('/edit/<int:movie_id>', methods=["GET", "POST"])
def edit(movie_id):
    movie = db.session.get(Movie, int(movie_id))
    form = Edit()

    if not movie:
        return "Movie Not Found", 404

    if form.validate_on_submit():
        movie.rating = form.rating.data
        if form.review.data:
            movie.review = form.review.data
        db.session.commit()
        return redirect("/")
    return render_template("edit.html", form=form)

@app.route('/delete/<int:movie_id>', methods=["POST"])
def delete(movie_id):
    book_to_delete = db.session.get(Movie, int(movie_id))
    if book_to_delete:
        db.session.delete(book_to_delete)
        db.session.commit()
    return redirect("/")

@app.route('/add', methods=["GET", "POST"])
def add():
    form = Add()
    return render_template("add.html", form=form)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)