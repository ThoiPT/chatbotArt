# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
import mysql.connector
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
#
from actions.db_connect import DataProduct
from actions.settinghost import connect


class action_detail_product(Action):

    def name(self) -> Text:
        return "action_detail_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product_choice = tracker.latest_message['entities'][0]['value'] ## get Entities
        
        ## MySQL query connect
        mycursor = connect.cursor()    
        sqlQuery = "SELECT name, sellPrice FROM products WHERE name LIKE '{}'".format(product_choice) 
        mycursor.execute(sqlQuery)
        results = mycursor.fetchall()

        price = results[0][2] ## Lấy giá tiền
        format_price = "{:,.0f}đ".format(price) ## Xử lý giá tiền 
        
        dispatcher.utter_message("Sản phẩm {} \n - Kích thước : {}".format(results[0][0], results[0][1], format_price))

        return []
        

class action_price(Action):
    def name(self) -> Text:
        return "action_price"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            product = str(tracker.latest_message['entities'][0]['value']) ## get Entitiess
            try:               
                attribute = str(tracker.latest_message['entities'][1]['value']) ## get Entitiess
            except:
                attribute = "Lỗi"
           
            print("- product: " + product + "\n - nattribute: " + attribute)

            ## MySQL query connect
            mycursor = connect.cursor()    
            sqlQuery = "SELECT sellPrice FROM products WHERE name LIKE '{}'".format(product) 
            mycursor.execute(sqlQuery)
            results = mycursor.fetchall()

            # Định nghĩa keyword hỏi về giá
            listOfAttr = ['giá', 'giá sao', 'bán sao', 'nhiêu tiền']
            inputKey = attribute

            for i in listOfAttr:
                if i == inputKey:
                    attribute = inputKey
                else:
                    attribute = ""

            if attribute:
                price = results[0][0] ## Lấy giá tiền
                format_price = "{:,.0f}đ".format(price) ## Xử lý giá tiền
                dispatcher.utter_message(response="utter_rep_price", price=format_price)
            else:
                dispatcher.utter_message("Mình chưa hiểu ý bạn cần, bạn có thể nói rõ hơn không!")
        
            return []

class action_size(Action):
    def name(self) -> Text:
        return "action_size"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            product_choice = tracker.latest_message['entities'][0]['value'] ## get Entities
            # print(product_choice)
            ## MySQL query connect
            mycursor = connect.cursor()    
            sqlQuery = "SELECT size FROM products WHERE name LIKE '{}'".format(product_choice) 
            mycursor.execute(sqlQuery)
            results = mycursor.fetchall()

            size = results[0][0] ## Lấy giá tiền  
            if product_choice:
                dispatcher.utter_message(response="utter_rep_size", size = size) 
            else:
                dispatcher.utter_message("sorry") 
            return []

# # --------------------------------------------------------------------------
class action_show_product(Action):

    def name(self) -> Text:
        return "action_show_product"

    def run(self, dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "Dict[Text, Any]") -> List[Dict[Text, Any]]:
        # name_category = tracker.get_slot('name_category')
        s = " "
        products = DataProduct(tracker.get_slot("name_products"))
        for p in products:
            dispatcher.utter_message(s.join(p))

        return []
