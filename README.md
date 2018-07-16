# IML Update Checker and Handler

[![Build Status](https://travis-ci.com/whamcloud/iml-update-check.svg?branch=master)](https://travis-ci.com/whamcloud/iml-update-check)

This repo provides rpm update alerts for agents -> manager

It consists of two projects:

iml-update-check
iml-update-handler

## Test Handler

`curl -v -H "x-forwarded-host: $HN" -d true --unix-socket /var/run/iml-update-handler.sock -X POST http://`
