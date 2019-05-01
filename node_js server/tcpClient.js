class tcpClient {
    constructor() {
        this.HOST = '127.0.0.1';
        this.PORT = 8583;

        this.new_data = '';

        this.net = require('net');
        this.client = new this.net.Socket();
        this.res = null;
    }

    connect(message, res) {
        this.client.connect(this.PORT, this.HOST, () => {
            console.log(`Client connected to: ${this.HOST}:${this.PORT}`);
            this.res = res;
            // Write a message to the socket as soon as the client is connected, the server will receive it as a message from the client
            this.client.write(message);
        });
    }

    /**
     * All the setters & getters starts here!
     * The client setter is the longest (and VERY LONG)
     * due to the fact that it contains the event handlers!
     */
    set net(net) {
        this._net = net;
    }

    get net() {
        return this._net;
    }

    set new_data(new_data) {
        this._new_data = new_data;
    }

    get new_data() {
        return this._new_data;
    }

    set client(client) {
        this._client = client;

        this.client.on('data', (data) => {
            this.new_data += data;

            if (data.toString().endsWith('exit')) {
                this.client.destroy();
            }
        });

        // What to do when the whole response has been received
        this.client.on('end', () => {
            console.log('Client received: ' + JSON.parse(this.new_data));

            let parsed = JSON.parse(this.new_data);
            let str = '';
            parsed.forEach(function(element) {
                // console.log(element);
                str += element.replace('\n\n', '<br><br>');
                str += '<br><br>'
            });
            this.res.send(str);
        });

        // Add a 'close' event handler for the client socket
        this.client.on('close', () => {
            console.log('Client closed');
        });

        // Handle error
        this.client.on('error', (err) => {
            console.error(err);
        });
    }

    get client() {
        return this._client;
    }
}

// Now the class is available "outside"
module.exports = tcpClient;