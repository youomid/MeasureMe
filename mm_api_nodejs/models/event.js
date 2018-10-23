'use strict';
module.exports = (sequelize, DataTypes) => {
  const Event = sequelize.define('Event', {
    user_name: DataTypes.STRING,
    event_type: DataTypes.STRING,
    description: DataTypes.STRING,
    event_info: DataTypes.JSON,
    date: DataTypes.DATE
  }, {});
  Event.associate = function(models) {
    // associations can be defined here
  };
  return Event;
};