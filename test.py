from flask import Flask, render_template, request, session, redirect
import pymysql

app = Flask(__name__)

# Configure the database connection
db = pymysql.connect(host='localhost',
                     user='root',
                     password='',
                     db='book_recommend')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    username=request.form.get('username')
    password=request.form.get('password')
    return "the username is {} and the passworsd is{}". format(username,password)

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