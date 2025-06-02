let sentiment;
let speech;
let currentText = "";
let resultLabel = "";

function setup() {
  createCanvas(900, 900);
  background(200);
  textAlign(CENTER, CENTER);
  textSize(24);

  // Load the sentiment model
  sentiment = ml5.sentiment('movieReviews', modelReady);

  // Start speech recognition
  speech = new p5.SpeechRec('en-US', gotSpeech);
  speech.continuous = true;
  speech.interimResults = false;
  speech.start();
}

function modelReady() {
  console.log('Sentiment model ready!');
}

function gotSpeech() {
  if (speech.resultValue) {
    currentText = speech.resultString;
    analyzeSentiment(currentText);
  }
}

function analyzeSentiment(text) {
  let prediction = sentiment.predict(text);
  resultLabel = prediction.score > 0.5 ? "😊 Positive" : "😠 Negative";
  if (prediction.score > 0.5) {
    background(0, 200, 100); // Green
  } else {
    background(200, 50, 50); // Red
  }
}

function draw() {
  fill(255);
  text("You said: " + currentText, width/2, height/2 - 30);
  text("Sentiment: " + resultLabel, width/2, height/2 + 30);
}

