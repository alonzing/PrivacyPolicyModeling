class tcpClient {
    constructor() {
        this.HOST = '172.19.3.233';
        this.PORT = 8080;

        this.new_data = '';
        this.end_of_json = 'END_OF_MESSAGE&#';

        this.net = require('net');
        this.client = new this.net.Socket();
    }

    connect(message) {
        this.client.connect(this.PORT, this.HOST, () => {
            console.log(`Client connected to: ${this.HOST}:${this.PORT}`);
            // Write a message to the socket as soon as the client is connected, the server will receive it as message from the client
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

    set end_of_json(end_of_json) {
        this._end_of_json = end_of_json;
    }

    get end_of_json() {
        return this._end_of_json;
    }

    set client(client) {
        this._client = client;

        this.client.on('data', (data) => {
            this.new_data += data;

            if(data.toString().endsWith(this.end_of_json)) {
                this.new_data = this.new_data.replace(this.end_of_json, '');

                console.log('Client received: ' + JSON.parse(this.new_data));
                this.new_data = '';

                if (data.toString().endsWith('exit')) {
                    this.client.destroy();
                }
            }
        });

        // Add a 'close' event handler for the client socket
        this.client.on('close', () => {
            console.log('Client closed');
        });

        // Handle error
        client.on('error', (err) => {
            console.error(err);
        });
    }

    get client() {
        return this._client;
    }
}

// Now the class is available "outside"
module.exports = tcpClient;