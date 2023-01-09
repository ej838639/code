"""
Book Search App

Based on the following requirements:
https://github.com/oreillymedia/interview-exercise-cloud

open browser and enter:
http://localhost:5000/book_search/choose
"""
import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect
import functools

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(host=os.environ['POSTGRES_URL'],
                            port=os.environ['POSTGRES_PORT'],
                            dbname=os.environ['POSTGRES_DB'],
                            user=os.environ['POSTGRES_USER'],
                            password=os.environ['POSTGRES_PW'])
    return conn


def config_db(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = get_db_connection()
        cur = conn.cursor()
        res = func(cur, *args, **kwargs)
        cur.close()
        conn.close()
        return res
    return wrapper

@app.route('/book_search/choose', methods=('GET', 'POST'))
def choose():
    if request.method == 'POST':
        title = request.form['title']
        authors = request.form['authors']
        isbn = request.form['isbn']

        return redirect(url_for('search_get', title=title, authors=authors, isbn=isbn))

    return render_template('choose.html')


@app.route('/book_search/all')
@config_db
def all_get(cur):
    cur.execute('select * from works')
    works = cur.fetchall()

    return render_template('index.html', books=works)


@app.route('/book_search/search_result/')
@config_db
def search_get(cur):
    title = request.args['title']
    authors = request.args['authors']
    isbn = request.args['isbn']

    if title and authors:
        cur.execute("select * from works WHERE LOWER(title) LIKE LOWER(%s) ESCAPE '' AND authors LIKE %s ESCAPE ''", ('%' + title + '%', '%' + authors + '%',))
    elif title:
        cur.execute("select * from works WHERE LOWER(title) LIKE LOWER(%s) ESCAPE ''", ('%' + title + '%',))
    elif authors:
        cur.execute("select * from works WHERE authors LIKE %s ESCAPE ''", ('%' + authors + '%',))
    elif isbn:
        cur.execute('select * from works where isbn=\'{}\';'.format(isbn))

    try:
        works = cur.fetchall()
        if works:
            return render_template('index.html', books=works)
        else:
            return render_template('no_result.html')

    except:
        return render_template('error.html')
