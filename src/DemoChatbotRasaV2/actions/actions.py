# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType
from rasa_sdk.events import SlotSet
import json
import re
import sqlite3
import pyodbc
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

# CONNECT TO SQLITE
sqliteConnection = sqlite3.connect(r'C:\Users\toan.le\Documents\Gitlab\certifiredml\Chatbot\RasaChatbotV2\testrasa.db')
cursor = sqliteConnection.cursor()
print("Database created and Successfully Connected to SQLite")

# CONNECT TO SQL SERVER
server = "PC-TOANLE"
database = "ChatbotRasa"
username = "sa"
password = "sa2012"
cnxn_sqlserver = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor_sqlserver = cnxn_sqlserver.cursor()
print("Successfully Connected to SQL Server")


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
            dispatcher.utter_message(text = "I don't have any information about {}.".format(text))
        return [SlotSet('language',None,None)]


class ActionAskHelp(Action):

    def name(self) -> Text:
        return "action_answer_help"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = {
            "text": "How can i help you? There are a few things I can do below: ",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "Talking with you",
                    "payload": "Hi, are you a bot?",
                },
                {
                    "content_type": "text",
                    "title": "View products",
                    "payload": "Products catalog",
                },
                {
                    "content_type": "text",
                    "title": "View Contact",
                    "payload": "view contact",
                }
            ]

        }
        dispatcher.utter_message(json_message=message)

        return []


class ActionAskContact(Action):

    def name(self) -> Text:
        return "action_answer_contact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        button_call = {
            "type": "phone_number",
            "title": "Call to helpdesk",
            "payload": "0123456789",
        }
        button_view_website = {
            "type": "web_url",
            "url": "https://github.com/Ambition1999",
            "title": "View website",
        }
        button_more = {
            "type": "postback",
            "title": "Need more?",
            "payload": "more",
        }
        response_message = "You can contact via below methods:"
        dispatcher.utter_message(text=response_message, buttons=[button_call,button_view_website,button_more])

        return []


class ActionAskProducts(Action):

    def name(self) -> Text:
        return "action_answer_products"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sqlite_select_Query = '''SELECT * from Products'''
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()

        # Add product into product list
        product_list = []
        for result in record:
            id = result[0]
            name = result[1].lower()
            des = result[2]
            img_url = result[3]
            price = result[4]
            link = result[5]
            product = {
                "id": id,
                "name": name,
                "intro": des,
                "img_url": img_url,
                "price": price,
                "link": link,
            }
            product_list.append(product)

        # Add product into template items
        template_items = []
        for product in product_list:
            template_item = {
                "title": product["name"],
                "image_url": product["img_url"],
                "subtitle": product["intro"] + " - " + str(product["price"]) + "$",
                "default_action": {
                    "type": "web_url",
                    "url": product["link"],
                    "webview_height_ratio": "full"
                },
                "buttons": [
                    {
                        "type": "web_url",
                        "url": product["link"],
                        "title": "View details"
                    },
                    {
                        "type": "web_url",
                        "url": "https://www.now.vn/",
                        "title": "Shop now"
                    }
                ]
            }
            template_items.append(template_item)

        message_str = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": template_items
                }
            }
        }

        ret_text = "Hi! I show you some of items below: "
        print(message_str)
        dispatcher.utter_message(text=ret_text, json_message=message_str)
        return []


