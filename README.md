# iml-update-check
iml-update-check

# Test
curl -v -H "x-forwarded-host: $HN" -d true --unix-socket /var/run/iml-update-handler.sock -X POST http://
