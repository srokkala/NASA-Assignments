const express = require('express');
const app = express();

const port = 3000;

//Serving the HTML File
app.get('/',(req,res) =>{
    res.sendFile('Fors.html',{root: __dirname});
});

// Serving the Local File
app.get('/list', (req,res) => {
    res.sendFile(__dirname + "/data.json");
});

// Display Which Port is Being Used
app.listen(port,() => console.log(`Listening on port ${port}`));

