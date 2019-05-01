var request = require('request');
var Cookie = require('request-cookies').Cookie;

request.post('https://www.cinema-city.co.il/order/?eventID=399218', function(err, response, body) {
    var rawcookies = response.headers['set-cookie'];
    for (var i in rawcookies) {
        var cookie = new Cookie(rawcookies[i]);
        console.log(cookie.key, cookie.value, cookie.expires);
    }
});