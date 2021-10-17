from flask import Flask, render_template, flash, redirect, request
import urllib.request
import re
import os
from pathlib import Path
from pynput.keyboard import Key, Controller
import time

app = Flask(__name__)

# Global variables

requestedRequests = set()
video_patternHD = "hls_1280x720.ts"
video_patternFHD = "hls_1920x1080.ts"
audio_pattern = "hls_aac-96k-eng.aac"
mp4_pattern = "1280x720.mp4"


keyboard = Controller()
# Adjust this variable to your network connection (from 0 to 1)
downloadingInterval = 0.1
videoDuration = 0
downloadedFiles = 0
automatic = False # Change this if you'd like to download manually

# Change path below if you want save videos in different location
path_to_directory = "data"
downloadingNow = "nothing"

# This line has to be set manually
print("Starting index: ")
i = int(input())
coursesList = []

########### Logic #############

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
    global downloadedFiles
    try:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        downloadingNow = f"{filename}"
        urllib.request.urlretrieve(url, filename)
        downloadingNow = "nothing"
        downloadedFiles += 1
        return True
    except FileNotFoundError:
        print("Destination directory doesn't exist")
        downloadingNow = "nothing"
        return False
    except ConnectionError:
        print("Connection error")
        downloadingNow = "nothing"
        return False


# Browser window must be active
def simulateKeyPress():
    global downloadedFiles
    # Switch to the next video
    if(downloadedFiles >= 2):
        keyboard.press('>')
        keyboard.release('>')
    downloadedFiles = 0
    # Reset requests list
    with keyboard.pressed(Key.shift):
        with keyboard.pressed(Key.alt):
            keyboard.press('5')
            keyboard.release('5')

def clearRequests():
    global requestedRequests
    global videoDuration
    time.sleep(videoDuration*downloadingInterval)
    print("Cleared recieved requests")
    requestedRequests = set()
    videoDuration = 0
    simulateKeyPress()

# Function below is triggered by user click
def clearRequestsInstantly():
    global requestedRequests
    global videoDuration
    print("Cleared recieved requests")
    requestedRequests = set()
    videoDuration = 0


@app.route('/')

@app.route('/next', methods=['POST'])
def next():
    clearRequestsInstantly()
    return ""

# Main route of scraper
@app.route('/media', methods=['POST'])
def media():
    global requestedRequests
    global i
    global directory
    global coursesList
    global videoDuration

    # Extract fields from extension request
    req = request.get_json(force=True)
    url = req['url']
    name = req['name']
    courseName = req['courseName']
    videoDuration = req['videoDuration']
    name = name.split('\n')[0]
    courseName = re.sub('[^0-9a-zA-Z]+', '_', courseName)
    name = re.sub('[^0-9a-zA-Z]+', '_', name)

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
        verbose_cls()
        i += 1

    # If course uses .aac and .ts we have to filter for unique requests
    if(len(requestedRequests) < 2):
        if is_video and video_pattern not in requestedRequests:
            fname = handle_windows_path(f"{directory}/video_{i}_{name}.ts")
            print(f"downloading {fname}")
            #urllib.request.urlretrieve(url, fname)
            while(download(url, fname) is False):
                print(f"downloading {fname}")
                print(f"Error during downloading {fname}")
            requestedRequests.add(video_pattern)
            print(f"Downloaded {fname}")

        if is_audio and audio_pattern not in requestedRequests:
            fname = handle_windows_path(f"{directory}/audio_{i}_{name}.aac")
            print(f"downloading {fname}")
            #urllib.request.urlretrieve(url, fname)
            while(download(url, fname) is False):
                print(f"downloading {fname}")
                print(f"Error during downloading {fname}")
            requestedRequests.add(audio_pattern)
            print(f"Downloaded {fname}")

        if len(requestedRequests) == 2:
            verbose_cls()
            i += 1
    if(automatic):
        clearRequests()
    return ""

if __name__ == '__main__':
    app.run(port=45010, threaded=False)

