const LocalStrategy = require('passport-local').Strategy;
const bcrypt = require('bcryptjs');
const User = require('../models').User;

module.exports = function passportModule(passport) {
  passport.use('login', new LocalStrategy({
    passReqToCallback: true
  },function(req, username, password, done){
    var salt = bcrypt.genSaltSync(10);
    User.findOne({
        where: {
          user_name: username
        }
      })
      .then((user) => {
        if(bcrypt.compareSync(password, user.password)){
          return done(null, user)
        }
        return done(null, false)
      })
  }));

  passport.use('register', new LocalStrategy({
    passReqToCallback: true
  },function(req, username, password, done){
    var salt = bcrypt.genSaltSync(10);
    User.create({
      user_name: username,
      password: bcrypt.hashSync(password, salt),
    })
    .then((user) => {
      return done(null, user);
    });
  }));
}