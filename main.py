from flask import Flask, render_template, redirect, session, url_for, request
import pymysql.cursors
import mysql.connector
from datetime import date, datetime
import smtplib
from flask_mail import Mail, Message

"""connection = pymysql.connect(host='localhost',
                             user='root',
                             password='mehdi786',
                             db='acmhack',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)"""
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mehdi786",
  database="acmhack"
)

ta = 0.0
ma = 0.0
hra = 0.0

app = Flask(__name__)
app.secret_key = 'myscrtkey'


@app.route('/', methods=['POST', 'GET'])
def index():
    if 'fname' in session:
        return redirect(url_for('employee'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM `users` WHERE `email`=%s and `password`=%s", (email, password))
        myresult = mycursor.fetchone()
        if myresult != None:
            session['fname'] = myresult[1]
            session['id'] = myresult[0]
            session['accnumber'] = myresult[-2]
            mycursor.execute("SELECT att FROM attendance WHERE id=%s", (session['id'],))
            myresult = mycursor.fetchone()
            if myresult != None:
                if (myresult[0].year != datetime.now().year and myresult[0].month != datetime.now().month and myresult[0].day != datetime.now().day):
                    mycursor.execute("INSERT INTO attendance(id, fname, att, atime) VALUES(%s,%s,%s,%s)", (myresult[0], myresult[1], date(datetime.now().year, datetime.now().month, datetime.now().day), datetime.now().strftime("%H:%M")))

                    mydb.commit()
            else:
                mycursor.execute("INSERT INTO attendance(id, fname, att, atime) VALUES(%s,%s,%s,%s)", (session['id'], session['fname'], date(datetime.now().year, datetime.now().month, datetime.now().day), datetime.now().strftime("%H:%M")))

                mydb.commit()
            return redirect(url_for('employee'))
        else:
            pass
    return render_template('index.html')

@app.route('/admin')
def admin():
    if 'ausername' not in session:
        return redirect(url_for('adminlogin'))
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM users")
    myresult = mycursor.fetchall()
    return render_template('admindashboard.html', allemp = myresult)


@app.route('/leavetrac', methods=['POST', 'GET'])
def leavetrac():
    if 'ausername' not in session:
        return redirect(url_for('adminlogin'))
    if request.method == "POST":
        if 'Approve' in request.form:
            print('Ye log itna kyu bol rahe hain!')
            # creates SMTP session 
            s = smtplib.SMTP('smtp.gmail.com', 587) 
            
            # start TLS for security 
            s.starttls() 
            
            # Authentication 
            s.login("wimpycat714@gmail.com", "temppassword123") 
            
            # message to be sent 
            message = 'Subject: {}\n\n{}'.format("Leave Approval", "Your leave has been approved.")
            
            # sending the mail 
            s.sendmail("wimpycat714@gmail.com", "mehdi.patel@gmail.com", message) 
            
            # terminating the session 
            s.quit()

        elif 'Disapprove' in request.form:
            print('Ye log itna kyu bol rahe hain part2!')
            # creates SMTP session 
            s = smtplib.SMTP('smtp.gmail.com', 587) 
            
            # start TLS for security 
            s.starttls() 
            
            # Authentication 
            s.login("wimpycat714@gmail.com", "temppassword123") 
            
            # message to be sent 
            message = 'Subject: {}\n\n{}'.format("Leave Disapproval", "Sorry! Your leave has not been approved.")
            
            # sending the mail 
            s.sendmail("wimpycat714@gmail.com", "mehdi.patel@gmail.com", message) 
            
            # terminating the session 
            s.quit()
        r_id = request.form['r_id']
        mycursor = mydb.cursor()
        sql = "DELETE FROM emp_leave WHERE id = %s"
        mycursor.execute(sql, (r_id,))
        mydb.commit()
        return redirect(url_for('leavetrac'))

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM emp_leave")
    myresult = mycursor.fetchall()

    return render_template('leavetrac.html', leaves=myresult)

@app.route('/meetingconf', methods=['POST', 'GET'])
def meetingconf():
    if 'ausername' not in session:
        return redirect(url_for('adminlogin'))
    if request.method == "POST":
        if 'Confirm' in request.form:
            cname = request.form['cname']
            cpname = request.form['cpname']
            name = request.form['name']
            mycursor = mydb.cursor()
            mycursor.execute("UPDATE meetings SET aon = 'approved' WHERE companyname = %s and clientname = %s and name = %s", (cpname, cname, name))
            mydb.commit()

        elif 'Dismiss' in request.form:
            mycursor = mydb.cursor()
            mycursor.execute("DELETE from meetings WHERE companyname = %s and clientname = %s and name = %s", (cpname, cname, name))
            mydb.commit()
        

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM meetings WHERE aon='disapproved' ")
    myresult = mycursor.fetchall()

    return render_template('meetingconf.html', meetings=myresult)
    

@app.route('/attendance')
def attendance():
    if 'ausername' not in session:
        return redirect(url_for('adminlogin'))
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM attendance")
    alist = mycursor.fetchall()
    return render_template('attendance.html', alist=alist)


@app.route('/admindashboard')
def admindashboard():
    if 'ausername' not in session:
        return redirect(url_for('adminlogin'))
    return render_template('admindashboard.html')

@app.route('/emp_dash')
def emp_dash():
    if 'id' not in session:
        return redirect(url_for('index'))
    return render_template('emp_dash.html')

@app.route('/remburs', methods=['GET', 'POST'])
def remburs():
    if 'ausername' not in session:
        return redirect(url_for('adminlogin'))
    if request.method == "POST":
        if 'Allow' in request.form:
            print('Ye log itna kyu bol rahe hain!')
            # creates SMTP session 
            s = smtplib.SMTP('smtp.gmail.com', 587) 
            
            # start TLS for security 
            s.starttls() 
            
            # Authentication 
            s.login("wimpycat714@gmail.com", "temppassword123") 
            
            # message to be sent 
            message = 'Subject: {}\n\n{}'.format("Reimbursement Approval", "Your request for reimbursement has been approved.")
            
            # sending the mail 
            s.sendmail("wimpycat714@gmail.com", "mehdi.patel@gmail.com", message) 
            
            # terminating the session 
            s.quit()

        elif 'Disallow' in request.form:
            print('Ye log itna kyu bol rahe hain part2!')
            # creates SMTP session 
            s = smtplib.SMTP('smtp.gmail.com', 587) 
            
            # start TLS for security 
            s.starttls() 
            
            # Authentication 
            s.login("wimpycat714@gmail.com", "temppassword123") 
            
            # message to be sent 
            message = 'Subject: {}\n\n{}'.format("Reimbursement Disapproval", "Sorry! Your request for reimbursement has been rejected.")
            
            # sending the mail 
            s.sendmail("wimpycat714@gmail.com", "mehdi.patel@gmail.com", message) 
            
            # terminating the session 
            s.quit()
        rid = request.form['rid']
        mycursor = mydb.cursor()
        sql = "DELETE FROM reim WHERE id = %s"
        mycursor.execute(sql, (rid,))
        mydb.commit()
        return redirect(url_for('remburs'))

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM reim")
    myresult = mycursor.fetchall()
    print(myresult)
    return render_template('remburs.html', rembers=myresult)

@app.route('/hostmeets', methods=['POST', 'GET'])
def hostmeets():
    if 'ausername' not in session:
        return redirect(url_for('adminlogin'))
    if request.method == 'POST':
        empidname = request.form['empidname']
        meeting_date = request.form['meeting_date']
        cpname = request.form['cpname']
        cname = request.form['cname']
        idx = empidname.index(" ")
        id_ = empidname[:idx]
        name = empidname[idx+1:]
        mycursor = mydb.cursor()
        sql = "INSERT INTO meetings VALUES (%s,%s,%s,%s,%s, %s)"
        val = (id_, cpname, cname, date(int(meeting_date[:4]), int(meeting_date[5:7]), int(meeting_date[8:])), 'disapproved', name)
        mycursor.execute(sql, val)
        mydb.commit()

    mycursor = mydb.cursor()
    mycursor.execute("SELECT id, fname FROM users")
    myresult = mycursor.fetchall()
    return render_template("hostmeets.html", emplist = myresult)

@app.route('/salcalc')
def salcalc():
    if 'ausername' not in session:
        return redirect(url_for('adminlogin'))
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM salary")
    slist = mycursor.fetchall()
    l=[]
    global ta
    global ma
    global hra
    for i in slist:
        l1=list(i[:-1])
        calcsal = (i[2]/12) - ((i[2]/480) * (i[-3] + (2*i[-4]))) + i[-2] + ((i[2]*i[3])/1920) + float(ta) + float(ma) + float(hra)
        calcsal = round(calcsal, 2) 
        ta,ma,hra = 0.0,0.0,0.0
        l1.append(calcsal)
        l.append(l1)
    return render_template('salcalcshow.html', slist=l)
    #if 'ausername' not in session:
    #    return redirect(url_for('adminlogin'))
    #return render_template('salcalc.html')
@app.route('/s', methods=['POST', 'GET'])
def s():
    if 'ausername' not in session:
        return redirect(url_for('adminlogin'))
    if request.method == "POST":
        global ta
        global ma
        global hra
        ta = request.form['ta']
        ma = request.form['ma']
        hra = request.form['hra']
        return redirect(url_for('salcalc'))
    return render_template("salcalc.html")

@app.route('/salcalcshow')
def salcalcshow():
    if 'ausername' not in session:
        return redirect(url_for('adminlogin'))
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM salary")
    slist = mycursor.fetchall()
    l=[]
    ta = 4000.0
    ma = 8000.0
    for i in slist:
        l1=list(i[:-1])
        calcsal = (i[2]/12) - ((i[2]/480) * (i[-3] + (2*i[-4]))) + i[-2] + ((i[2]*i[3])/1920) + ta + ma
        calcsal = round(calcsal, 2) 
        l1.append(calcsal)
        l.append(l1)
    print(l)
    return render_template('salcalcshow.html', slist=l)

@app.route('/adminlogin', methods=['POST', 'GET'])
def adminlogin():
    if 'ausername' in session:
        return redirect(url_for('admin'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['ausername'] = username
        if username == 'admin' and password == 'admin':
            return redirect(url_for('admin'))
        else:
            pass
    return render_template('adminlogin.html')


@app.route('/leave_app',methods=['GET','POST'])
def leave_app():
    if 'fname' not in session:
        return redirect(url_for('index'))
    if request.method == "POST":
        reason = request.form['reason']
        from_date = request.form['from']
        to_date = request.form['to']

        mycursor = mydb.cursor()
        sql = "INSERT INTO emp_leave VALUES (%s,%s,%s,%s,%s)"
        val = (session['id'], session['fname'], reason, date(int(from_date[:4]), int(from_date[5:7]), int(from_date[8:])), date(int(to_date[:4]), int(to_date[5:7]), int(to_date[8:])))
        mycursor.execute(sql, val)

        mydb.commit()      
    return render_template('leave_app.html')

@app.route('/reimbursements',methods=['GET','POST'])
def reimbursements():
    if 'fname' not in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        amt=request.form['amount']
        exp_date=request.form['expenditure_date']
        mycursor = mydb.cursor()
        sql = "INSERT INTO reim VALUES (%s,%s,%s,%s)"
        val = (session['id'], session['fname'], amt, date(int(exp_date[:4]), int(exp_date[5:7]), int(exp_date[8:])))
        mycursor.execute(sql, val)

        mydb.commit()  
    return render_template('reimbursements.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'fname' in session:
        return redirect(url_for('employee'))
    if request.method == 'POST':
        fname = request.form['fname']
        mname = request.form['mname']
        lname = request.form['lname']
        dob = request.form['dob']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['cpassword']
        doj = request.form['doj']
        pnumber = request.form['pnumber']
        accnumber = request.form['accnumber']
        address = request.form['address']
        department = request.form['department']
        post = request.form['post']
        if password == cpassword and len(password) >=6:
            days_in_year = 365.2425    
            year = int(dob[:4])
            month = int(dob[5:7])
            day = int(dob[8:])
            age = int((date.today() - (date(year, month, day))).days / days_in_year)
            mycursor = mydb.cursor()
            sql = "INSERT INTO users (fname, mname, lname, email, password, age, address, post, department, dob, pnumber, accnumber, joiningdate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (fname,mname,lname,email,password,int(age),address,post, department, date(int(dob[:4]), int(dob[8:]), int(dob[5:7])), pnumber, accnumber, date(int(doj[:4]), int(doj[8:]), int(doj[5:7])))
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        else:
            return render_template('register.html', Error="Oops! Something went wrong!")
    return render_template('register.html', Error='')

@app.route('/adminlogout')
def adminlogout():
    # remove the username from the session if it is there
    session.pop('ausername', None)
    return redirect(url_for('adminlogin'))

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    mycursor = mydb.cursor()
    sql = "UPDATE attendance SET gtime = %s"
    val = (datetime.now().strftime("%H:%M"))
    mycursor.execute(sql, (val,))
    mydb.commit()
    mycursor = mydb.cursor()
    sql = "SELECT atime, gtime FROM attendance WHERE id = %s"
    mycursor.execute(sql, (session['id'],))
    myresult = mycursor.fetchone()
    h = int(myresult[1][:2]) - int(myresult[0][:2])
    h = h * 60
    m = int(myresult[1][3:]) - int(myresult[0][3:])
    m = m + h
    s = ''
    if m >= 480:
        s = 'Full Day'
    elif m<480 and m>=240:
        s = "Half Day"
    else:
        s = 'Absent'
    d = datetime.today().strftime('%Y-%m-%d')
    mycursor = mydb.cursor()
    sql = "UPDATE attendance SET td = %s where id = %s and att = %s"
    print('d: ', d)
    mycursor.execute(sql, (m, session['id'], d))
    mydb.commit()
    sql = "UPDATE attendance SET day = %s where id = %s and att = %s"
    mycursor.execute(sql, (s, session['id'], d))
    mydb.commit()
    session.pop('fname', None)
    session.pop('id', None)
    session.pop('accnumber', None)
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    if 'fname' not in session:
        return redirect(url_for('index'))
    id = session['id']
    mycursor = mydb.cursor()
    sql = "SELECT * FROM users WHERE id = %s"
    mycursor.execute(sql, (id,))
    myresult = mycursor.fetchone()
    if myresult != None:
        id = myresult[0]
        name = myresult[1]
        email = myresult[4]
        pnumber = myresult[-3]
        post = myresult[9]
    return render_template('profile.html', id=id, name=name, email=email, pnumber=pnumber, post=post)

@app.route('/employee', methods=['POST', 'GET'])
def employee():
    if 'fname' in session:
        mycursor = mydb.cursor()
        sql = "SELECT * FROM meetings WHERE id = %s and aon = 'disapproved' "
        mycursor.execute(sql, (session['id'],))
        myresult1 = mycursor.fetchall()
        mycursor = mydb.cursor()
        sql = "SELECT * FROM meetings WHERE id = %s and aon = 'approved' "
        mycursor.execute(sql, (session['id'],))
        myresult2 = mycursor.fetchall()
        return render_template('employee.html', ameetings=myresult2, dmeetings=myresult1)
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)