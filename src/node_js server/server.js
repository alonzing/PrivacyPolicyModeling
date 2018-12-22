// var clientTCP = require('./clientTCP');

var ClientTCP = require('./tcpClient');
var clientTCP = new ClientTCP();

const http = require('http'); // BUILT-IN MODULE

// One of the functions of the module
// This is an event handler!!!
const server = http.createServer((req, res) => {
    if(req.url === '/') {
        // if we're on the home page
        console.log('Entered the home page!'); // Will be displayed on server console
        // console.log(JSON.stringify({"1": "https://stackoverflow.com/"}));
        var str = '{ "commandID": "1", "param": "http://www.mizostudio.com/privacy-policy.htm" }';
        var obj = JSON.parse(str);

        clientTCP.connect(JSON.stringify(obj));
        res.write('This is the home page!'); // Will be displayed on web page
    }

    if(req.url === '/api/pp/') {
        console.log('Entered the PP page!'); // Will be displayed on server console
        res.write('This is the PP page!'); // Will be displayed on web page
    }

    res.end();
});

port = 3000;
server.listen(port, function() {
    console.log(`Listening on port ${port}...`);
});