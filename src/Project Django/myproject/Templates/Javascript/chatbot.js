var messages = [], //array that hold the record of each string in chat
  lastUserMessage = "",
  botMessage = "",
  botName = 'Rasa chatbot',
  talking = true;

async function newEntry() {
  if (document.getElementById("chatbox").value != "") {
    lastUserMessage = document.getElementById("chatbox").value;
    document.getElementById("chatbox").value = "";
    console.log("Last user message is: " + lastUserMessage)
    messages.push(lastUserMessage);
    var res = await $.ajax({
        type: 'POST',
        url: "http://localhost:5002/webhooks/rest/webhook",
        data: JSON.stringify({
            sender: "abcd1234",
            message: lastUserMessage
        }),
        error: function(e) {
            console.log(e);
        },
        dataType: "json",
        contentType: "application/json"
    });

    // console.log("Response data: ", res);
    res.forEach(myFunction);
    function myFunction(item){
        messages.push("<b>" + botName + ":</b> " + item["text"]);
    }
    for (var i = 1; i < 8; i++) {
      if (messages[messages.length - i])
        document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i];
    }
  }
}

// //text to Speech
// //https://developers.google.com/web/updates/2014/01/Web-apps-that-talk-Introduction-to-the-Speech-Synthesis-API
// function Speech(say) {
//   if ('speechSynthesis' in window && talking) {
//     var utterance = new SpeechSynthesisUtterance(say);
//     //msg.voice = voices[10]; // Note: some voices don't support altering params
//     //msg.voiceURI = 'native';
//     //utterance.volume = 1; // 0 to 1
//     //utterance.rate = 0.1; // 0.1 to 10
//     //utterance.pitch = 1; //0 to 2
//     //utterance.text = 'Hello World';
//     //utterance.lang = 'en-US';
//     speechSynthesis.speak(utterance);
//   }
// }

document.onkeypress = keyPress;
function keyPress(e) {
  var x = e || window.event;
  var key = (x.keyCode || x.which);
  if (key == 13 || key == 3) {
    newEntry();
  }
  if (key == 38) {
    console.log('hi');
  }
}

function clearPlaceHolder() {
  document.getElementById("chatbox").placeholder = "";
}