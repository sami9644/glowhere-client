from flask import *
import database as db
import upload
from functools import wraps
from datetime import datetime as dt

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global nexturl
        if 'userid' not in session:
            # nexturl = request.url
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function

def convert_to_24_hour_format(time_str):
    try:
        # Parse the input time in 12-hour format
        time_obj = dt.strptime(time_str, "%I:%M %p")
        # Format it in 24-hour format
        time_24_hour = time_obj.strftime("%H:%M")
        return time_24_hour
    except ValueError:
        # If the input is not in 12-hour format, return it as is
        return time_str

def is_between_8_to_10(time_str):
    try:
        # Split the time string into hours and minutes
        hours, minutes = map(int, time_str.split(':'))
        
        # Check if the time is between 8:00 and 10:00
        if 8 <= hours <= 22:
            return True
        else:
            return False
    except ValueError:
        # If the input is not in the correct format, return False
        return False

app = Flask(__name__)
app.secret_key = "CLIENT9644"

@app.errorhandler(404)
def notfound(error):
    return render_template("notfound.html")



@app.route("/")
def home():
    if 'userid' not in session:
        return render_template("index.html")
    else:
        return redirect(f"/dashboard/{session['userid']}")

@app.route("/login")
def login():
    if 'userid' not in session:
        return render_template("login.html")
    else:
        return redirect(f"/dashboard/{session['userid']}")

@app.route("/signup")
def signUp():
    if 'userid' not in session:
        return render_template("signup.html")
    else:
        return redirect(f"/dashboard/{session['userid']}")

@app.route("/address")
def ourAddress():
    return render_template("addr.html")

@app.route("/register",methods=['POST'])
def register():
    fullname = request.form['fullname']
    username = request.form['username']
    email = request.form['email-id']
    password1 = request.form['password']
    password2 = request.form['password2']
    if password1 != password2:
        return '<script>alert("Passwords dont match!");window.location.href="/signup"</script>'
    else:
        try:
            db.signup(fullname,username,email,password1)
            return '<script>alert("successfully registered! you can now log in!");window.location.href="/login"</script>'
        except db.pymysql.IntegrityError:
            return '<script>alert("username or email already registered!");window.location.href="/signup"</script>'
        except Exception as e:
            return e
        
@app.route("/savesession",methods=['POST'])
def saveSession():
    username = request.form['username']
    password = request.form['password']
    logIn = db.login(username,password)
    if not(logIn):
        return '<script>alert("username or password incorrect!");window.location.href="/login"</script>'
    else:
        session['userid'] = logIn[0]
        return redirect(f"/dashboard/{session['userid']}")
    
@app.route("/dashboard/<userid>")
@login_required
def dashboard(userid):
    if userid == session['userid']:
        return render_template("dashboard.html",userid=userid,info=db.userinfo,services=db.services(),isbooked=db.isbooked)
    else:
        return 'access denied!',403

@app.route("/bookservice",methods=['POST'])
def bookService():
    date = request.form['bookdate']
    time = request.form['booktime']
    serviceid = request.form['serviceid']
    bookedby = session['userid']
    bookedon = f'{dt.today().year}-{dt.today().month}-{dt.today().day} {dt.now().hour}:{dt.now().minute}'
    bookedfor = f'{"-".join(date.split("-"))} {":".join(time.split(":"))}'
    if is_between_8_to_10(time) and (int(date.split("-")[0]) >= int(dt.today().year)):
        db.bookservice(serviceid,bookedby,bookedon,bookedfor)
        return '<script>alert("Service booked!");window.location.href="/"</script>'
    else:
        return '<script>alert("Booking is only allowed only for 8:00AM to 10:00AM");window.location.href="/"</script>'

@app.route('/mybookings')
@login_required
def mybooking():
    mybooking = db.mybookings(session['userid'])
    return render_template('mybooking.html',userid=session['userid'],info = db.userinfo,mybookings=mybooking,serinfo=db.serviceinfo)

@app.route('/unbook/<bookingid>')
@login_required
def unbookservice(bookingid):
    if bookingid:
        conn = db.db()
        cur = conn.cursor()
        cur.execute("DELETE FROM booking WHERE bookingid = %s",(bookingid))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(message="Service unbooked successfully!")
    else:
        return jsonify(message="Error unbooking service! try again!")

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
