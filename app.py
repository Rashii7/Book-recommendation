from flask import Flask,render_template,request, redirect, url_for
import pickle
import numpy as np
# from flask_mysqldb import MySQL
import pymysql
import pandas
import json
from flaskext.mysql import MySQL

popular_books = pickle.load(open('popular_books.pkl','rb'))
table = pickle.load(open('table.pkl','rb'))
books_brs = pickle.load(open('books_brs.pkl','rb'))
similarity_score = pickle.load(open('similarity_score.pkl','rb'))

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'book_recommend'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def login():
   return redirect(url_for('login_validation'))

@app.route('/login_validation', methods=["POST", "GET"])
def login_validation():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:


            # return json.dumps({"message":_name})

            conn = mysql.connect()

            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
            return redirect(url_for('home'))
        else:
            return 'abe ssaale'
@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html',
                           book_name = list(popular_books['Book-Title'].values),
                           author = list(popular_books['Book-Author'].values),
                           image=list(popular_books['Image-URL-M'].values),
                           votes=list(popular_books['Number of ratings'].values),
                           rating=[round(rating) for rating in popular_books['Average number of ratings'].values],
                           )



@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(table.index == user_input)[0][0]
    similar_books = sorted(list(enumerate(similarity_score[index])), key=lambda a: a[1], reverse=True)[1:6]

    data = []
    for i in similar_books:
        item = []
        temp_df = books_brs[books_brs['Book-Title'] == table.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)


    print(data)

    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
