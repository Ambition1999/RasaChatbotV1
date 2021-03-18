# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType
from rasa_sdk.events import SlotSet
import json
import re
import sqlite3
import random
import datetime as dt

import country_api

DATABASE = ["talking with you",
            "asking with you",
            "working with you",
            "remind you of your schedule",
            "show current time",
            "chatting with you"]

class ActionShowTime(Action):

    def name(self) -> Text:
        return "action_show_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        date_time = dt.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        dispatcher.utter_message(text=f"Current time is: {date_time}")
        return []

class ActionShowCountry(Action):

    def name(self) -> Text:
        return "action_show_country"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text=country_api.Weather('vietnam'))
        return []


class ActionRecommend(Action):

    def name(self) -> Text:
        return "action_recommend"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food = []
        for i in range(2):
            food_number = random.randrange(len(DATABASE))
            food.append(DATABASE[food_number])

        dispatcher.utter_message(
            text="I can '{}' or '{}'...".format(food[0], food[1]))

        return []

sqliteConnection = sqlite3.connect(r'C:\Users\toan.le\Documents\DemoChatbotRasaV2\testrasa.db')
cursor = sqliteConnection.cursor()
print("Database created and Successfully Connected to SQLite")
# sqlite_select_Query = '''SELECT * from cars'''
# cursor.execute(sqlite_select_Query)
# print(cursor.fetchall())
# record = cursor.fetchall()
# text_input = "audi price?"
# check = False
# for result in record:
#     id = result[0]
#     name = result[1].lower()
#     price = result[2]
#     print(id,name,price)
#     if name in text_input:
#         check = True
#         print("Price of '{}' is: '{}'".format(name,price))
# if not check:
#     print("Product was not found!!!")


class ActionAskKnowledgeBaseCar(Action):
    def name(self) -> Text:
        return "action_custom_car"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # text = tracker.latest_message['text']
        # text_input = text.lower()
        sqlite_select_Query = '''SELECT * from Cars LIMIT 5'''
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        # check = False
        # print(text_input)
        text_result = "Top 5 cars is: \n"
        for result in record:
            id = result[0]
            name = result[1].lower()
            price = result[2]
            # if name in text_input:
            #     check = True
            #     dispatcher.utter_message(text = "Price of {} is: {} $".format(name,price))
            # check = True
            text_result += "Id: {}, Name: {}, Price {} $\n".format(id,name,price)
            # dispatcher.utter_message(text = "Price of {} is: {} $".format(name,price))
        # if not check:
        #     dispatcher.utter_message(text = "Product was not found!!!")
        dispatcher.utter_message(text=text_result)
        # return [SlotSet("car", price)]
        return []

class ActionSubmitPersonalForm(Action):
    def name(self) -> Text:
        return "action_submit_personal_form"

    def run(self,dispatcher,
            tracker: Tracker,
            domain: "DomainDict",) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_details_thanks",
                                 Name=tracker.get_slot("full_name"),
                                 Mobile_number=tracker.get_slot("phone_number"))

class ActionSubmitPersonalForm(Action):
    def name(self) -> Text:
        return "action_submit_programing_language_form"

    def run(self,dispatcher,
            tracker: Tracker,
            domain: "DomainDict",) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_slots_values",
                                 Language=tracker.get_slot("language"),
                                 Application_Type=tracker.get_slot("application_type"),
                                 Learning_Time=tracker.get_slot("learning_time"))

class ActionAskKnowledgeBaseProgramingLanguage(Action):
    def name(self) -> Text:
        return "action_answer_programing_language"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        text = tracker.get_slot('language')
        if text is None or text is '':
            dispatcher.utter_message(text="What programing language to want to know?")
        text_input = text.lower()
        sqlite_select_Query = '''SELECT * from ProgramingLanguages'''
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        check = False
        print("Tracker is",text_input)
        for result in record:
            id = result[0]
            name = result[1].lower()
            des = result[2]
            link = result[3]
            if name in text_input:
                check = True
                dispatcher.utter_message(text = "Programing language: {}\nConception: {}\nMore information:{}".format(name,des,link))
                break
        if not check:
            dispatcher.utter_message(text = "I don't information about {}.".format(text))
        return [SlotSet('language',None,None)]


# text = 'java'
# text_input = text.lower()
# sqlite_select_Query = '''SELECT * from ProgramingLanguages'''
# cursor.execute(sqlite_select_Query)
# record = cursor.fetchall()
# check = False
# for result in record:
#     id = result[0]
#     name = result[1].lower()
#     des = result[2]
#     link = result[3]
#     if name in text_input:
#         check = True
#         print("name is", name)
#         print("Language is: {}\nConception: {}\nMore information:{}".format(name, des, link))
#         break
# if not check:
#     print("I don't information about {}.".format(text))