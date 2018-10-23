var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var User = require('./models').User;
var passportModule = require('./passport').passportModule;

var app = express();
var expressWs = require('express-ws')(app);

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');


// authentication setup
var passport = require('passport');
var expressSession = require('express-session');
app.use(expressSession({secret: 'mm_api_secret_key', resave: true, saveUninitialized: true}));
app.use(passport.initialize());
app.use(passport.session());

passport.serializeUser(function(user, done) {
  done(null, user.id);
});
 
passport.deserializeUser(function(id, done) {
  User.findById(id, function(err, user) {
    done(err, user);
  });
});

passportModule(passport)

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);

app.listen(3000)

module.exports = app;
