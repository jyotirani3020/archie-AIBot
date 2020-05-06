var SpeechRecognition = window.webkitSpeechRecognition;
  
var recognition = new SpeechRecognition();

var Textbox = $('#textInput');
var instructions = $('instructions');

var Content = '';

recognition.continuous = true;

recognition.onresult = function(event) {

  var current = event.resultIndex;

  var transcript = event.results[current][0].transcript;
 
    Content += transcript;
    Textbox.val(Content);
  
};

recognition.onstart = function() { 
  instructions.text('Voice recognition is ON.');
}

recognition.onspeechend = function() {
  instructions.text('No activity.');
}

recognition.onerror = function(event) {
  if(event.error == 'no-speech') {
    instructions.text('Try again.');  
  }
}

$('#start-btn').on('click', function(e) {
  if (Content.length) {
    Content += ' ';
  }
  recognition.start();
});

$('#stop-btn').on('click', function(e) {
  
  recognition.stop();
  
  Content = ''

  getBotResponse();
 
});

Textbox.on('userInput',function() {
  Content = $(this).val();
})






//typing
function getBotResponse() {
  var rawText = $("#textInput").val();
  var userHtml = '<p class="userText"><span>' + rawText + "</span></p>";
  $("#textInput").val("");
  $("#chatbox").append(userHtml);
  document
    .getElementById("userInput")
    .scrollIntoView({ block: "start", behavior: "smooth" });
  $.get("/get", { msg: rawText }).done(function(data) {
  var botHtml = '<p class="botText"><span>' + data + "</span></p>";
  var tts = data;
  $("#chatbox").append(botHtml);

  var msg = new SpeechSynthesisUtterance();
  var voices = window.speechSynthesis.getVoices();
  msg.voice = voices[50];
  msg.lang = 'en-GB'
  msg.text = tts;
  speechSynthesis.speak(msg);
  document
    .getElementById("userInput")
    .scrollIntoView({ block: "start", behavior: "smooth" });
    
      
  });
}
$("#textInput").keypress(function(e) {
  if (e.which == 13) {
    getBotResponse();
    
  }
});




  

