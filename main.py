from flask import render_template, redirect, request, url_for, flash
from models import app, db, Books, BookForm, Delete, RecommendBook, Image, Read, get_image
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import CSRFProtect, validate_csrf
import smtplib
import requests
import os

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
csrf = CSRFProtect(app)
bootstrap = Bootstrap5(app)



with app.app_context():
    db.create_all()

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit():

    results = db.session.query(Books.title, Books.author).all()
    books = [f"{row.title} --- {row.author}" for row in results]
    ur_results = db.session.query(Books.title, Books.author).filter(Books.read == False).all()
    ur_books = [f"{row.title} --- {row.author}" for row in ur_results]
    books.insert(0, "")
    ur_books.insert(0, "")
    add = BookForm()
    delete = Delete()
    image = Image()
    read = Read()
    read.book.choices = ur_books
    delete.book.choices = books
    image.book.choices = books

    if request.method == 'POST':
        if add.validate_on_submit():
            title = add.title.data.strip()
            author = add.author.data.strip()
            read = add.read.data
            img = get_image(title)
            if img == None:
                img = 'static/no-cover.png'
            new_book = Books(title=title, author=author, img=img, read=read)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('edit'))
        else:
            message = "<p style='color:red'>*ERROR*</p>"
            return render_template('edit.html', add=add, image=image, delete=delete, read=read, new_message=message)
        
    else:
        return render_template('edit.html', add=add, delete=delete, read=read, image=image)
    
@app.route('/read_book', methods=['POST'])
def read_book():

    results = db.session.query(Books.title, Books.author).all()
    books = [f"{row.title} --- {row.author}" for row in results]
    ur_results = db.session.query(Books.title, Books.author).filter(Books.read == False).all()
    ur_books = [f"{row.title} --- {row.author}" for row in ur_results]
    books.insert(0, "")
    ur_books.insert(0, "")
    add = BookForm()
    delete = Delete()
    image = Image()
    read = Read()
    read.book.choices = ur_books
    delete.book.choices = books
    image.book.choices = books

    if read.validate_on_submit():
        title = image.book.data.split(' --- ')[0]
        entry = db.session.query(Books).filter(Books.title == title).first()
        entry.read = 1
        db.session.commit()
        return redirect(url_for('edit'))
    else:
        message = "<p style='color:red'>*ERROR*</p>"
        return render_template('edit.html', add=add, delete=delete, image=image, read=read, rd_message=message)
    
@app.route('/image', methods=['POST'])
def image():

    results = db.session.query(Books.title, Books.author).all()
    books = [f"{row.title} --- {row.author}" for row in results]
    ur_results = db.session.query(Books.title, Books.author).filter(Books.read == False).all()
    ur_books = [f"{row.title} --- {row.author}" for row in ur_results]
    books.insert(0, "")
    ur_books.insert(0, "")
    add = BookForm()
    delete = Delete()
    image = Image()
    read = Read()
    read.book.choices = ur_books
    delete.book.choices = books
    image.book.choices = books

    if image.validate_on_submit():
        title = image.book.data.split(' --- ')[0]
        entry = db.session.query(Books).filter(Books.title == title).first()
        image = image.image.data
        entry.img = image
        db.session.commit()
        return redirect(url_for('edit'))
    else:
        message = "<p style='color:red'>*ERROR*</p>"
        return render_template('edit.html', add=add, delete=delete, image=image, read=read, img_message=message)
    
@app.route('/delete', methods=['POST'])
def delete():

    results = db.session.query(Books.title, Books.author).all()
    books = [f"{row.title} --- {row.author}" for row in results]
    ur_results = db.session.query(Books.title, Books.author).filter(Books.read == False).all()
    ur_books = [f"{row.title} --- {row.author}" for row in ur_results]
    books.insert(0, "")
    ur_books.insert(0, "")
    add = BookForm()
    delete = Delete()
    image = Image()
    read = Read()
    read.book.choices = ur_books
    delete.book.choices = books
    image.book.choices = books

    if delete.validate_on_submit():
        title = delete.book.data.split(' --- ')[0]
        entry = db.session.query(Books).filter(Books.title == title).first()
        db.session.delete(entry)
        db.session.commit()
        return redirect(url_for('edit'))
    else:
        message = "<p style='color:red'>*ERROR*</p>"
        return render_template('edit.html', add=add, image=image, delete=delete, read=read, del_message=message)

@app.route('/read')
def read():
    results = db.session.query(Books).filter(Books.read == True).all()
    return render_template('books.html', books=results, heading='Read Books')

@app.route('/unread')
def unread():
    results = db.session.query(Books).filter(Books.read == False).all()
    return render_template('books.html', books=results, heading='Reading List')

@app.route('/rec', methods=['GET', 'POST'])
def rec():

    rec = RecommendBook()
    if request.method == 'POST':
        if rec.validate_on_submit():
            my_email = os.getenv("SMTP_EMAIL")
            password = os.getenv("SMTP_PASSWORD")

            title = rec.title.data
            author = rec.author.data
            details = rec.details.data
            their_email = rec.email.data
            connection = smtplib.SMTP("smtp.gmail.com", 587)
            connection.starttls()
            connection.login(my_email, password)
            connection.sendmail(from_addr=my_email, to_addrs=my_email, 
                                msg=f'Subject: Book Recommendation!\n\n{title} by {author} was recommended by {their_email}. They recommended this book because: {details}')
            connection.close()
            flash("<p style='color:green'>Email successfully sent!</p>")
            return redirect(url_for('rec'))
        else:
            flash("<p style='color:red'>Invalid reCAPTCHA</p>")
            return redirect(url_for('rec'))
        
    return render_template('rec.html', form=rec)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
