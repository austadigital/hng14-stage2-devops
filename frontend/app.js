const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();

// FIX 9: Use environment variable instead of hardcoded URL
const API_URL = process.env.API_URL || "http://api:8000";

app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));

// FIX 10: Proper error handling for /submit
app.post('/submit', async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/jobs`);
    res.json(response.data);
  } catch (err) {
    res.status(500).json({
      error: "Failed to submit job",
      details: err.message
    });
  }
});

// FIX 11: Proper error handling for /status/:id
app.get('/status/:id', async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/jobs/${req.params.id}`);
    res.json(response.data);
  } catch (err) {
    res.status(err.response?.status || 500).json({
      error: "Failed to fetch job status",
      details: err.message
    });
  }
});

const PORT = process.env.PORT || 3000;

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Frontend running on port ${PORT}`);
});

