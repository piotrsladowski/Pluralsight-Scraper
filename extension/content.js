var urlRegex = /^https?:\/\/(?:[^./?#]+\.)?.pluralsight\.com/;

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        let text = document.querySelector('button.content-item.is-current').innerText;
        let cName = document.querySelector('a.course-title__link').innerText;
        var toSend = String(text);
        console.log(toSend);
        fetch('http://localhost:5000/media', {
            method: 'POST',
            headers: { 'Content-type': 'application/json' },
            body: JSON.stringify({ url: request.url, name: toSend, courseName: cName })
        });
        sendResponse("ok");
    });