var urlRegex = /^https?:\/\/(?:[^./?#]+\.)?.pluralsight\.com/;

/*chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
      console.log(sender.tab ?
                  "from a content script:" + sender.tab.url :
                  "from the extension");
      if (request.text == "send_url")
        sendResponse({farewell: "goodbye"});
    }
  );*/

// Get neccessary data from DOM and send it back to the background.js
chrome.runtime.onMessage.addListener(function(msg, sender, sendResponse) {
    if (msg.text == 'send_url') {
        //let text = document.querySelector('button.content-item.is-current').innerText;
        let text = document.querySelector('button.content-item_is-current__1qJV9').innerText;
        //content-item_content-item__66EcK u-flex u-align-items-stretch content-item_is-current__1qJV9
        let cName = document.querySelector('a.course-title_course-title__link__1ExwT').innerText;
        //let cName = document.querySelector('a.course-title__link').innerText;
        var arrayIn = text.split('\n')[1];
        var array = arrayIn.split(' ');
        var sec = array[array.length - 1].slice(0, -1);
        var min = array[array.length - 2].slice(0, -1);
        var time = parseInt(min, 10) * 60 + parseInt(sec, 10);
        console.log(time)
        var toSend = String(text);
        console.log(toSend);
        fetch('http://127.0.0.1:45010/media', {
            method: 'POST',
            mode: 'no-cors',
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