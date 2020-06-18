var urlRegex = /^https?:\/\/(?:[^./?#]+\.)?.pluralsight\.com/;

// Get neccessary data from DOM and send it back to the background.js
chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
    if (msg.text == 'send_url') {
        let text = document.querySelector('button.content-item.is-current').innerText;
        let cName = document.querySelector('a.course-title__link').innerText;
        var arrayIn = text.split('\n')[1];
        var array = arrayIn.split(' ');
        var sec = array[array.length - 1].slice(0, -1);
        var min = array[array.length - 2].slice(0, -1);
        var time = parseInt(min, 10) * 60 + parseInt(sec, 10);
        console.log(time)
        var toSend = String(text);
        console.log(toSend);
        fetch('http://localhost:5000/media', {
            method: 'POST',
            headers: { 'Content-type': 'application/json' },
            body: JSON.stringify({ url: msg.url, name: toSend, courseName: cName, videoDuration: time })
        });
        chrome.runtime.sendMessage({
            type: "notification",
            options: {
                type: "basic",
                title: "VideoDuration",
                message: time
            }
        });
        sendResponse("ok");
    }


});


// Unfortunately website has to implement key event handler. Solution below should work on supported website
// but this scrapper uses simulateKeyPress() from routes.py
Podium = {};
Podium.keydown = function(k) {
    var oEvent = document.createEvent('KeyboardEvent');

    // Chromium Hack
    Object.defineProperty(oEvent, 'keyCode', {
        get: function() {
            return this.keyCodeVal;
        }
    });
    Object.defineProperty(oEvent, 'which', {
        get: function() {
            return this.keyCodeVal;
        }
    });

    if (oEvent.initKeyboardEvent) {
        oEvent.initKeyboardEvent("keydown", true, true, document.defaultView, k, k, "", "", false, "");
    } else {
        oEvent.initKeyEvent("keydown", true, true, document.defaultView, false, false, false, false, k, 0);
    }

    oEvent.keyCodeVal = k;

    if (oEvent.keyCode !== k) {
        alert("keyCode mismatch " + oEvent.keyCode + "(" + oEvent.which + ")");
    }

    document.body.dispatchEvent(oEvent);
}

// Listen for next video messages
chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
    if (msg.text === 'next_video') {
        Podium.keydown(75);
    }
    sendResponse("ok");
});