var urlRegex = /^https?:\/\/(?:[^./?#]+\.)?.pluralsight\.com/;

chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
    if (msg.text == 'send_url') {
        let text = document.querySelector('button.content-item.is-current').innerText;
        let cName = document.querySelector('a.course-title__link').innerText;
        var toSend = String(text);
        console.log(toSend);
        fetch('http://localhost:5000/media', {
            method: 'POST',
            headers: { 'Content-type': 'application/json' },
            body: JSON.stringify({ url: msg.url, name: toSend, courseName: cName })
        });
        sendResponse("ok");
    }
});

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
        console.log("Key has been pressed")
    }
    sendResponse("ok");
});