class httpServer {
    constructor() {
        this.PORT = 3000;

        this.ClientTCP = require('./tcpClient'); // Our module
        this.clientTCP = new this.ClientTCP(); // Running our module

        this.http = require('http'); // BUILT-IN MODULE

        this.server.listen(this.PORT, this.sayHello());
    }

    sayHello() {
        console.log(`Listening on port ${this.PORT}...`);
    }

    set PORT(PORT) {
        this._PORT = PORT;
    }

    get PORT() {
        return this._PORT;
    }

    set ClientTCP(ClientTCP) {
        this._ClientTCP = ClientTCP;
    }

    get ClientTCP() {
        return this._ClientTCP;
    }

    set clientTCP(clientTCP) {
        this._clientTCP = clientTCP;
    }

    get clientTCP() {
        return this._clientTCP;
    }

    set http(http) {
        this._http = http;

        // This is an event handler
        this.server = http.createServer((req, res) => {
            if(req.method === 'POST') {
                console.log('');
            }

            if(req.url === '/') {
                // if we're on the home page
                console.log('Entered the home page!'); // Will be displayed on server console
                var str = '{ "commandID": "1", "param": "http://www.mizostudio.com/privacy-policy.htm" }';
                var obj = JSON.parse(str);

                this.clientTCP.connect(JSON.stringify(obj));
                res.write('This is the home page!'); // Will be displayed on web page
            }

            if(req.url === '/api/pp/') {
                console.log('Entered the PP page!'); // Will be displayed on server console
                res.write('This is the PP page!'); // Will be displayed on web page
            }

            res.end();
        });
    }

    get http() {
        return this._http;
    }

    set server(server) {
        this._server = server;
    }

    get server() {
        return this._server;
    }
}

// Now the class is available "outside"
module.exports = httpServer;

http_server = new httpServer();