// getRequest('http://localhost:3000/?pp_url=https://www.snappii.com/policy', onResponse);
// http://localhost:3000/?pp_url=http://afrogfx.com/Appspoilcy/com.MuslimRefliction.Al.Adab.Al.Mufrad-privacy_policy.html

function onResponse(response) {
    let jsonContent = JSON.parse(response);
    displayScore(jsonContent.score);
    document.getElementById("pp_text").innerText = jsonContent.pp_text;
}

function displayScore(score) {
    let score_badge = document.getElementById("pp_score_badge");
    score_badge.innerText = score;
    let badge_class;
    if (score >= 90) {
        badge_class = "badge badge-success";
    } else if (score >= 70) {
        badge_class = "badge badge-warning";
    } else {
        badge_class = "badge badge-danger";
    }
    score_badge.setAttribute("class", badge_class);
    document.getElementById("pp_score_header").innerHTML += "Score: "
}

function OnSubmit() {
    let v = document.getElementById('pp_url_input').value;

    // Mock
    getRequest(document.getElementById('pp_url_input').value, onResponse);

    // if (v !== "") {
    //     getRequest(document.getElementById('pp_url_input').value, onResponse);
    //     document.getElementById('error_msg').innerText = '';
    //
    // } else {
    //     document.getElementById('error_msg').innerText = 'Please enter a valid URL, idiot.';
    // }
}

function responseMock() {
    return '{"pp_text":"PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT ",' +
        '"category":"CATEGORY_NAME", "score":"75", "uid": 1100}';
}

function getRequest(theUrl, callback) {
    callback(responseMock())
    // let xmlHttp = new XMLHttpRequest();
    //
    // xmlHttp.open("GET", theUrl, true); // true for asynchronous
    // xmlHttp.onreadystatechange = function () {
    //     if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
    //         callback(xmlHttp.responseText);
    //     }
    // };
    // xmlHttp.send();
}

