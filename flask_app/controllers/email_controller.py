from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template, redirect, request, session, flash
bcrypt = Bcrypt(app)
from flask_app.models import email_model
app.secret_key = 'emailvalidation'

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/check', methods=['post'])
def email_check():
    # check if email is valid email
    if not email_model.Emails.validate_email(request.form):
        return redirect('/')
    print('email checks out')
    # check if email is already in database
    if email_model.Emails.validate_user(request.form):
        print('is in database')
        return redirect('/')
    print('not in database, saving email')
    email_model.Emails.save(request.form)
    return redirect('/success')

@app.route('/success')
def success():
    emails = email_model.Emails.get_all()
    return render_template('success.html', emails = emails)

@app.route('/delete/<int:id>')
def delete_email(id):
    email_model.Emails.delete(id)
    return redirect('/success')

@app.route('/home')
def clear_sess():
    session.clear()
    return redirect('/')

@app.route('/show_emails')
def show_emails():
    session.clear()
    return redirect('/success')