# Importing flask utilities for pages
from flask import Flask, render_template, request, Markup, redirect, url_for, flash, jsonify

# Importing Structures for Registration and Login Forms
from form import Registration
from login import Login

# Importing mysql
from flask_mysqldb import MySQL

from flaskwebgui import FlaskUI

# Importing utilities for fetching document page numbers
import os
import PyPDF2
from win32com.client import Dispatch
import pythoncom

# Importing other utilities
import datetime
import subprocess
import csv
import json
import random


app = Flask(__name__)

ui = FlaskUI(app)

# Secret Key for forms
app.config['SECRET_KEY'] = '2314552c4105b7962aea79e24786c762'


# configuring database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Prathmesh@15'
app.config['MYSQL_DB'] = 'printer'

mysql = MySQL(app)

# Setting path for file operations
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


# Lists for capturing data of students throughout the process
data = []  # main list which would be used for displaying student_page
grp_prnt = []  # fetches individual data and appends data in main list
grp_id = []  # fetching just the grp_id
no_of_documents = 0  # Number of documents printed today initially 0
lab = [1, 2, 3, 4, 5, 6, 7]  # For Number of Labs

# Lists for getting csv data for each particular Lab
list1 = []  # LAB1
list2 = []  # LAB2
list3 = []  # LAB3
list4 = []  # LAB4
list5 = []  # LAB5
list6 = []  # LAB6
list7 = []  # LAB7
val = []
# for showing count of print documents of each lab
files = [0, 0, 0, 0, 0, 0, 0]


@app.route("/End")
def app_end():
    return render_template("end_page.html")


# Function to perform send operation n student_page
@app.route('/background_process_test')
def test():

    global data
    csv_name = APP_ROOT + '/files/LAB1.csv'
    # Creating Header of csv
    with open(csv_name, 'a', newline='') as csvfile:
        fieldnames = ['DateTime', 'Group ID',
                      'Document Name', 'No of Pages', 'Copies', 'Total']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    # Inserting values in csv
    for i in data:

        if(i[4] != 'Rejected'):

            Total = i[2] * i[3]
            
            with open(csv_name, 'a', newline='') as csvfile:
                fieldnames = ['DateTime', 'Group ID',
                              'Document Name', 'No of Pages', 'Copies', 'Total']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(
                    {'DateTime': i[5], 'Group ID': i[0], 'Document Name': i[1], 'No of Pages': i[2], 'Copies': i[3], 'Total': Total})

    filename = "\send.bat"
    target = APP_ROOT + filename

    subprocess.call([target])
    print("hello")
    return render_template("end_page.html")

# Redirects to student_page
@app.route("/student_page")
def student_page():

    global data
    return render_template("print_upload.html", posts=data)

# Fetching pdf page number


def page_pdf(filename):
    pdfobj = open(filename, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfobj)
    count = pdfReader.getNumPages()
    pdfobj.close()
    return count

# Fetching doc page number


def page_doc(name):
    pythoncom.CoInitialize()  # for threading the process
    word = Dispatch('Word.Application')
    word.Visible = False
    doc = word.Documents.Open(name)
    doc.Repaginate()
    num_of_sheets = doc.ComputeStatistics(2)
    doc.Close()
    word.Quit()
    return num_of_sheets


# For checking the limits and allowing on its basis
def validation(filename, target, copy):

    global grp_prnt
    global grp_id

    copy = int(copy)
    filename = filename
    count = 0
    if(filename[-3:] == "pdf"):
        name = target
        count = page_pdf(name)

    elif(filename[-3:] == "doc"):
        name = target
        count = page_doc(name)

    else:
        name = target
        count = page_doc(name)

    x = datetime.datetime.now()
    a = x.strftime("%A")
    if(a == "Monday"):
        day = "monday"

    elif(a == "Tuesday"):
        day = "tuesday"

    elif(a == "Wednesday"):
        day = "wednesday"

    elif(a == "Thursday"):
        day = "thursday"

    elif(a == "Friday"):
        day = "friday"

    cur = mysql.connection.cursor()
    query = "SELECT " + day + \
        ",week FROM daily WHERE grp_id = '" + str(grp_id[0]) + "' ;"

    cur.execute(query)
    week_data = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    grp_prnt.append(count)
    grp_prnt.append(copy)

    total = count * copy

    # Returns True if print pages within the limit
    if((total + week_data[0][0]) <= 20 and (total + week_data[0][1]) <= 45):
        # First condition checks for today's usage and checks limit
        # Second condition checks for weekly count and checks limit
        return True

    return False


