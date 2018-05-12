const express = require('express')
const path = require('path');

const app = express()

app.use(express.static(__dirname + '/public'))

app.get('/', function(req, res){
	res.sendFile(path.join(__dirname+'/public/index.html'))
})

app.listen(3050, () => console.log('MeasureMe static file server listening on port 3050'))