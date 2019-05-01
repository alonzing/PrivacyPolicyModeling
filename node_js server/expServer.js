class expServer {
    constructor() {
        this.express = require('express');
        this.app = this._express();
        this.app.use(function(req, res, next) {
            res.header("Access-Control-Allow-Origin", "*");
            res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
            next();
        });
        this.app.get('/',(req, res) => {
            // if we're on the home page
            console.log('Entered the home page!'); // Will be displayed on server console

            if (req.query) {
                let str = req.query;
                // let obj = JSON.parse(str);
                this._clientTCP = new this._ClientTCP(); // Running our module
                // this.clientTCP.connect(JSON.stringify(obj));
                this.clientTCP.connect('{ \"commandID\": \"1\"' + ',' + '\"param\":' + '\"' + str.pp_url + '"' + '}', res);
            }
        });

        this.ClientTCP = require('./tcpClient'); // Our module
        this.clientTCP = new this._ClientTCP(); // Running our module

        this.PORT = process.env.PORT || 3000; // set PORT = some_value (in console)
        this.listen();
    }

    listen() {
        this._app.listen(this._PORT, () => {
            // Will be displayed on server console
            console.log(`listening on port ${this._PORT}`);
        });
    }

    get clientTCP() {
        return this._clientTCP;
    }

    set clientTCP(value) {
        this._clientTCP = value;
    }

    get ClientTCP() {
        return this._ClientTCP;
    }

    set ClientTCP(value) {
        this._ClientTCP = value;
    }

    get PORT() {
        return this._PORT;
    }

    set PORT(value) {
        this._PORT = value;
    }

    get app() {
        return this._app;
    }

    set app(value) {
        this._app = value;
    }

    get express() {
        return this._express;
    }

    set express(value) {
        this._express = value;
    }
}

// Now the class is available "outside"
module.exports = expServer;

express_server = new expServer();



// this.app.get('/api/courses/:id', (req, res) => {
//     let course = courses.find(c => c.id === parseInt(req.params.id));
//     if (course) {
//         res.send(course);
//     } else {
//         res.status(404).send('The course ID was not found!');
//     }
// });

// this.app.post('/api/courses', (req, res) => {
//     const course = { // Create a course object
//         id: this._courses.length + 1, // Take the length of the 'courses' array
//         name: req.body.name // take the name from the body of the request
//     };
//
//     course.push(course); // Create the course on the server
//     res.send(course); // return the new course to the client (send the respons)
// });