def name_validation(files):

    global grp_id
    test = grp_id[0]
    # Validate the name by slicing
    if(test[:9] == files[:9]):
        return True
    return False


# Redirects to upload page
@app.route("/upload", methods=['GET', 'POST'])
def upload():

    global grp_prnt
    global data
    global grp_id

    file_list = []
    if request.method == 'POST':

        # Gets the number of copies and converts it into list
        copies = str(request.form['copies'])
        copies = copies.split(',')

        target = os.path.join(APP_ROOT, "files\\")

        if not os.path.isdir(target):
            os.mkdir(target)

        i = 0  # i is used to iterate the copies list
        for files in request.files.getlist("file"):
            temp_list = []
            filename = files.filename
            destination = "\\".join([target, filename])
            files.save(destination)
            temp_list.append(filename)

            grp_prnt.append(filename)

            if(not validation(filename, destination, copies[i])):
                temp_list.append('Rejected')
                grp_prnt.append('Rejected')
            else:
                if(name_validation(filename)):
                    temp_list.append('Accepted')
                    grp_prnt.append('Accepted')

                else:
                    temp_list.append('Rejected')
                    grp_prnt.append('Rejected')

            # Entering Date Time
            now = datetime.datetime.now()
            dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
            grp_prnt.append(dt_string)

            if(i < len(copies)):

                data.append(grp_prnt[:])

                grp_prnt.clear()
                grp_prnt.append(grp_id[0])

            i += 1
            file_list.append(temp_list)
        for i in file_list:
            if(i[1] == "Rejected"):
                # Removes the documents from the file which are Rejected
                os.remove(target + "/" + i[0])

        # Clears the temporary lists so that new data can be appended
        grp_prnt.clear()
        grp_id.clear()
        return redirect(url_for('student_page'))

    return render_template("upload_file.html")

