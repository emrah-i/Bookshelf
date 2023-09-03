from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, BooleanField, PasswordField, SelectField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
db.init_app(app)

def get_image(title):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    response = requests.get(url=f'https://www.goodreads.com/search?q={title}')
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    anchor = soup.select('table[class="tableList"] tr td a[class="bookTitle"]')
    link = anchor[0]['href']
    response = requests.get(url=f"https://www.goodreads.com/{link}", headers=headers)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    img = soup.select('img[class="ResponsiveImage"]')
    if len(img) == 0:
        return None

    return img[0]['src']

def must_equal_validator(form, field):
    if field.data != "ilovecats":
        raise ValidationError("Key is wrong. You cannot edit the database.")

class Books(db.Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(150), unique=True, nullable=False)
    author = Column(String(100))
    img = Column(String(250))
    read = Column(Boolean, default=False)

class BookForm(FlaskForm):
    key = PasswordField('Key:', validators=[DataRequired(), must_equal_validator], render_kw={'placeholder': 'Keyword'})
    title = StringField('Title:', validators=[DataRequired(), Length(min=2, max=150)], render_kw={'placeholder': 'Title'})
    author = StringField('Author:', validators=[DataRequired(), Length(min=2, max=150)], render_kw={'placeholder': 'Author'})
    read = BooleanField('Read')
    submit = SubmitField()

class Image(FlaskForm):
    key = PasswordField('Key:', validators=[DataRequired(), must_equal_validator], render_kw={'placeholder': 'Keyword'})
    book = SelectField('Select Book:', validators=[DataRequired()])
    image = StringField('Image Source:', validators=[DataRequired(), Length(min=2, max=250)], render_kw={'placeholder': 'Source'})
    submit = SubmitField()

class Delete(FlaskForm):
    key = PasswordField('Key:', validators=[DataRequired(), must_equal_validator], render_kw={'placeholder': 'Keyword'})
    book = SelectField('Select Book:', validators=[DataRequired()])
    delete = SubmitField(render_kw={'value': 'Delete', 'style': 'background-color: #E74C3C;border-color: #E74C3C'})

class Read(FlaskForm):
    key = PasswordField('Key:', validators=[DataRequired(), must_equal_validator], render_kw={'placeholder': 'Keyword'})
    book = SelectField('Select Book:', validators=[DataRequired()])
    read = SubmitField(render_kw={'value': 'Read'})

class RecommendBook(FlaskForm):
    title = StringField('Title:', validators=[DataRequired(), Length(min=2, max=150)], render_kw={'placeholder': 'Title'})
    author = StringField('Author:', validators=[DataRequired(), Length(min=2, max=150)], render_kw={'placeholder': 'Author'})
    details = TextAreaField('Details:', validators=[DataRequired(), Length(min=2, max=500)], render_kw={'placeholder': 'Enter your reason for recommending'})
    email = EmailField('Your Email:', validators=[DataRequired()], render_kw={'placeholder': 'Email'})
    send = SubmitField()
