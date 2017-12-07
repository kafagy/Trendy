import time, sys, subprocess
from flaskext.mysql import MySQL
from flask import Flask, render_template, json, request, session, redirect
from werkzeug import generate_password_hash, check_password_hash

# TODO Fix username variables email inside sign in and out
# TODO Change inside the retreival script the "delete" statements and use instead "update" statements
# TODO Use a loading bar when waiting for the retrival processes to finish
# TODO SQL getting no results after retreival
# TODO Quit the chrome browser if retreival has no errors
# TODO Clean Trendy code
# TODO Add subreddit link column to reddit table
# TODO Create an ETL script

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'abc123'
app.config['MYSQL_DATABASE_DB'] = 'trendy'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/userHome')
def userHome():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT username FROM users WHERE email = %s"
    cursor.execute(sql, useremail)
    username = cursor.fetchone()[0]
    print(username)

    procT = subprocess.Popen([sys.executable, '/Users/kafagy/PycharmProjects/Trendy/retreival/twitter.py', username])
    procF = subprocess.Popen([sys.executable, '/Users/kafagy/PycharmProjects/Trendy/retreival/facebook.py', username])
    procR = subprocess.Popen([sys.executable, '/Users/kafagy/PycharmProjects/Trendy/retreival/reddit.py', username])

    procT.wait()
    procF.wait()
    procR.wait()

    sql = "SELECT trend, link FROM twitter INNER JOIN users u ON twitter.username = u.username WHERE twitter.username = %s"
    cursor.execute(sql, username)
    twitter = cursor.fetchall()
    if not cursor.rowcount:
        print("No results found")
    else:
        print(twitter)

    sql = "SELECT trend, link , content FROM facebook INNER JOIN users u ON facebook.username = u.username WHERE facebook.username = %s"
    cursor.execute(sql, username)
    facebook = cursor.fetchall()
    if not cursor.rowcount:
        print("No results found")
    else:
        print(facebook)

    sql = "SELECT thread, link, comment, href FROM reddit INNER JOIN users u ON reddit.username = u.username WHERE reddit.username = %s"
    cursor.execute(sql, username)
    reddit = cursor.fetchall()
    if not cursor.rowcount:
        print("No results found")
    else:
        print(reddit)

    if session.get('user'):
        return render_template('userHome.html', twitter=twitter, facebook=facebook, reddit=reddit)
    else:
        return render_template('error.html', error='Unauthorized Access')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    global useremail
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        useremail = _email
        _password = request.form['inputPassword']
        if _name and _email and _password:
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                redirect('/userHome')
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


@app.route('/showSignIn')
def showSignin():
    return render_template('signin.html')


@app.route('/signIn', methods=['POST'])
def signIn():
    global useremail
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
        useremail = _username
        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin', (_username,))
        data = cursor.fetchall()
        print("username: ", data)
        if len(data) > 0:
            if check_password_hash(str(data[0][2]), _password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html', error='Wrong Email address or Password.')
        else:
            return render_template('error.html', error='Wrong Email address or Password.')
    except Exception as e:
        return render_template('error.html', error=str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(port=5000)