# Redirects to Registration Form
@app.route("/Student_Reg", methods=["GET", "POST"])
def reg():
    form = Registration()
    if request.method == 'POST':

        if form.validate_on_submit():

            s1_name = form.s1name.data
            s2_name = form.s2name.data
            s3_name = form.s3name.data
            roll_no1 = form.roll_no1.data
            roll_no2 = form.roll_no2.data
            roll_no3 = form.roll_no3.data
            year = form.year.data
            batch = form.batch.data
            sem = form.sem.data
            pwd = form.password.data

            # Establishes connection
            cur = mysql.connection.cursor()
            cur.execute("SELECT year FROM students")
            check_year = cur.fetchall()
            mysql.connection.commit()
            count = 0

            # Used to check the total number of grp_id of a year and create a new grp_id
            for i in check_year:
                if(i[0] == year):
                    count += 1

            count += 1

            if(count < 10):
                new_count = "0" + str(count)

            grp_id = year + '0' + str(sem) + '_0' + str(batch) + new_count

            flash("Account created successfully. Your group id is %s" % (grp_id))

            now = datetime.datetime.now()
            dt_string = now.strftime("%Y-%m-%d %H:%M:%S")

            # Inserts group details in database (table: students)
            cur.execute("INSERT INTO students(grp_id,first_name,second_name,third_name,roll_1,roll_2,roll_3,year,sem,batch,password,reg_date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (grp_id, s1_name, s2_name, s3_name, roll_no1, roll_no2, roll_no3, year, sem, batch, pwd, dt_string))
            mysql.connection.commit()

            # Inserts grp into database (table: daily)
            cur.execute(
                "INSERT INTO daily(grp_id,monday,tuesday,wednesday,thursday,friday,week)VALUES(%s,%s,%s,%s,%s,%s,%s)", (grp_id, 0, 0, 0, 0, 0, 0))
            mysql.connection.commit()

            # Inserts grp into database (table: week)
            cur.execute(
                "INSERT INTO week(grp_id,week1,week2,week3,week4,week5,week6,week7,week8,week9,week10,week11,week12,week13,week14,week15)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (grp_id, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('login_page'))
    return render_template("student_reg.html", form=form)


@app.route("/admin_homepage")
def admin_home():

    global list1
    global list2
    global list3
    global list4
    global list5
    global list6
    global list7
    global files

    # Fetching csv files of all 7 labs which contains essential details for printing
    with open('LAB1.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        list1 = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            list1.append({'DateTime': row["DateTime"], 'Group_ID': row["Group ID"], 'D_Name': row["Document Name"],
                          'Pages': row["No of Pages"], 'Copies': row["Copies"], 'Total': row["Total"]})
            line_count += 1
        line_count -= 1
        files[0] = line_count

    with open('LAB2.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        list2 = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            list2.append({'DateTime': row["DateTime"], 'Group_ID': row["Group ID"], 'D_Name': row["Document Name"],
                          'Pages': row["No of Pages"], 'Copies': row["Copies"], 'Total': row["Total"]})
            line_count += 1
        line_count -= 1
        files[1] = line_count

    with open('LAB3.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        list3 = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            list3.append({'DateTime': row["DateTime"], 'Group_ID': row["Group ID"], 'D_Name': row["Document Name"],
                          'Pages': row["No of Pages"], 'Copies': row["Copies"], 'Total': row["Total"]})
            line_count += 1
        line_count -= 1
        files[2] = line_count

    with open('LAB4.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        list4 = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            list4.append({'DateTime': row["DateTime"], 'Group_ID': row["Group ID"], 'D_Name': row["Document Name"],
                          'Pages': row["No of Pages"], 'Copies': row["Copies"], 'Total': row["Total"]})
            line_count += 1
        line_count -= 1
        files[3] = line_count

    with open('LAB5.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        list5 = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            list5.append({'DateTime': row["DateTime"], 'Group_ID': row["Group ID"], 'D_Name': row["Document Name"],
                          'Pages': row["No of Pages"], 'Copies': row["Copies"], 'Total': row["Total"]})
            line_count += 1
        line_count -= 1
        files[4] = line_count

    with open('LAB6.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        list6 = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            list6.append({'DateTime': row["DateTime"], 'Group_ID': row["Group ID"], 'D_Name': row["Document Name"],
                          'Pages': row["No of Pages"], 'Copies': row["Copies"], 'Total': row["Total"]})
            line_count += 1
        line_count -= 1
        files[5] = line_count

    with open('LAB7.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        list7 = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            list7.append({'DateTime': row["DateTime"], 'Group_ID': row["Group ID"], 'D_Name': row["Document Name"],
                          'Pages': row["No of Pages"], 'Copies': row["Copies"], 'Total': row["Total"]})
            line_count += 1
        line_count -= 1
        files[6] = line_count

    return render_template('admin_homepage.html', template_folder='templates', static_folder='static', list1=list1, list2=list2, list3=list3, list4=list4, list5=list5, list6=list6, list7=list7,  result=line_count)


@app.route("/admin_group")
def admin_groupdetails():

    # Displaying group details to the admin
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    list1 = []
    for i in data:
        roll = str(i[4]) + ", " + str(i[5]) + ", " + str(i[6])
        date = str(i[11])
        list1.append({'DateTime': date[:-3], 'Group_ID': i[0], 's1name': i[1],
                      's2name': i[2], 's3name': i[3], 'Roll': roll, 'Sem': i[8], 'Batch': i[9]})

    return render_template('admin_groupdetails.html', template_folder='templates', static_folder='static', posts=list1)


