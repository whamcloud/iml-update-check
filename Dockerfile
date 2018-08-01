FROM node:alpine
WORKDIR /usr/src/app
COPY handler.js .
EXPOSE 8080

COPY wait-for-settings.sh /usr/local/bin/
ENTRYPOINT [ "wait-for-settings.sh" ]

CMD ["node", "./handler.js"]
