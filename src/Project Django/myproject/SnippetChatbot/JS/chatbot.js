var messages = [], //array that hold the record of each string in chat
  lastUserMessage = "",
  botMessage = "",
  botName = 'Rasa chatbot', userClass = "chatlog-user", botClass = "chatlog-bot",
  conversationId = "";
  talking = true;

async function newEntry() {
  if (document.getElementById("chatbox").value != "") {
    lastUserMessage = document.getElementById("chatbox").value; //get element in text input
    document.getElementById("chatbox").value = "";
    console.log("Last user message is: " + lastUserMessage);
    var objectUserMessage = {role: "user", message: lastUserMessage};
    messages.push(objectUserMessage);
    displayMessage();
    //messages.push(lastUserMessage);
    var res = await $.ajax({
        type: 'POST',
        url: "http://localhost:5002/webhooks/rest/webhook",
        data: JSON.stringify({
            sender: checkConversationId(),
            message: lastUserMessage
        }),
        error: function(e) {
            console.log(e);
        },
        dataType: "json",
        contentType: "application/json"
    });

    console.log("Response data: ", res);
    res.forEach(myFunction);
    function myFunction(item){
        var objectMessage = {role: "bot", message: item["text"]};
        messages.push(objectMessage);
        //messages.push("<b>" + botName + ":</b> " + item["text"]);

    }
    displayMessage();
    // for (var i = 1; i < 11; i++) {
    //   if (messages[messages.length - i] && typeof messages[messages.length - i] === 'object' && messages[messages.length - i] !== null){
    //        document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i]["message"];
    //     if(messages[messages.length - i]["role"] == "user"){
    //         document.getElementById("chatlog" + i).setAttribute("class",userClass);
    //     }else{
    //         document.getElementById("chatlog" + i).setAttribute("class",botClass);
    //     }
    //   }
    // }
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

function displayMessage(){
    for (var i = 1; i < 11; i++) {
      if (messages[messages.length - i] && typeof messages[messages.length - i] === 'object' && messages[messages.length - i] !== null){
           document.getElementById("chatlog" + i).innerHTML = messages[messages.length - i]["message"];
        if(messages[messages.length - i]["role"] == "user"){
            document.getElementById("chatlog" + i).setAttribute("class",userClass);
        }else{
            document.getElementById("chatlog" + i).setAttribute("class",botClass);
        }
      }
    }
}

function clearPlaceHolder() {
  document.getElementById("chatbox").placeholder = "";
}

function checkConversationId(){
    if(conversationId !== null && conversationId !== ""){ //If have conversation id
        console.log("Set conversation id: " + conversationId);
        return conversationId;
    }
    else{
        return generateConversationId(); //If don't have conversation id => Generate and save to cookie
    }
}

function generateConversationId(){
    if(getCookie("ConversationId") !== "")
    {
        conversationId = getCookie("ConversationId");
        console.log("Get conversation id from cookie: " + conversationId);
        return conversationId;
    }else{
        var uid = generateUID();
        conversationId = uid;
        console.log("Generate/set conversation id: " + conversationId)
        setCookie("ConversationId",conversationId,0.5);
        return conversationId;
    }
}

function generateUID(){
    var navigator_info = window.navigator;
    var screen_info = window.screen;
    var uid = navigator_info.mimeTypes.length;
    uid += navigator_info.userAgent.replace(/\D+/g, '');
    uid += navigator_info.plugins.length;
    uid += screen_info.height || '';
    uid += screen_info.width || '';
    uid += screen_info.pixelDepth || '';
    console.log(uid);
    return uid;
}