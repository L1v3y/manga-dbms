from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pymysql
import os

app = Flask(__name__)
app.secret_key = 'asdf'  # Change this to a random secret key

# MySQL Configuration
MYSQL_HOST = 'localhost'
MYSQL_USER = '<your_username>'
MYSQL_PASSWORD = '<your_password>'
MYSQL_DB = 'manga'

# Connect to MySQL
conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB, cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def index():
    if 'username' in session:
        # Fetch manga data from the database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Manga")
        manga_data = cursor.fetchall()
        return render_template('dashboard.html', manga_data=manga_data)
    else:
        return redirect(url_for('login'))

def manga():
    if 'username' in session:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Manga")
        manga_data = cursor.fetchall()
        return render_template('manga.html', manga_data=manga_data)
    else:
        return redirect(url_for('login'))

@app.route('/author')
def author():
    if 'username' in session:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Author")
        author_data = cursor.fetchall()
        return render_template('author.html', author_data=author_data)
    else:
        return redirect(url_for('login'))

@app.route('/genre')
def genre():
    if 'username' in session:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Genre")
        genre_data = cursor.fetchall()
        return render_template('genre.html', genre_data=genre_data)
    else:
        return redirect(url_for('login'))

@app.route('/review')
def review():
    if 'username' in session:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Review")
        review_data = cursor.fetchall()
        return render_template('review.html', review_data=review_data)
    else:
        return redirect(url_for('login'))

@app.route('/publish')
def publish():
    if 'username' in session:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Publish")
        publish_data = cursor.fetchall()
        return render_template('publish.html', publish_data=publish_data)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the username and password are correct (you should hash the password for security)
        if username == 'hemker' and password == 'animedekhnewalahemker':
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')


@app.route('/add_manga_entry', methods=['GET', 'POST'])
def add_manga_entry():
    if request.method == 'POST':
        try:
            # Get form data
            manga_id = request.form['manga_id']
            title = request.form['title']
            description = request.form['description']
            cover_image = request.form['cover_image']
            release_date = request.form['release_date']
            status = request.form['status']
            author_id = request.form['author_id']
            rating = request.form['rating']
            genre_id = request.form['genre_id']
            publisher_id = request.form['publisher_id']

            # Perform SQL insertion
            with conn.cursor() as cursor:
                sql = "INSERT INTO Manga (MangaID, Title, Description, CoverImage, ReleaseDate, Status, AuthorID, Rating, GenreID, PublisherID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (manga_id, title, description, cover_image, release_date, status, author_id, rating, genre_id, publisher_id))
                conn.commit()

            response = {'success': True, 'message': 'Manga entry added successfully.'}
        except Exception as e:
            conn.rollback()
            response = {'success': False, 'message': str(e)}

        return jsonify(response)
    else:
        # Handle GET request to render the HTML form
        return render_template('add_manga_entry.html')

@app.route('/delete_manga_entry', methods=['GET','POST'])
def delete_manga_entry():
    if request.method == 'POST':
        try:
            # Get MangaID from form data
            manga_id = request.form['manga_id']

            # Perform SQL deletion
            with conn.cursor() as cursor:
                sql = "DELETE FROM Manga WHERE MangaID = %s"
                cursor.execute(sql, (manga_id,))
                conn.commit()

            response = {'success': True, 'message': 'Manga entry deleted successfully.'}
        except Exception as e:
            conn.rollback()
            response = {'success': False, 'message': str(e)}

        return jsonify(response)
    else:
        # Handle GET request to render the HTML form
        return render_template('delete_manga_entry.html')    

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
