const buckets = require('../services').Buckets;


module.exports = {
  getById(req, res){
    return res.status(200).send([])
  },
  getDashboard(req, res){
    // retrieve hourly buckets for the past
    return Promise.all(buckets.getDashboard(req.params.username))
              .then(function(allData){
                res.status(200).send({
                  'events': allData[0],
                  'daily_history': allData[1],
                  'monthly_history': allData[2]
                })
              })
  },
}