class ActionAskAboutYou(Action):

    def name(self) -> Text:
        return "action_answer_about_you"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Data test, need read product info from database
        details_list = []
        product_01 = {
            "name": "Product 1",
            "img_url": "https://api.time.com/wp-content/uploads/2018/11/sweetfoam-sustainable-product.jpg?quality=85",
            "intro": "Rainbow Sandals",
            "link": "https://github.com/Ambition1999",
        }
        product_02 = {
            "name": "Product 2",
            "img_url": "https://cdn.shopify.com/s/files/1/0070/7032/files/camera_56f176e3-ad83-4ff8-82d8-d53d71b6e0fe.jpg?v=1527089512",
            "intro": "Pro Camera",
            "link": "https://github.com/Ambition1999",
        }
        product_03 = {
            "name": "Product 3",
            "img_url": "https://www.roudstudio.com/images/works/product-photo/img01.jpg",
            "intro": "Elegant Watches",
            "link": "https://github.com/Ambition1999",
        }
        product_04 = {
            "name": "Product 1",
            "img_url": "https://api.time.com/wp-content/uploads/2018/11/sweetfoam-sustainable-product.jpg?quality=85",
            "intro": "Rainbow Sandals",
            "link": "https://github.com/Ambition1999",
        }
        product_05 = {
            "name": "Product 2",
            "img_url": "https://cdn.shopify.com/s/files/1/0070/7032/files/camera_56f176e3-ad83-4ff8-82d8-d53d71b6e0fe.jpg?v=1527089512",
            "intro": "Pro Camera",
            "link": "https://github.com/Ambition1999",
        }
        product_06 = {
            "name": "Product 3",
            "img_url": "https://www.roudstudio.com/images/works/product-photo/img01.jpg",
            "intro": "Elegant Watches",
            "link": "https://github.com/Ambition1999",
        }
        product_07 = {
            "name": "Product 1",
            "img_url": "https://api.time.com/wp-content/uploads/2018/11/sweetfoam-sustainable-product.jpg?quality=85",
            "intro": "Rainbow Sandals",
            "link": "https://github.com/Ambition1999",
        }
        product_08 = {
            "name": "Product 2",
            "img_url": "https://cdn.shopify.com/s/files/1/0070/7032/files/camera_56f176e3-ad83-4ff8-82d8-d53d71b6e0fe.jpg?v=1527089512",
            "intro": "Pro Camera",
            "link": "https://github.com/Ambition1999",
        }
        product_09 = {
            "name": "Product 3",
            "img_url": "https://www.roudstudio.com/images/works/product-photo/img01.jpg",
            "intro": "Elegant Watches",
            "link": "https://github.com/Ambition1999",
        }
        details_list.extend([product_01, product_02, product_03, product_04, product_05, product_06, product_07, product_08, product_09])

        template_items = []
        for product in details_list:
            template_item = {
                "title": product["name"],
                "image_url": product["img_url"],
                "subtitle": product["intro"],
                "default_action": {
                    "type": "web_url",
                    "url": product["link"],
                    "webview_height_ratio": "tall"
                    # "messenger_extensions": True
                },
                "buttons": [
                    {
                        "type": "web_url",
                        "url": product["link"],
                        "title": "View details",
                        # "webview_height_ratio": "compact",
                        # "messenger_extensions": True
                    },
                    {
                        "type": "web_url",
                        "url": "https://www.now.vn/",
                        "title": "Shop now",
                    }
                ]
            }
            template_items.append(template_item)

        message_str = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    # "top_element_style": "large",
                    "elements": template_items,
                    # "buttons": [
                    #     {
                    #         "title": "View More",
                    #         "type": "postback",
                    #         "payload": "payload"
                    #     }
                    # ]
                }
            }
        }

        ret_text = "Hi! I show you some of items below: "
        print(message_str)
        dispatcher.utter_message(text=ret_text, json_message=message_str)
        return []


