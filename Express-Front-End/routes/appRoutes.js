const express = require('express');
const PredictiveModelAPI = require('../api/PredictiveModelApi');
const router = express.Router();

router.get('/', function (req, res) {
  res.render('pages/landingPage');
});

router.get('/pie-chart-component', function (req, res) {
  res.render('pages/pieChartExamplePage');
});

router.get('/bar-chart-component', function (req, res) {
  res.render('pages/barChartExamplePage');
});

router.get('/table-chart-component', function (req, res) {
  const results = PredictiveModelAPI.getResults();
  const headers = PredictiveModelAPI.getHeaders();
  res.render('pages/tabularExamplePage', { results, headers });
});

module.exports = router;