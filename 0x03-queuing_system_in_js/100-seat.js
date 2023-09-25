const express = require('express');
const redis = require('redis');
const { promisify } = require('util');
const kue = require('kue');
const bodyParser = require('body-parser');

const app = express();
const port = 1245;

// Create a Redis client and use promisify
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Create a Kue queue
const queue = kue.createQueue();

// Middleware to parse JSON request bodies
app.use(bodyParser.json());

// Initialize the number of available seats and reservationEnabled
let availableSeats = 50;
let reservationEnabled = true;

// Function to set the available seats in Redis
const reserveSeat = async (number) => {
  try {
    await setAsync('available_seats', number.toString());
  } catch (error) {
    throw new Error('Reservation failed');
  }
};

// Function to get the current available seats from Redis
const getCurrentAvailableSeats = async () => {
  try {
    const seats = await getAsync('available_seats');
    return parseInt(seats) || 0;
  } catch (error) {
    throw new Error('Unable to get available seats');
  }
};

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', async (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });
});

// Route to process the queue and decrease available seats
app.get('/process', async (req, res) => {
  res.json({ status: 'Queue processing' });

  const currentSeats = await getCurrentAvailableSeats();

  if (currentSeats === 0) {
    reservationEnabled = false;
    return;
  }

  if (currentSeats >= 1) {
    try {
      await reserveSeat(currentSeats - 1);
    } catch (error) {
      // Handle errors here if needed
    }
  }

  queue.process('reserve_seat', async (job, done) => {
    if (currentSeats === 0) {
      done(new Error('Not enough seats available'));
      return;
    }
    done();
  });

  queue.on('job complete', (id) => {
    console.log(`Seat reservation job ${id} completed`);
  });

  queue.on('job failed', (id, error) => {
    console.log(`Seat reservation job ${id} failed: ${error.message}`);
  });
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});