# Opening message to introduce yourself and give some action for user can do
class ActionOpeningMessage(Action):

    def name(self) -> Text:
        return "action_opening_message"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Define object information
        fire_protection_knowledge = {
            "title": "Know about Fire Safety and Protection Equipments",
            "subtitle": "",
            "img_url": "https://i.pinimg.com/originals/4d/1d/07/4d1d0783837b1eea6cca219e83094e96.jpg"
        }

        fire_protection_equipments = {
            "title": "View some new Fire Protection Equipments",
            "subtitle": "",
            "img_url": "https://frankscope.co.ke/storage/images/fire-fighting-equipment_1559207151.jpg"
        }

        contacts = {
            "title": "View contacts",
            "subtitle": "",
            "img_url": "https://apmlromania.com/EN/wp-content/uploads/2018/04/contact.jpg"
        }

        message_str = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    # "top_element_style": "compact",
                    "elements": [
                      {
                        "title": fire_protection_knowledge["title"],
                        # "subtitle": fire_protection_knowledge["subtitle"],
                        "image_url": fire_protection_knowledge["img_url"],
                        "buttons": [
                            {
                                "title": "View more",
                                "type": "postback",
                                "payload": '/ask_fire_protection'
                            }
                        ]
                      },
                      {
                        "title": fire_protection_equipments["title"],
                        # "subtitle": fire_protection_equipments["subtitle"],
                        "image_url": fire_protection_equipments["img_url"],
                        "buttons": [
                            {
                                "title": "View more",
                                "type": "postback",
                                "payload": '/ask_fire_safety_and_protection_equipment_items'
                            }
                        ]
                      },
                      {
                        "title": contacts["title"],
                        # "subtitle": contacts["subtitle"],
                        "image_url": contacts["img_url"],
                        "buttons": [
                            {
                                "title": "View more",
                                "type": "postback",
                                "payload": "/ask_contact"
                            }
                        ]
                      },
                    ]
                }
            }
        }
        print(message_str)
        dispatcher.utter_message(text="Hi there! I'm a Fire Assistant")
        dispatcher.utter_message(text="I have knowledge about Fire Protection 💥💥💥 and Fire Protection Equipments 🧯🧯🧯")
        dispatcher.utter_message(text="How can I help you?", json_message=message_str)
        return []


class ActionAskFireProtection(Action):

    def name(self) -> Text:
        return "action_answer_fire_protection"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        define_of_fire_protection_01 = """"Fire protection is the study and practice of mitigating the unwanted effects of potentially destructive fires 🔥🔥🔥.
\nIt involves the study of the behaviour, compartmentalisation, suppression and investigation of fire and its related emergencies, as well as the research and development, production, testing and application of mitigating systems. 
\nIn structures, be they land-based, offshore or even ships, the owners and operators are responsible to maintain their facilities in accordance with a design-basis that is rooted in laws, including the local building code and fire code, which are enforced by the Authority Having Jurisdiction.
"""
        define_of_fire_protection_02 = """"Buildings must be constructed in accordance with the version of the building code that is in effect when an application for a building permit is made. 
        Building inspectors check on compliance of a building under construction with the building code. Once construction is complete, a building must be maintained in accordance with the current fire code, which is enforced by the fire prevention officers of a local fire department. 
        In the event of fire emergencies, Firefighters, fire investigators, and other fire prevention personnel are called to mitigate, investigate and learn from the damage of a fire. Lessons learned from fires are applied to the authoring of both building codes and fire codes.
                                        """

        message = {
            "text": "So, what do you want to know next? ",
            "quick_replies": [
                {
                    "content_type": "text",
                    # "title": "Protect equipments ?",
                    # "payload": "what is fire safety and protection equipments",
                    "title": "Protect equipments?",
                    "payload": '/ask_fire_safety_and_protection_equipment'
                },
                {
                    "content_type": "text",
                    # "title": "View protect equipment items",
                    # "payload": "show me fire safety and protection equipment items",
                    "title": "View product items 👀",
                    "payload": '/ask_fire_safety_and_protection_equipment_items'
                }
            ]

        }
        dispatcher.utter_message(text=define_of_fire_protection_01)
        # dispatcher.utter_message(text=define_of_fire_protection_02)
        dispatcher.utter_message(image="https://media.tenor.com/images/7a17952f62ac88e6a8a2edf2af544836/tenor.gif")
        dispatcher.utter_message(json_message=message)

        return []


