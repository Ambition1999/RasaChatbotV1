import requests

sender = input("What's your name?\n")

bot_message = ""
while bot_message != "Bye":
    message = input("What's your message?\n")
    print("Sending message now...")
    if message is not None:
        tasks = {"sender": sender, "message": message}
        r = requests.post('http://localhost:5002/webhooks/rest/webhook', json = tasks)


        print("Bot says, ", end=' ')
        for i in r.json():
            bot_message = i['text']
            print(f"{i['text']}")