const url = require("url");
const fs = require("fs");

const http = require("http");
const https = require("https");

const ca = fs.readFileSync(process.env.IML_CA_PATH);

const port = process.env.LISTEN_PID > 0 ? { fd: 3 } : 8080;

const urlObj = url.parse(url.resolve(process.env.SERVER_HTTP_URL, "api/updates_available/"));

const config = Object.assign(
  {
    headers: {
      Authorization: `ApiKey ${process.env.API_USER}:${process.env.API_KEY}`,
      Accept: "application/json",
      "Content-type": "application/json"
    },
    ca: [ca],
    requestCert: true,
    method: "POST"
  },
  urlObj
);

http
  .createServer((req, res) => {
    let buff = "";

    req.on("error", err => {
      res.writeHead(400, { "Content-Type": "application/javascript" });
      res.end();
      console.error(`Request Failed: ${err}`);
    });

    const hn = req.headers["x-ssl-client-name"];

    req.on("data", d => {
      buff += d;
    });

    req.on("end", () => {
      let updatesAvail;

      try {
        updatesAvail = JSON.parse(buff);
      } catch (e) {
        res.writeHead(400, { "Content-Type": "application/javascript" });
        res.end();
        console.error(`Bad Request: hn: ${hn} data: ${buff} : ${e}`);
      }

      const r = https.request(config);

      r.on("error", err => {
        res.writeHead(500, { "Content-Type": "application/javascript" });
        res.end();
        console.error(`Failed to update (${updatesAvail}) for ${hn}: ${err}`);
      });
      r.write(
        JSON.stringify({
          host_address: hn,
          available: updatesAvail
        })
      );
      r.end(() => {
        if (res.finished) return;
        res.writeHead(200, { "Content-Type": "application/javascript" });
        res.end();
      });
    });
  })
  .listen(port);