class ActionAskFireSafetyAndProtectionEquipments(Action):

    def name(self) -> Text:
        return "action_answer_fire_safety_and_protection_equipments"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        define_of_fire_safety_and_protection_equipments = """"Fire safety and protection equipment is used for extinguishing fires, preventing flames from spreading, and helping people escape fires 🔥🔥🔥.
📣 - Escape ladders attach to window sills to provide an emergency escape route from the upper level of a building.
📣 - Fire-barrier products (also called fire stops) help prevent the spread of fire and smoke.
📣 - Fire blankets smother small fires or provide a protective wrap to shield someone from a fire.
📣 - Fire extinguishers spray water or chemical agents for putting out small fires. 
📣 - Fire hoses and fire-hose nozzles connect to a pressurized supply of water or fire retardant for extinguishing large fires. 
📣 - Fire-probing tools includes axes, hammers, pikes, and other equipment for breaking down walls, poking through roofs, and locating smoldering fires.
📣 - Fire-resistant treatments coat surfaces to help stop flames from spreading in the event of a fire. 
"""

        message = {
            "text": "Wanna view production equipment items? ",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "View product items",
                    "payload": '/ask_fire_safety_and_protection_equipment_items'
                }
            ]

        }
        dispatcher.utter_message(text=define_of_fire_safety_and_protection_equipments)
        dispatcher.utter_message(json_message=message)

        return []


class ActionAskViewProtectionEquipmentItems(Action):

    def name(self) -> Text:
        return "action_answer_view_protection_equipment_items"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        cnxn_sqlserver = '''SELECT * from Products'''
        cursor_sqlserver.execute(cnxn_sqlserver)
        record = cursor_sqlserver.fetchall()
        print(record)

        # Add product into product list
        product_list = []
        for result in record:
            id = result[0]
            name = result[1]
            des = result[3]
            img_url = result[2]
            price = result[5]
            link = result[4]
            product_type_id = result[6]
            product = {
                "id": id,
                "name": name,
                "intro": des,
                "img_url": img_url,
                "price": price,
                "link": link,
                "product_type_id": product_type_id
            }
            product_list.append(product)

        # Add product into template items
        template_items = []
        for product in product_list:
            template_item = {
                "title": product["name"],
                "image_url": product["img_url"],
                "subtitle": product["intro"] + "-" + str(product["price"]) + "$",
                "default_action": {
                    "type": "web_url",
                    "url": product["link"],
                    "webview_height_ratio": "full"
                },
                "buttons": [
                    {
                        "type": "web_url",
                        "url": product["link"],
                        "title": "View details"
                    },
                    {
                        "type": "web_url",
                        "url": product["link"],
                        "title": "Shop now"
                    }
                ]
            }
            template_items.append(template_item)

        message_str = {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": template_items
                }
            }
        }

        ret_text = "Hi! I show you some of items below: "
        print(message_str)
        dispatcher.utter_message(text=ret_text, json_message=message_str)
        return []


class ActionGoodbye(Action):

    def name(self) -> Text:
        return "action_goodbye"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = {
            "text": "Please rate the conversation:",
            "quick_replies": [
                {
                    "content_type": "text",
                    "title": "⭐⭐⭐⭐⭐",
                    "payload": '/rating_conversation'
                },
                {
                    "content_type": "text",
                    "title": "⭐⭐⭐⭐",
                    "payload": 'rate conversation'
                },
                {
                    "content_type": "text",
                    "title": "⭐⭐⭐",
                    "payload": 'rate conversation'
                },
                {
                    "content_type": "text",
                    "title": "⭐⭐",
                    "payload": 'rate conversation'
                },
                {
                    "content_type": "text",
                    "title": "⭐",
                    "payload": 'rate conversation'
                }
            ]
        }
        dispatcher.utter_message(json_message=message)

        return []

# icon ☎️📸 🤔🤔🤔