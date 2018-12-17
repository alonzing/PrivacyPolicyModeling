var net = require('net');

// Configuration parameters
var HOST = '172.19.3.233';
var PORT = 8080;

// Create Client instance
var client = new net.Socket();
var len = 0;
var new_data = '';
const end_of_json = 'END_OF_MESSAGE&#';

client.on('data', (data) => {
    new_data += data;

    if(data.toString().endsWith(end_of_json)) {
        new_data = new_data.replace(end_of_json, '');

        console.log('Client received: ' + JSON.parse(new_data));
        new_data = '';

        if (data.toString().endsWith('exit')) {
            client.destroy();
        }
    }
});

// Add a 'close' event handler for the client socket
client.on('close', () => {
    console.log('Client closed');
});

// Handle error
client.on('error', (err) => {
    console.error(err);
});

exports.connect = function(tempname) {
    // Connect to the defined port & host
    // Run the function
    client.connect(PORT, HOST, () => {
        console.log('Client connected to: ' + HOST + ':' + PORT);
        // Write a message to the socket as soon as the client is connected, the server will receive it as message from the client
        client.write(tempname);
    });
};