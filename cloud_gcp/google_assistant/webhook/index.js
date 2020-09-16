    'use strict';

    const functions = require('firebase-functions');
    const {WebhookClient} = require('dialogflow-fulfillment');
    const {Card, Suggestion} = require('dialogflow-fulfillment');

    var admin = require("firebase-admin");

    //var serviceAccount = require("dankers-firebase-adminsdk-r85r7-df645bc8df.json");
    //admin.initializeApp({
    //  credential: admin.credential.cert(serviceAccount),
    //  databaseURL: "https://dankers.firebaseio.com"
    //});

    //var db = admin.firestore();

    process.env.DEBUG = 'dialogflow:debug'; // enables lib debugging statements

    exports.dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
      const agent = new WebhookClient({ request, response });
      console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
      console.log('Dialogflow Request body: ' + JSON.stringify(request.body));

      function welcome(agent) {
        agent.add(`Welcome to my agent!`);
      }

      function fallback(agent) {
        agent.add(`I didnt understand`);
        agent.add(`Im sorry, can you try again?`);
      }

      function setLights(agent) {
        agent.add(`Responds from webhook`);

        process.stdout.write("hello: ");

        //let devices = db.collection("devices");

        //process.stdout.write("devices: %j", devices);
      }

      // Run the proper function handler based on the matched Dialogflow intent name
      let intentMap = new Map();
      intentMap.set('Default Welcome Intent', welcome);
      intentMap.set('Default Fallback Intent', fallback);
      intentMap.set('home automation', setLights);

      agent.handleRequest(intentMap);
    });
