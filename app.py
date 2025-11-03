from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import random

app = Flask(__name__)

EXCEL_FILE = "users.xlsx"

# --- Create Excel if not exists ---
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=["Name", "Email", "Password", "Address", "Hospital", "Date", "Status"])
    df.to_excel(EXCEL_FILE, index=False)


@app.route('/')
def home():
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']

        hospitals = ['CityCare Hospital', 'GreenLife Clinic', 'Metro Health Center']
        hospital = random.choice(hospitals)

        df = pd.read_excel(EXCEL_FILE)
        new_user = pd.DataFrame([[name, email, password, address, hospital, "Not Selected", "Pending"]],
                                columns=df.columns)
        df = pd.concat([df, new_user], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        return redirect(url_for('home'))
    return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    df = pd.read_excel(EXCEL_FILE)
    user = df[(df['Email'] == email) & (df['Password'] == password)]

    if not user.empty:
        name = user.iloc[0]['Name']
        hospital = user.iloc[0]['Hospital']
        date = user.iloc[0]['Date']
        status = user.iloc[0]['Status']
        return render_template('dashboard.html', name=name, hospital=hospital, date=date, status=status)
    else:
        return "Invalid credentials. <a href='/'>Try again</a>"


@app.route('/admin')
def admin_panel():
    df = pd.read_excel(EXCEL_FILE)
    return render_template('admin_panel.html', tables=df.to_html(index=False))


@app.route('/update_status', methods=['POST'])
def update_status():
    email = request.form['email']
    new_status = request.form['status']

    df = pd.read_excel(EXCEL_FILE)
    df.loc[df['Email'] == email, 'Status'] = new_status
    df.to_excel(EXCEL_FILE, index=False)
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.run(debug=True)
