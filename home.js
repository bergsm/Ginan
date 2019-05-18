var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var handlebars = require('express-handlebars').create({defaultLayout:'main'});

const spawn = require("child_process").spawnSync;

app.use(express.static('public'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');
app.set('port', 3030);


app.get('/', function(req,res){
  res.render('crawler');
});

app.post('/test-page', function (req, res) {
    console.log(req.body);
    //res.send(req.body);
    if (req.body.search_type == 'DFS') {
        const pythonProcess = spawn('python',["./public/DFT.py", req.body.starting_url, req.body.crawl_limit]);
        res.render('crawler');
    }
    else {
	const pythonProcess = spawn('python', ["./public/breadthFirstSearch.py", req.body.starting_url, req.body.crawl_limit, req.body.keywordInput]);
	res.render('crawler');
    }
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

