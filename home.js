var express = require('express');
var bodyParser = require('body-parser');
//var multer = require('multer'); 
var app = express();
var handlebars = require('express-handlebars').create({defaultLayout:'main'});

app.use(express.static('public'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
//app.use(multer());

app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');
app.set('port', 50500);

app.get('/', function(req,res){
  res.render('crawler');
});

app.post('/test-page', function (req, res) {
    console.log("Should Show shit below");
    console.log(req.body);
    res.send(req.body);
});

app.use(function(req,res){
	res.status(404);
	res.render('404');
});

app.use(function(err, req, res, next){
	console.error(err.stack);
	res.type('plain/text');
	res.status(500);
	res.render('500');
});





app.listen(app.get('port'), function(){
	console.log('Express started on http://localhost:' + app.get('port') + '; press Ctrl-C to terminate.');
});

