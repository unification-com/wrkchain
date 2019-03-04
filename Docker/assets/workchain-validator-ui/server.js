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
        WORKCHAIN_ROOT_ABI: process.env.WORKCHAIN_ROOT_ABI,
        WORKCHAIN_ROOT_CONTRACT_ADDRESS: process.env.WORKCHAIN_ROOT_CONTRACT_ADDRESS,
        MAINCHAIN_EXPLORER_URL: process.env.MAINCHAIN_EXPLORER_URL,
        WORKCHAIN_ROOT_WRITE_TIMEOUT: process.env.WORKCHAIN_ROOT_WRITE_TIMEOUT,
        WORKCHAIN_NAME: process.env.WORKCHAIN_NAME
    });
});

// block validation page
app.get('/validate', function(req, res) {
    res.render('pages/validate',{
        WORKCHAIN_WEB3_PROVIDER_URL: process.env.WORKCHAIN_WEB3_PROVIDER_URL,
        MAINCHAIN_WEB3_PROVIDER_URL: process.env.MAINCHAIN_WEB3_PROVIDER_URL,
        WORKCHAIN_ROOT_CONTRACT_ADDRESS: process.env.WORKCHAIN_ROOT_CONTRACT_ADDRESS,
        WORKCHAIN_ROOT_ABI: process.env.WORKCHAIN_ROOT_ABI,
        BLOCK_NUM: req.query.block,
        WORKCHAIN_NAME: process.env.WORKCHAIN_NAME
    });
});

app.listen(process.env.WORKCHAIN_VALIDATOR_SERVICE_PORT);

console.log( "=====================================");
console.log( "= WORKCHAIN VALIDATOR SERVICE READY =");
console.log( "= ------------------------          =");
console.log( "=                                   =");
console.log( "= open:                             =");
console.log( "= http://localhost:" + process.env.WORKCHAIN_VALIDATOR_SERVICE_PORT + "             =");
console.log( "=                                   =");
console.log( "=====================================");