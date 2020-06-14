from flask import render_template, flash, redirect, request
from app import app, db
from app.forms import LoginForm
from app.models import Course, Files
import urllib.request
import re
import os
from pathlib import Path

import random
import threading
import time


class ExportingThread(threading.Thread):
    def __init__(self):
        self.progress = 0
        super().__init__()

    def run(self):
        # Your exporting stuff goes here ...
        for _ in range(10):
            time.sleep(1)
            self.progress += 10

# Global variables

requestedRequests = set()
video_patternHD = "hls_1280x720.ts"
video_patternFHD = "hls_1920x1080.ts"
audio_pattern = "hls_aac-96k-eng.aac"
mp4_pattern = "1280x720.mp4"

# Change path below if you want save videos in different location
path_to_directory = "data2"
#directory = f"{path_to_directory}/{courseName}"

downloadingNow = "nothing"

# This has to be set manually
print("Starting index: ")
i = int(input())
coursesList = []
exporting_threads = {}

### Logic

def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')

def verbose_cls():
    clear_console()
    print("##################")
    print("Downloaded video and audio")
    print("##################")

def handle_windows_path(posix_path):
    if os.name == 'nt':
        return posix_path.replace('/', '\\')
    return posix_path

def download(url, filename):
    global downloadingNow
    # TODO add interrupted connection exception
    try:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        downloadingNow = f"{filename}"
        urllib.request.urlretrieve(url, filename)
        downloadingNow = "nothing"
        return True
    except FileNotFoundError:
        print("Destination directory doesn't exist")
        downloadingNow = "nothing"
        return False

def getCourseList():
    global coursesList
    tempList = Course.query.all()
    for item in tempList:
        c = str(item).split()[1]
        c = c[:-1]
        coursesList.append(c)

getCourseList()

@app.route('/')
@app.route('/index')
def index():
    global coursesList
    global exporting_threads

    """
    thread_id = random.randint(0, 10000)
    exporting_threads[thread_id] = ExportingThread()
    exporting_threads[thread_id].start()
    return 'task id: #%s' % thread_id"""

    return render_template('index.html', title='Dashboard', courses=coursesList)

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

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', downloadingText=downloadingNow)

@app.route('/browse')
def browse():
    course = Course.query.all()
    return render_template('browse.html', courses=course)

@app.route('/progress/<int:thread_id>')
def progress(thread_id):
    global exporting_threads
    return str(exporting_threads[thread_id].progress)

@app.route('/test', methods=['POST'])
def test():
    print("not implemented")
    return ""

@app.route('/next', methods=['POST'])
def next():
    global requestedRequests
    print("Cleared recieved requests")
    requestedRequests = set()
    return ""

# Main route of scraper
@app.route('/media', methods=['POST'])
def media():
    global requestedRequests
    global i
    global directory
    global coursesList

    req = request.json
    url = req['url']
    name = req['name']
    courseName = req['courseName']
    name = name.split('\n')[0]
    courseName = re.sub('[^0-9a-zA-Z]+', '_', courseName)
    name = re.sub('[^0-9a-zA-Z]+', '_', name)
    if(courseName not in coursesList):
        c = Course(coursename=courseName)
        db.session.add(c)
        db.session.commit()
        getCourseList()
        #courses = Course.query.all()

    directory = f"{path_to_directory}/{courseName}"
    video_pattern = ""
    is_video = False
    is_videoHD = re.search(video_patternHD, url)
    is_videoFHD = re.search(video_patternFHD, url)
    if(is_videoFHD):
        is_video = True
        video_pattern = video_patternFHD
    if(is_videoHD):
        is_video = True
        video_pattern = video_patternHD
    is_audio = re.search(audio_pattern, url)

    # There is only one GET request if the wideo is a mp4
    is_mp4 = re.search(mp4_pattern, url)
    if is_mp4:
        requestedRequests.add(video_pattern)
        requestedRequests.add(audio_pattern)
        fname = handle_windows_path(f"{directory}/video_{i}_{name}.mp4")
        print(f"downloading {fname}")
        urllib.request.urlretrieve(url, fname)
        print(f"downloading {fname}")
        courseID = db.session.query(Course).filter_by(coursename=courseName).first().id
        verbose_cls()
        i += 1

    # If course uses .aac and .ts we have to filter for unique requests
    if(len(requestedRequests) < 2):
        courseID = db.session.query(Course).filter_by(coursename=courseName).first().id
        if is_video and video_pattern not in requestedRequests:
            fname = handle_windows_path(f"{directory}/video_{i}_{name}.ts")
            print(f"downloading {fname}")
            #urllib.request.urlretrieve(url, fname)
            while(download(url, fname) is False):
                print(f"downloading {fname}")
                print(f"Error during downloading {fname}")
            requestedRequests.add(video_pattern)
            f = Files(filename=f"video_{i}_{name}.ts", course_id=courseID)
            db.session.add(f)
            db.session.commit()
            print(f"Downloaded {fname}")

        if is_audio and audio_pattern not in requestedRequests:
            fname = handle_windows_path(f"{directory}/audio_{i}_{name}.aac")
            print(f"downloading {fname}")
            #urllib.request.urlretrieve(url, fname)
            while(download(url, fname) is False):
                print(f"downloading {fname}")
                print(f"Error during downloading {fname}")
            requestedRequests.add(audio_pattern)
            f = Files(filename=f"audio_{i}_{name}.aac", course_id=courseID)
            db.session.add(f)
            db.session.commit()
            print(f"Downloaded {fname}")

        if len(requestedRequests) == 2:
            verbose_cls()
            i += 1
    return ""


