const Event = require('../models').Event;
const moment = require('moment');

module.exports = {
  list(req, res){
    return Event
      .findAll()
      .then((events) => res.status(200).send(events))
      .catch((error) => res.status(400).send(error))
  },
  getByUserName(req, res){
    return Event
      .findAll({
        where: {
          user_name: req.params.username
        }
      })
      .then((events) => res.status(200).send(events))
      .catch((error) => res.status(400).send(error))
  },
  add(req, res){
    return Event
      .create({
        user_name: req.body.username,
        event_type: req.body.event_type,
        description: req.body.description,
        event_info: req.body.event_info,
        date: req.body.date
      })
      .then((events) => res.status(200).send(events))
      .catch((error) => res.status(400).send(error))
  },
  update(req, res){
    return Event
      .findAll({
        where: {
          user_name: req.params.username
        }
      })
      .then((events) => {
        events.forEach((event) => {
          event.update({
            description: req.body.description
          })
          .then((events) => console.log('Success updating object: ' + event))
          .catch((error) => console.log('Error updating object: ' + event))
        })

        return res.status(200).send(events)
      })
      .catch((error) => res.status(400).send(error))
  },
  delete(req, res){
    return Event
      .destroy({
        where: {
          user_name: req.params.username
        }
      })
      .then((events) => res.sendStatus(200).send(events))
      .catch((error) => res.sendStatus(400).send(error))
  },

}