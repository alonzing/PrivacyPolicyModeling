createForm();
getRequest('http://localhost:3000/?pp_url=http://afrogfx.com/Appspoilcy/com.MuslimRefliction.Al.Adab.Al.Mufrad-privacy_policy.html', onResponse);

function createForm() {
    let f = document.createElement("form");
    f.setAttribute('onsubmit', "alert('hello!')");

    f.setAttribute('name', "theForm");
    let form_group = document.createElement("div");

    form_group.setAttribute('class', "form-group");
    let pp_url_input = document.createElement("input");
    pp_url_input.setAttribute('type', "text");

    pp_url_input.setAttribute('class', "form-control");
    form_group.appendChild(pp_url_input);

    f.appendChild(form_group);
    document.getElementsByClassName('container')[0].appendChild(f);

}

function onResponse(response) {
    let text = document.createElement("p");
    text.setAttribute("class", 'text-justify');
    text.innerText = response;
    document.getElementsByClassName('container')[0].appendChild(text);


    console.log(response);
}

function getRequest(theUrl, callback) {
    let xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
            callback(xmlHttp.responseText);
        }
    };
    xmlHttp.open("GET", theUrl, true); // true for asynchronous

    xmlHttp.setRequestHeader("Content-Type", "application/json");
    xmlHttp.send();
}

// <!--<form name="theForm" onsubmit="alert(document.getElementById('exampleInputEmail1').value)">-->
// <!--<div class="form-group">-->
// <!--<label for="exampleInputEmail1">Privacy Policy URL</label>-->
// <!--<input type="text" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp"-->
// <!--placeholder="Please enter privacy policy URL" name="pp_url">-->
// <!--</div>-->
// <!--<button type="submit" class="btn btn-primary">Submit</button>-->
//     <!--</form>-->
