from flask import render_template, flash, redirect, request
from app import app, db
from app.forms import LoginForm
from app.models import Course, Files
import urllib.request
import re
import os

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

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Mati'}
    courses = Course.query.all()
    global exporting_threads

    thread_id = random.randint(0, 10000)
    exporting_threads[thread_id] = ExportingThread()
    exporting_threads[thread_id].start()
    return 'task id: #%s' % thread_id

    #return render_template('index.html', title='Dashboard', courses=courses)

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
    return render_template('dashboard.html')

@app.route('/browse')
def browse():
    course = Course.query.all()
    return render_template('browse.html', courses=course)


### logic

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
    try:
        urllib.request.urlretrieve(url, filename)
        return True
    except FileNotFoundError:
        print("Destination directory doesn't exist")
        return False

requestedRequests = set()
video_pattern = "hls_1280x720.ts"
audio_pattern = "hls_aac-96k-eng.aac"
mp4_pattern = "1280x720.mp4"

course_kind_directory = "networking"
course_kind_name = "docker"
path_to_directory = "data"
directory = f"{path_to_directory}/{course_kind_name}/{course_kind_directory}"

print("Starting index: ")
i = int(input())
exporting_threads = {}

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
    print("jazda")
    requestedRequests = set()
    return ""


@app.route('/media', methods=['POST'])
def media():
    global requestedRequests
    global i
    req = request.json
    url = req['url']
    name = req['name']
    courseName = req['courseName']
    name = name.split('\n')[0]
    name = name.replace(' ', '_')
    for ch in ['/','?','.',',',':','*','"','<','>','|']:
        if ch in name:
            name = name.replace(ch, '_')

    # There is only one GET request if the wideo is a mp4
    is_mp4 = re.search(mp4_pattern, url)
    if is_mp4:
        requestedRequests.add(video_pattern)
        requestedRequests.add(audio_pattern)
        fname = handle_windows_path(f"{directory}/video_{i}_{name}.mp4")
        print(f"downloading {fname}")
        urllib.request.urlretrieve(url, fname)
        print(f"downloading {fname}")
        verbose_cls()
        i += 1


    is_video = re.search(video_pattern, url)
    is_audio = re.search(audio_pattern, url)
    # If course uses .aac and .ts we have to filter for unique requests
    if(len(requestedRequests) < 2):
        if is_video and video_pattern not in requestedRequests:
            requestedRequests.add(video_pattern)
            fname = handle_windows_path(f"{directory}/video_{i}_{name}.ts")
            print(f"downloading {fname}")
            #urllib.request.urlretrieve(url, fname)
            while(download(url, fname) is False):
                print(f"downloading {fname}")
                print(f"Error during downloading {fname}")
            print(f"pobrałem {fname}")

        if is_audio and audio_pattern not in requestedRequests:
            requestedRequests.add(audio_pattern)
            fname = handle_windows_path(f"{directory}/audio_{i}_{name}.aac")
            print(f"downloading {fname}")
            #urllib.request.urlretrieve(url, fname)
            while(download(url, fname) is False):
                print(f"downloading {fname}")
                print(f"Error during downloading {fname}")
            print(f"pobrałem {fname}")

        if len(requestedRequests) == 2:
            verbose_cls()
            i += 1
    return ""