@app.route("/admin_print")
def admin_printdetails():

    # Fetching database (table: daily, week)
    # Displaying current week's printing details of each individual
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM daily")
    daily = cur.fetchall()
    mysql.connection.commit()

    list1 = []
    for i in daily:

        list1.append({'Group_ID': i[0], 'Monday': i[1], 'Tuesday': i[2],
                      'Wednesday': i[3], 'Thursday': i[4], 'Friday': i[5], 'Week': i[6]})

    # Displaying all week's printing details of each individual
    cur.execute("SELECT * FROM week")
    weekly = cur.fetchall()
    mysql.connection.commit()
    cur.close()

    list2 = []
    for i in weekly:
        list2.append({'Group_ID': i[0], 'week1': i[1], 'week2': i[2], 'week3': i[3], 'week4': i[4], 'week5': i[5], 'week6': i[6], 'week7': i[7],
                      'week8': i[8], 'week9': i[9], 'week10': i[10], 'week11': i[11], 'week12': i[12], 'week13': i[13], 'week14': i[14], 'week15': i[15]})

    return render_template('admin_printdetails.html', template_folder='templates', static_folder='static', posts=list1, weekly=list2)


@app.route('/weekwise')
def weekwise():

    # Passing values of each week's total count to the dashboard
    results = []
    cur = mysql.connection.cursor()
    query = "SELECT SUM( week1 ), SUM( week2 ), SUM( week3 ), SUM( week4 ), SUM( week5 ), SUM( week6 ), SUM( week7 ), SUM( week8 ), SUM( week9 ), SUM( week10 ), SUM( week11 ), SUM( week12 ), SUM( week13 ), SUM( week14 ), SUM( week15 ) FROM week;"
    cur.execute(query)
    all_week = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    # pass values for line chart- weekwise pages

    for i in range(0, 15):
        results.append(int(all_week[0][i]))

    return jsonify({'results': results})


@app.route('/batchwise')
def batchwise():

    oddsem = [7, 8, 9, 10, 11]
    evensem = [1, 2, 3, 4, 5]
    info = []

    month = datetime.datetime.now().month

    cur = mysql.connection.cursor()

    if(month in evensem):
        # SECOND YEAR

        for i in range(1, 4):

            query = "SELECT COUNT(s.grp_id) FROM students s LEFT JOIN daily d USING(grp_id) WHERE s.year = 'SE' AND MOD(s.sem,2) = 0 AND s.batch = '" + str(i) + "';"
            cur.execute(query)
            se_details = cur.fetchall()
            mysql.connection.commit()
            info.append(se_details[0][0])

        # THIRD YEAR

        for i in range(1, 4):

            query = "SELECT COUNT(s.grp_id) FROM students s LEFT JOIN daily d USING(grp_id) WHERE s.year = 'TE' AND MOD(s.sem,2) = 0 AND s.batch = '" + str(i) + "';"
            cur.execute(query)
            te_details = cur.fetchall()
            mysql.connection.commit()
            info.append(te_details[0][0])

        # FOURTH YEAR

        for i in range(1, 4):

            query = "SELECT COUNT(s.grp_id) FROM students s LEFT JOIN daily d USING(grp_id) WHERE s.year = 'FE' AND MOD(s.sem,2) = 0 AND s.batch = '" + str(i) + "';"
            cur.execute(query)
            fe_details = cur.fetchall()
            mysql.connection.commit()
            info.append(fe_details[0][0])

    elif(month in oddsem):

        # SECOND YEAR
        for i in range(1, 4):

            query = "SELECT COUNT(s.grp_id) FROM students s LEFT JOIN daily d USING(grp_id) WHERE s.year = 'SE' AND MOD(s.sem,2) <> 0 AND s.batch = '" + str(i) + "';"
            cur.execute(query)
            se_details = cur.fetchall()
            mysql.connection.commit()
            info.append(se_details[0][0])

        # THIRD YEAR

        for i in range(1, 4):

            query = "SELECT COUNT(s.grp_id) FROM students s LEFT JOIN daily d USING(grp_id) WHERE s.year = 'TE' AND MOD(s.sem,2) <> 0 AND s.batch = '" + str(i) + "';"
            cur.execute(query)
            te_details = cur.fetchall()
            mysql.connection.commit()
            info.append(te_details[0][0])

        # FOURTH YEAR

        for i in range(1, 4):

            query = "SELECT COUNT(s.grp_id) FROM students s LEFT JOIN daily d USING(grp_id) WHERE s.year = 'FE' AND MOD(s.sem,2) <> 0 AND s.batch = '" + str(i) + "';"
            cur.execute(query)
            fe_details = cur.fetchall()
            mysql.connection.commit()
            info.append(fe_details[0][0])

        cur.close()

    # pass value for bar graph = batchwise pages

    return jsonify({'info': info})


