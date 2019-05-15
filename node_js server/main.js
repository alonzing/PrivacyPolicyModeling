// getRequest('http://localhost:3000/?pp_url=https://www.snappii.com/policy', onResponse);
// http://localhost:3000/?pp_url=http://afrogfx.com/Appspoilcy/com.MuslimRefliction.Al.Adab.Al.Mufrad-privacy_policy.html


function displayStatisticalDetails(response) {
    document.getElementById("t_body_number_of_paragraphs_val").innerText = response.num_of_paragraphs;
    document.getElementById("t_body_number_of_paragraphs_category_val").innerText = response.num_of_paragraphs_category_value;
    document.getElementById("t_body_number_of_topics_val").innerText = response.num_of_topics;
    document.getElementById("t_body_number_of_topics_category_val").innerText = response.num_of_topics_category_value;
    document.getElementById("t_body_missing_material_paragraphs_val").innerText = response.num_of_missing_paragraphs;
    document.getElementById("t_body_missing_material_paragraphs_category_val").innerText = response.num_of_missing_paragraphs_category_value;
    document.getElementById("statistical_table").removeAttribute("hidden");
}
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
async function onResponse(response) {
    document.getElementById("spinner").setAttribute("hidden", "hidden");

    displayScore(response.score);
    displayParagraphs(response.paragraphs);
    displayStatisticalDetails(response);
    // Show or hide text button
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

function displayParagraphs(paragraphs) {
    let str = '';
    let lastIndex = 0;
    paragraphs.forEach(function (element) {
        if (element["index"] < lastIndex) {
            return;
        }
        lastIndex++;
        str += element["paragraph"].replace(/\n*\n/gi, ".\n") + ".\n\n";
    });

    document.getElementById("pp_text_content").innerText = str;
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

    if (v !== "") {
        getRequest(document.getElementById('pp_url_input').value, onResponse);
        document.getElementById('error_msg').innerText = '';

    } else {
        document.getElementById('error_msg').innerText = 'Please enter a valid URL, idiot.';
    }
}


function getRequest(theUrl, callback) {
    axios.get('http://127.0.0.1:5000/pp-prediction?url=' + theUrl)
        .then(async function (response) {
            // handle success
            await sleep(5000);
            callback(response.data);
        })
        .catch(function (error) {
            // handle error
            console.log(error);
        })
        .finally(function () {
            // always executed
        });
    document.getElementById("spinner").removeAttribute("hidden");
}

