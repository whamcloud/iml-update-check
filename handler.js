const url = require('url');
const fs = require('fs');

const http = require('http');
const https = require('https');

const ca = fs.readFileSync(process.env.IML_CA_PATH);

var port = process.env.LISTEN_PID > 0 ? { fd: 3 } : '/var/run/iml-update-handler.sock';
http.createServer( (req, res) => {
    var buff = "";

    req.on('error', (err) => {
	res.writeHead(400, {'Content-Type': 'application/javascript'});
	res.end();
	console.error("Request Failed: "+err);
    });

    const hn = req.headers['x-forwarded-host'];

    req.on('data', (d) => {
	buff += d;
    });

    req.on('end', () => {
	var update = url.parse(url.resolve(process.env.SERVER_HTTP_URL, "api/updates_available/"));
	update.headers = { "Authorization": 'ApiKey '+process.env.API_USER+':'+process.env.API_KEY,
			   "Accept": "application/json",
			   "Content-type": "application/json" };
	update.ca = [ ca ];
	update.requestCert = true;
	update.method = 'POST';

	var updatesAvail;
	try {
	    updatesAvail = JSON.parse(buff);
	} catch (e) {
	    res.writeHead(400, {'Content-Type': 'application/javascript'});
	    res.end();
	    console.error("Bad Request: hn:"+hn+" data:`"+buff+"' : "+e);
	    return;
	}

	var r = https.request(update);
	r.on('error', (err) => {
	    res.writeHead(500, {'Content-Type': 'application/javascript'});
	    res.end();
	    console.error("Failed to update ("+updatesAvail+") for "+hn+": "+err);
	});
	r.write(JSON.stringify({ host_address: hn,
				 available: updatesAvail }));
	r.end( () => {
	    if (res.finished)
		return;
	    res.writeHead(200, {'Content-Type': 'application/javascript'});
	    res.end();
	});

    });

}).listen(port);
