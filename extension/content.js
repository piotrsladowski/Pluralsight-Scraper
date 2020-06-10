var urlRegex = /^https?:\/\/(?:[^./?#]+\.)?.pluralsight\.com/;

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        let text = document.querySelector('button.content-item.is-current').innerText;
        var toSend = String(text);
        console.log(toSend);
        fetch('http://localhost:65432/adam', {
            method: 'POST',
            headers: { 'Content-type': 'application/json' },
            body: JSON.stringify({ url: request.url, name: toSend })
        });
        sendResponse("ok");
    });