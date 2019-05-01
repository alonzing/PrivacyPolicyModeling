const request = require('request');
request('http://localhost:5000/get-pp?url=http://afrogfx.com/Appspoilcy/com.MuslimRefliction.Al.Adab.Al.Mufrad-privacy_policy.html', {json: true}, (err, res, body) => {
    let a = res.body;
    console.log(a[1]);
});