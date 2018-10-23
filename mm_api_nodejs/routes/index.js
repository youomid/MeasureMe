var express = require('express');
const passport = require('passport');
const eventController = require('../controllers').event;
const bucketsController = require('../controllers').buckets;
const simulationController = require('../controllers').simulation;

var router = express.Router();

// authentication urls
router.post(
  '/login',
  passport.authenticate('login'),
  function(req, res) {
    res.status(200).send("Successfully logged in.")
  });
router.post('/register',
  passport.authenticate('register'),
  function(req, res){
    res.status(200).send("Successfully registered.")
  });
router.post('/logout',
  function(req, res){
    req.logout();
    res.status(200).send("Successfully logged out.")
  });


// Event model urls
router.get('/api/event', eventController.list);
router.post('/api/event', eventController.add);
router.get('/api/event/:username', eventController.getByUserName);
router.post('/api/event/:username', eventController.update);
router.delete('/api/event/:username', eventController.delete)

// buckets urls
router.get('/api/buckets', bucketsController.getById)

// dashboard
router.get('/dashboard/:username', bucketsController.getDashboard)

// simulation urls
router.get('/simulations/complete_work_session', simulationController.completeWorkSession)
router.get('/simulations/incomplete_work_session', simulationController.incompleteWorkSession)
router.get('/simulations/paused_work_session', simulationController.pausedWorkSession)
router.get('/simulations/daily_complete', simulationController.dailyComplete)

// websockets url
router.ws('/ws/sendmessage', function(ws, req){
  ws.on('message', function(msg){
    console.log(msg);
  });
});

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

module.exports = router;
