from flask import render_template, flash, redirect
from app import app, db
from app.forms import LoginForm
from app.models import Course, Files

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Mati'}
    courses = Course.query.all()
    return render_template('index.html', title='Dashboard', courses=courses)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/course/<coursename>')
def course(coursename):
    course = Course.query.filter_by(coursename=coursename).first_or_404()
    course_id = course.id
    files = Files.query.filter_by(course_id=course_id)
    return render_template('course.html', course=course, files=files)