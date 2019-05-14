// getRequest('http://localhost:3000/?pp_url=http://afrogfx.com/Appspoilcy/com.MuslimRefliction.Al.Adab.Al.Mufrad-privacy_policy.html', onResponse);
// http://localhost:3000/?pp_url=http://afrogfx.com/Appspoilcy/com.MuslimRefliction.Al.Adab.Al.Mufrad-privacy_policy.html

function onResponse(response) {
    let main_text = document.getElementById("main_text");
    if (main_text == null) {
        main_text = document.createElement("p");
        main_text.setAttribute("class", 'text-justify');
        main_text.setAttribute("id", "main_text");
        document.getElementsByClassName('container')[0].appendChild(main_text);
    }

    main_text.innerText = response;
    console.log(response);
}

function x() {
    let v = document.getElementById('pp_url_input').value;
    if (v !== "") {
        getRequest(document.getElementById('pp_url_input').value, onResponse);
        document.getElementById('error_msg').innerText = '';

    } else {
        document.getElementById('error_msg').innerText = 'Please enter a valid URL, idiot.';
    }
}

function getRequest(theUrl, callback) {
    let xmlHttp = new XMLHttpRequest();

    xmlHttp.open("GET", theUrl, true); // true for asynchronous
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
            callback(xmlHttp.responseText);
        }
    };
    xmlHttp.send();
}

