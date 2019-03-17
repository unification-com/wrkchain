require("dotenv").config();
var express = require('express');
var app = express();

// set the view engine to ejs
app.set('view engine', 'ejs');

app.use('/',express.static(__dirname + '/public'));

// index page
app.get('/', function(req, res) {
    res.render('pages/index',{
        MAINCHAIN_WEB3_PROVIDER_URL: process.env.MAINCHAIN_WEB3_PROVIDER_URL,
        WRKCHAIN_ROOT_ABI: process.env.WRKCHAIN_ROOT_ABI,
        WRKCHAIN_ROOT_CONTRACT_ADDRESS: process.env.WRKCHAIN_ROOT_CONTRACT_ADDRESS,
        MAINCHAIN_EXPLORER_URL: process.env.MAINCHAIN_EXPLORER_URL,
        WRKCHAIN_ROOT_WRITE_TIMEOUT: process.env.WRKCHAIN_ROOT_WRITE_TIMEOUT,
        WRKCHAIN_NAME: process.env.WRKCHAIN_NAME
    });
});

// block validation page
app.get('/validate', function(req, res) {
    res.render('pages/validate',{
        WRKCHAIN_WEB3_PROVIDER_URL: process.env.WRKCHAIN_WEB3_PROVIDER_URL,
        MAINCHAIN_WEB3_PROVIDER_URL: process.env.MAINCHAIN_WEB3_PROVIDER_URL,
        WRKCHAIN_ROOT_CONTRACT_ADDRESS: process.env.WRKCHAIN_ROOT_CONTRACT_ADDRESS,
        WRKCHAIN_ROOT_ABI: process.env.WRKCHAIN_ROOT_ABI,
        BLOCK_NUM: req.query.block,
        WRKCHAIN_NAME: process.env.WRKCHAIN_NAME
    });
});

app.listen(process.env.WRKCHAIN_VALIDATOR_SERVICE_PORT);

console.log( "=====================================");
console.log( "= WRKCHAIN VALIDATOR SERVICE READY =");
console.log( "= ------------------------          =");
console.log( "=                                   =");
console.log( "= open:                             =");
console.log( "= http://localhost:" + process.env.WRKCHAIN_VALIDATOR_SERVICE_PORT + "             =");
console.log( "=                                   =");
console.log( "=====================================");