@app.route("/dashboard")
def admin_dashboard():

    # Fetching all the data for cards in dashboard
    global no_of_documents

    card_details = []  # Storing values of cards in this list

    # Fetching number of registered users
    cur = mysql.connection.cursor()
    cur.execute("SELECT grp_id FROM students")
    id_details = cur.fetchall()
    mysql.connection.commit()

    count = 0

    for i in id_details:
        count += 1

    card_details.append(count)

    # Fetching today's total print count
    x = datetime.datetime.now()
    a = x.strftime("%A")
    if(a == "Monday"):
        day = "monday"

    elif(a == "Tuesday"):
        day = "tuesday"

    elif(a == "Wednesday"):
        day = "wednesday"

    elif(a == "Thursday"):
        day = "thursday"

    elif(a == "Friday"):
        day = "friday"

    query = "SELECT SUM( " + day + " ), SUM(week) FROM daily;"
    cur.execute(query)
    sum = cur.fetchall()
    mysql.connection.commit()

    card_details.append(sum[0][0])

    # Fetching  total print count till date
    query = "SELECT SUM( week1 ), SUM( week2 ), SUM( week3 ), SUM( week4 ), SUM( week5 ), SUM( week6 ), SUM( week7 ), SUM( week8 ), SUM( week9 ), SUM( week10 ), SUM( week11 ), SUM( week12 ), SUM( week13 ), SUM( week14 ), SUM( week15 ) FROM week;"
    cur.execute(query)
    all_week = cur.fetchall()
    mysql.connection.commit()

    card_details.append(no_of_documents)

    # Fetching today's number of document printed
    total_prints = sum[0][1]
    for i in range(0, 15):
        total_prints += all_week[0][i]

    card_details.append(total_prints)

    cur.close()
    return render_template('dashboard.html', template_folder='templates', static_folder='static', lab=lab, files=files, card_details=card_details)


@app.route("/dashboard", methods=["POST", "GET"])
def getit():

    # Logic for checklist in dashboard page
    global val
    if request.method == 'POST':
        val = request.form.getlist('delBox')
    print(val)
    for i in val:
        i = int(i)
        files[i-1] = 0
    return redirect(url_for('admin_dashboard'))


