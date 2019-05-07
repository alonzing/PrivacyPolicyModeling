createForm();
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

function createForm() {
    let f = document.createElement("form");
    f.onsubmit = function () {
        let v = document.getElementById('pp_url_input').value;
        if (v !== "") {
            getRequest(document.getElementById('pp_url_input').value, onResponse);
            document.getElementById('error_msg').innerText = '';

        } else {
            document.getElementById('error_msg').innerText = 'Please enter a valid URL, idiot.';
        }
        return false;
    };
    f.name = "theForm";
    let form_group = document.createElement('div');
    form_group.setAttribute('class', 'form-group row');

    let pp_url_input = document.createElement('input');
    pp_url_input.setAttribute('type', 'text');
    pp_url_input.setAttribute('class', 'col-sm-10 form-control');
    pp_url_input.setAttribute('id', 'pp_url_input');
    pp_url_input.setAttribute('placeholder', 'Privacy Policy URL');
    form_group.appendChild(pp_url_input);

    let send_button = document.createElement('button');
    send_button.setAttribute('type', 'submit');
    send_button.setAttribute('class', 'col-sm-2 btn btn-primary');
    send_button.setAttribute('id', 'send_button');
    send_button.innerText = 'Send';
    form_group.appendChild(send_button);

    let error_msg = document.createElement('small');
    error_msg.setAttribute('id', 'error_msg');
    error_msg.setAttribute('class', 'text-danger');
    form_group.appendChild(error_msg);


    f.appendChild(form_group);
    document.getElementsByClassName('container')[0].appendChild(f)
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

