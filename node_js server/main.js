// getRequest('http://localhost:3000/?pp_url=https://www.snappii.com/policy', onResponse);
// http://localhost:3000/?pp_url=http://afrogfx.com/Appspoilcy/com.MuslimRefliction.Al.Adab.Al.Mufrad-privacy_policy.html


function onResponse(response) {
    let jsonContent = JSON.parse(response);
    displayScore(jsonContent.score);
    document.getElementById("pp_text_content").innerText = jsonContent.pp_text;

    $('#pp_text_div').attr('class', 'd-block');
    $("#pp_text_collapse").on(('show.bs.collapse'), function () {
        $("#pp_text_collapse_button").attr('disabled', true);
    }).on(('hide.bs.collapse'), function () {
        $("#pp_text_collapse_button").attr('disabled', true);
    }).on(('shown.bs.collapse'), function () {
        $("#pp_text_collapse_button").text('Hide Text').attr('disabled', false);
    }).on(('hidden.bs.collapse'), function () {
        $("#pp_text_collapse_button").text('Show Text').attr('disabled', false);
    });
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
    document.getElementById("pp_score_header").innerHTML = "Score: ";
    score_badge.setAttribute("class", badge_class);
}

function OnSubmit() {
    let v = document.getElementById('pp_url_input').value;

    // // Mock
    // getRequest(document.getElementById('pp_url_input').value, onResponse);

    if (v !== "") {
        getRequest(document.getElementById('pp_url_input').value, onResponse);
        document.getElementById('error_msg').innerText = '';

    } else {
        document.getElementById('error_msg').innerText = 'Please enter a valid URL, idiot.';
    }
}

function responseMock() {
    return '{"pp_text":"PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT PP TEXT ",' +
        '"category":"CATEGORY_NAME", "score":"50"}';
}

function getRequest(theUrl, callback) {
    console.log('response');
    // axios.get('http://www.google.com/')
    //     .then(function (response) {
    //         // handle success
    //         console.log(response);
    //     })
    //     .catch(function (error) {
    //         // handle error
    //         console.log(error);
    //     })
    //     .finally(function () {
    //         // always executed
    //     });


    axios.get('http://127.0.0.1:5000/pp-prediction?url=' + theUrl)
        .then(function (response) {
            // handle success
            callback(response.data);
        })
        .catch(function (error) {
            // handle error
            console.log(error);
        })
        .finally(function () {
            // always executed
        });
}