@app.route("/fetching_records")
def fetch_records():

    global no_of_documents

    # Calling powershell script for Print Job Details
    process = subprocess.Popen(
        ["powershell", "E:\\printer.ps1"], stdout=subprocess.PIPE)
    result1 = process.communicate()
    result1 = str(result1[0])

    # Calling powershell script for Print Job Details-Copies
    process = subprocess.Popen(
        ["powershell", "E:\\printer_copies.ps1"], stdout=subprocess.PIPE)
    result2 = process.communicate()
    result2 = str(result2[0])

    list1 = []
    list3 = []
    list2 = []
    list4 = []
    data = []

    list1.append(result1.split("@{"))
    list2.append(result2.split("@{"))

    for i in range(1, len(list1[0])):

        no_of_documents += 1

        name = []
        page = []
        copies = []
        list3.append(list1[0][i].split(";"))  # Inserting Pages
        list4.append(list2[0][i].split(";"))  # Inserting Copies

        # For document Name
        doc_name = list3[0][2]
        if(doc_name[9:23] == "Microsoft Word"):
            # For Word document
            name.append(doc_name[26:35])
        else:
            # For PDF document
            name.append(doc_name[9:18])

        # For page number
        doc_page = list3[0][0]
        page.append(doc_page[10:])

        # For copies
        doc_copy = list4[0][0]
        if(doc_copy[8] == "}"):
            copies.append(doc_copy[7])
        else:
            copies.append(doc_copy[7:9])

        data.append({'D_Name': name[0], 'Page': page[0], 'Copies': copies[0]})
        list3.clear()
        list4.clear()

    # Finding day at which entry is to be done
    x = datetime.datetime.now()
    a = x.strftime("%A")
    if(a == "Monday"):
        day = "monday"
        value = 1
    elif(a == "Tuesday"):
        day = "tuesday"
        value = 2
    elif(a == "Wednesday"):
        day = "wednesday"
        value = 3
    elif(a == "Thursday"):
        day = "thursday"
        value = 4
    elif(a == "Friday"):
        day = "friday"
        value = 5

    for i in data:

        # Fetching the databse for getting prev values and adding it with print job details to create new values
        cur = mysql.connection.cursor()
        query = "SELECT " + day + " FROM daily WHERE grp_id = '" + \
            i['D_Name'] + "' ;"  # change it to D_Name
        cur.execute(query)
        prev_prints = cur.fetchall()
        mysql.connection.commit()

        total = int(i['Page']) * int(i['Copies']) + prev_prints[0][0]

        # Updation of database with new values (table : daily)
        query = "UPDATE daily SET " + day + " = '" + \
            str(total) + "' WHERE grp_id = '" + \
            i['D_Name'] + "' ;"  # change it to D_Name

        cur.execute(query)
        mysql.connection.commit()

        # Fetching prev days data from current day to monday and adding them to get till dates count
        query = "SELECT * FROM daily WHERE grp_id = '" + \
            i['D_Name'] + "' ;"  # change it to D_Name
        cur.execute(query)
        all_week = cur.fetchall()
        mysql.connection.commit()
        week_data = 0

        for j in range(value, 0, -1):

            week_data += all_week[0][j]

        # Updation of database for week (table: daily)
        query = "UPDATE daily SET week = '" + \
            str(week_data) + "' WHERE grp_id = '" + \
            i['D_Name'] + "' ;"  # change it to D_Name

        cur.execute(query)
        mysql.connection.commit()
        cur.close()

    return redirect(url_for('admin_home'))


@app.route("/new_week")
def new_week():

    # Takes data from database (table: week)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM week;")
    data = cur.fetchall()
    count = len(data)  # counts the length
    mysql.connection.commit()

    # Just a random checking of top 20 entries weekly value in each week
    if(count >= 20):
        end = 20
    else:
        end = count

    index = 0
    # Logic for getting the next week
    for i in range(1, 16):
        for j in range(0, end):
            if(data[j][i] != 0):
                index += 1
                break
        if(index < i):
            index += 1
            break

    cur.execute("SELECT grp_id, week FROM daily;")
    week_data = cur.fetchall()

    mysql.connection.commit()

    # Insertion of value in that week
    for i in range(0, count):

        query = "UPDATE week SET week" + str(index) + " = " + \
            str(week_data[i][1]) + " WHERE grp_id = '" + \
            week_data[i][0] + "' ;"

        cur.execute(query)
        mysql.connection.commit()

    cur.execute(
        "UPDATE daily SET monday = 0, tuesday = 0, wednesday = 0, thursday = 0, friday = 0, week = 0;")
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('admin_home'))


@app.route("/", methods=["GET", "POST"])
def login_page():

    global grp_prnt
    global grp_id

    login = Login()
    if request.method == 'POST':
        if login.validate_on_submit():

            # Getting values from database (tables: students,admin)
            # student Database
            cur = mysql.connection.cursor()
            cur.execute("SELECT grp_id,password FROM students")
            student_details = cur.fetchall()
            mysql.connection.commit()

            # admin Database
            cur.execute("SELECT * FROM admin")
            admin_details = cur.fetchall()
            mysql.connection.commit()
            cur.close()

            # Checks whether the credentials are of admin
            if(login.username.data == admin_details[0][0] and login.password.data == admin_details[0][1]):
                return redirect(url_for('admin_home'))
            else:

                # Checks whether the credentials are of students
                for i in student_details:
                    if(i[0] == login.username.data):

                        # If grp_id matches checks for password
                        if(i[1] == login.password.data):

                            # If both matches then appends the grp_id in temporary lists
                            grp_prnt.append(login.username.data)
                            grp_id.append(login.username.data)
                            return redirect(url_for('upload'))
                # If credentials are wrong
                flash('INVALID CREDENTIALS')

    return render_template("login_page.html", login=login)


if __name__ == "__main__":
    ui.run()
