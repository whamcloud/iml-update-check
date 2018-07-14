# IML Update Checker and Handler
iml-update-check
iml-update-handler

# Test Handler
curl -v -H "x-forwarded-host: $HN" -d true --unix-socket /var/run/iml-update-handler.sock -X POST http://
