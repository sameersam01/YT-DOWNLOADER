
function downloadVideo() {
    // Get the YouTube video URL from the input field
    var url = document.getElementById('link_from_web').value;

    // Create a new XMLHttpRequest
    var xhr = new XMLHttpRequest();

    // Configure it: GET-request for the URL /download?url=...
    xhr.open('GET', '/download?url=' + encodeURIComponent(url), true);

    // Send the request over the network
    xhr.send();

    xhr.onload = function() {
        if (xhr.status != 200) {
            // analyze HTTP response
            alert(`Error ${xhr.status}: ${xhr.statusText}`);
        } else {
            // show the result
            alert(`Done, got ${xhr.response.length} bytes`);
        }
    };

    xhr.onerror = function() {
        alert("Request failed");
    };
}

