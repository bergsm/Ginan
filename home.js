var express = require('express');
var bodyParser = require('body-parser');
var app = express();
var cookieParser = require('cookie-parser'); //had to install this module separately. NPM cookie-parser docs: https://expressjs.com/en/resources/middleware/cookie-parser.html
app.use(cookieParser());
var handlebars = require('express-handlebars').create({defaultLayout:'main'});
var fs = require('fs'); //this is for reading from a file

const spawn = require("child_process").spawnSync;

app.use(express.static('public'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');
app.set('port', 3030);

//template for creating a cookie taken from here: https://stackoverflow.com/questions/16209145/how-to-set-cookie-in-node-js-using-express-framework
//NOTE: very heavily relied upon as written for SO answer
// set a cookie
app.use(function (req, res, next) {
   // check if client sent cookie
     var cookie = req.cookies.graph_session;
     if (cookie === undefined)
     {
     	// no: set a new cookie
     	// use random number for proof of concept
        var randomNumber=Math.random().toString();
        randomNumber=randomNumber.substring(2,randomNumber.length);
        //read the file synchronously. Was having trouble with async... source: https://stackoverflow.com/questions/10058814/get-data-from-fs-readfile
	var graph_session_data = fs.readFileSync('./public/graph_session', 'utf8'); //will need to change this, I was writing to a file graph_session in BFS script
	//was the data read correctly?
	console.log(graph_session_data);
	//set the cookie
        res.cookie('graph_session',randomNumber, { maxAge: 900000, httpOnly: false });
        console.log('cookie created successfully');
	console.log(req.cookies.graph_session);
     } 
     else
     {
     	// yes, cookie was already present 
        console.log('cookie exists', cookie);
     } 
     next();
});

app.get('/', function(req,res){
  //log the cookie data. Source: https://stackoverflow.com/questions/39615479/cookies-undefined-on-node-js-express-localhost
  console.log(req.cookies.graph_session);
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

