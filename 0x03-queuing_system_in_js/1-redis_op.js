import redis from 'redis';

// this creates a new client
const client = redis.createClient(); 
// By default redis.createClient() will use 127.0.0.1 and port 6379

// listen for the connect event to see whether we successfully connected to the redis-server
client.on('connect', () => console.log('Redis client connected to the server'));

// listen for the error event tocheck if we failed to connect to the redis-server
client.on('error', (err) => console.error(`Redis client not connected to the server: ${err.message}`));

function setNewSchool(schoolName, value) {
    // redis.print prints “Reply: OK” to the console saying that redis saved the value
    client.set(schoolName, value, redis.print);
}

function displaySchoolValue(schoolName) {
    client.get(schoolName, (err, result) => {
        if (err) {
            console.log(err);
            throw err;
        }
    console.log(result);
    });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
