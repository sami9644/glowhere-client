import uuid
import pymysql
from werkzeug.security import check_password_hash,generate_password_hash

def db():
    conn = pymysql.connect(host='sql.freedb.tech',password='KW7q$ctWygGn%X8',user='freedb_glowuser',database='freedb_Glowheredb')
    return conn

def uniqueid():
    user_id = uuid.uuid4()
    user_id = str(user_id).replace("-","")
    return user_id

def signup(fullname,username,email,password):
    conn = db()
    cur = conn.cursor()
    userid = uniqueid()
    cur.execute("INSERT INTO users(userid,fullname,username,email,password) VALUES (%s,%s,%s,%s,%s)",
                    (userid,fullname,username,email,generate_password_hash(password)))
    conn.commit()
    cur.close()
    conn.close()

def login(username,password):
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s",(username))
    data = cur.fetchone()
    cur.close()
    conn.close()
    if data:
        hashedpassword = data[4]
        if check_password_hash(hashedpassword,password) and (data[5] == 'false'):
            return data
        else:
            return False
    else:
        return False
    
def userinfo(userid):
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE userid = %s",(userid))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data

def services():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM services")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def isbooked(serviceid,userid):
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM booking WHERE service = %s AND bookedby =%s",(serviceid,userid,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data

def bookservice(service,bookedby,bookedon,bookedfor):
    conn = db()
    cur = conn.cursor()
    cur.execute("INSERT INTO booking(bookingid,service,bookedby,bookedon,bookedfor) VALUES(%s,%s,%s,%s,%s)",(uniqueid(),service,bookedby,bookedon,bookedfor))
    conn.commit()
    cur.close()
    conn.close()   

def mybookings(userid):
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM booking WHERE bookedby = %s",(userid))
    bookinglist = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return bookinglist

def serviceinfo(serviceid):
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM services WHERE serviceid = %s",(serviceid))
    info = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return info