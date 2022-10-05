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
from regex import S
from sqlalchemy import null
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

            try:
                product = str(tracker.latest_message['entities'][0]['value']) ## get Entitiess
            except:
                product = "null"

            print(product)  

            ## Nếu sản phẩm không tồn tại trong csdl
            if product == "null":
                dispatcher.utter_message("Sản phẩm này bên shop không kinh doanh bạn nhé, bạn có thể tham khảo thêm các sản phẩm ở trang chủ")
            else:
                ## MySQL query connect
                mycursor = connect.cursor()    
                sqlQuery = "SELECT name, sellPrice FROM products WHERE name LIKE '{}'".format(product) 
                mycursor.execute(sqlQuery)
                results = mycursor.fetchall()        

                for i in results:            
                    if i[0].lower() == product.lower():
                        price = results[0][1] ## Lấy giá tiền
                        format_price = "{:,.0f}đ".format(price) ## Xử lý giá tiền
                    else:
                        dispatcher.utter_message("Sản phẩm này bên shop không kinh doanh bạn nhé, bạn có thể tham khảo thêm các sản phẩm ở trang chủ")
                        
                    dispatcher.utter_message(response="utter_rep_price", price=format_price)
            return []

class action_size(Action):
    def name(self) -> Text:
        return "action_size"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            try:
                product = tracker.latest_message['entities'][0]['value'] ## get Entities
            except:
                product = "null"
            
            if product == "null":
                dispatcher.utter_message("Bạn cần xem kích thước của sản phẩm nào vậy ạ ?")
            else:

                ## MySQL query connect
                mycursor = connect.cursor()    
                sqlQuery = "SELECT name, size FROM products WHERE name LIKE '{}'".format(product) 
                mycursor.execute(sqlQuery)
                results = mycursor.fetchall()

                size = results[0][1] ## Lấy kích thước
                for i in results: 
                    if i[0].lower() == product.lower():
                        dispatcher.utter_message(response="utter_rep_size", size = size) 
                    else:
                        dispatcher.utter_message("Bạn cần xem kích thước của sản phẩm nào vậy ạ ?")
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
