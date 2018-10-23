const redis = require('redis');
const moment = require('moment');
const Event = require('../models').Event;
const _ = require('underscore');
const client = redis.createClient();
const { Op } = require('sequelize')


var generateTimes = function(period){
  // generate a list of time ranges from start to end with a certain period
  // e.g. [[1536678000000, 1536681599999],...]
  
  if(period == "day"){
    var start = moment.utc().startOf('month').valueOf();
    var end = moment.utc().endOf('month').startOf('day').valueOf();
    var start_times = _.range(start,end, 8.64e+7);
    var end_times = _.range(start+86399999,end, 8.64e+7);

  }else if(period == "hour"){
    var start = moment().startOf('day').valueOf();
    var end = moment().endOf('day').startOf('hour').valueOf();
    var start_times = _.range(start,end, 3.6e+6);
    var end_times = _.range(start+3599999,end, 3.6e+6);
  }
  
  return [start_times, end_times];

};

var getMonthlyHistory = function(username){
  // example hash: "DailyBucket:test|1536678000000|1536681599999"
  var times = generateTimes("day");
  var buckets = [];

  for(var i =0; i < times[0].length; i++){
    client.hgetall(
      "DailyBucket:" + username + "|" + times[0][i] + "|" + times[1][i],
      function(err, result){
        if(result){
          buckets.push(result);
        }
      });
  }
  
  return buckets;
};

var getDailyHistory = function(username){
  var times = generateTimes("hour");
  var buckets = [];

  for(var i = 0; i < times[0].length; i++){
    client.hgetall(
      "HourlyBucket:" + username + "|" + times[0][i] + "|" + times[1][i],
      function(err, result){
        if(result){
          buckets.push(result);
        }
      });
  }

  return buckets;
};

var getEvents = function(username){
    // retrieve events for the past day for a user
    return Event
      .findAll({
        where: {
          user_name: username,
          date: {
            [Op.gte]: moment().subtract(1, "days").toDate(),
          },
        }
      })
      .then((events) => events)
};

var getDashboard = function(username){
    return [getEvents(username), getDailyHistory(username), getMonthlyHistory(username)];
};


module.exports = {
  getDashboard,
};

