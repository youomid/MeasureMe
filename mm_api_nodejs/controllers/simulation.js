const superagent = require('superagent');

const EVENTS_SOURCE_URL = "http://localhost:1111"


module.exports = {
  completeWorkSession(req, res){
    return superagent.post(EVENTS_SOURCE_URL)
      .send("complete-work-session")
      .then(() => {
        return res.status(200).send("Success")
      });
  },
  incompleteWorkSession(req, res){
    return superagent.post(EVENTS_SOURCE_URL)
      .send("incomplete-work-session")
      .then(() => {
        return res.status(200).send("Success")
      });
  },
  pausedWorkSession(req, res){
    return superagent.post(EVENTS_SOURCE_URL)
      .send("paused-work-session")
      .then(() => {
        return res.status(200).send("Success")
      });
  },
  dailyComplete(req, res){
    return superagent.post(EVENTS_SOURCE_URL)
      .send("daily-goal-complete")
      .then(() => {
        return res.status(200).send("Success")
      });
  }
}