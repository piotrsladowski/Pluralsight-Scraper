let videoRequestSended = false;
let audioRequestSended = false;
let mp4RequestSended = false;

chrome.browserAction.onClicked.addListener(function () {
    videoRequestSended = false;
    audioRequestSended = false;
    mp4RequestSended = false;
    console.clear()
    console.log("reset")
    fetch('http://localhost:65432/kamil', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: "next_video_please"
    });
});

function doStuffWithDom(domContent) {
    console.log('I received the DOM content:\n');
}

chrome.webRequest.onBeforeSendHeaders.addListener(
    function (details) {
        if (details.url) {
            const isVideo = details.url.includes("hls_1280x720.ts");
            const isAudio = details.url.includes("hls_aac-96k-eng.aac");
            const isMp4 = details.url.includes("1280x720.mp4");
            const isExpiration = details.url.includes("expiretime");

            if (!isExpiration) {
                if (!isMp4) {
                    if (isVideo && !videoRequestSended) {
                        videoRequestSended = true;
                        mp4RequestSended = true;
                        sendRequestToContentJs(details, "video");
                    }

                    if (isAudio && !audioRequestSended) {
                        audioRequestSended = true;
                        mp4RequestSended = true;
                        sendRequestToContentJs(details, "audio");
                    }
                } else {
                    if (!mp4RequestSended) {
                        mp4RequestSended = true;
                        videoRequestSended = true;
                        audioRequestSended = true;
                        sendRequestToContentJs(details, "mp4");
                    }
                }
            }
        }

    }, { urls: ["*://*.pluralsight.com/*"] }, ["blocking"]);

function sendRequestToContentJs(details, kind) {
    // send url to content.js to extract video_name
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.tabs.sendMessage(tabs[0].id, { url: details.url }, function (response) {
            console.log("URL has been sent");
        });
    });
    console.log(`${kind} request: ${details.url}`)
}
