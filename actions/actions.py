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
        

class action_ask_product(Action):
    def name(self) -> Text:
        return "action_ask_product"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            try:
                product_slot = tracker.get_slot("product")
                attr = tracker.get_slot("attr")
    
            except:
                product_slot = "null"
                attr = "null"
              
            # attr_qty = tracker.get_slot("attr_qty")
            print("Slot P: "+ product_slot)    
            print("Attr: " + attr)
            # print("Attr_Qty: " + attr_qty)


            mycursor = connect.cursor()    
            sqlQuery = "SELECT name, sellPrice FROM products WHERE name LIKE '{}'".format(product_slot) 
            mycursor.execute(sqlQuery)
            results = mycursor.fetchall()        
            
            ## Nếu để trống sản phẩm
            for p in results:
                if product_slot == "null":
                    dispatcher.utter_message("Bạn cần hỏi sản phẩm nào vậy bạn, bạn gửi tên sản phẩm giúp mình với")
                elif p[0].lower() != product_slot.lower():
                    dispatcher.utter_message("Sản phẩm hiện chưa có trên Shop hoặc gửi sai tên sản phẩm")
                else:
                    ## MySQL query connect
                    mycursor = connect.cursor()    
                    sqlQuery = "SELECT name, sellPrice FROM products WHERE name LIKE '{}'".format(product_slot) 
                    mycursor.execute(sqlQuery)
                    results = mycursor.fetchall()        

                    for i in results:            
                        if i[0].lower() == product_slot.lower():
                            price = results[0][1] ## Lấy giá tiền
                            format_price = "{:,.0f}đ".format(price) ## Xử lý giá tiền
                        else:
                            dispatcher.utter_message("Sản phẩm này bên shop không kinh doanh bạn nhé, bạn có thể tham khảo thêm các sản phẩm ở trang chủ")
                            
                        dispatcher.utter_message(response="utter_rep_price", price=format_price)

            return []

class action_ask_qty(Action):
    def name(self) -> Text:
        return "action_ask_qty"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            try:
                product_slot = tracker.get_slot("product")
                attr_qty = tracker.get_slot("attr_qty")
            except:
                product_slot = "null"
                attr_qty = "null"
            
            if attr_qty == "null":
                dispatcher.utter_message("Bạn cần hỏi gì ạ")
            else:

                ## MySQL query connect
                mycursor = connect.cursor()    
                sqlQuery = "SELECT name, quantity FROM products WHERE name LIKE '{}'".format(product_slot) 
                mycursor.execute(sqlQuery)
                results = mycursor.fetchall()

                # size = results[0][1] ## Lấy kích thước
                for i in results: 
                    if i[0].lower() == product_slot.lower():
                        dispatcher.utter_message(response="utter_rep_qty") 
                    else:
                        dispatcher.utter_message("Bạn có thể nhắc lại giúp mình không ạ")
            return []

# # --------------------------------------------------------------------------
class action_ask_size(Action):

    def name(self) -> Text:
        return "action_ask_size"

    def run(self, dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "Dict[Text, Any]") -> List[Dict[Text, Any]]:
        
        product_slot = tracker.get_slot("product")
        attr_size = tracker.get_slot("attr_size")

        if attr_size:

            mycursor = connect.cursor()    
            sqlQuery = "SELECT name, size FROM products WHERE name LIKE '{}'".format(product_slot) 
            mycursor.execute(sqlQuery)
            results = mycursor.fetchall()

            product = results[0][0]
            size = results[0][1]

            dispatcher.utter_message(response="utter_rep_size", size=size)
        else:
            dispatcher.utter_message("Bạn cần xem kích thước sản phẩm nào vậy")

        return []


class action_ask_weight(Action):

    def name(self) -> Text:
        return "action_ask_weight"

    def run(self, dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "Dict[Text, Any]") -> List[Dict[Text, Any]]:
        
        product_slot = tracker.get_slot("product")
        attr_weight = tracker.get_slot("attr_weight")

        if attr_weight:

            mycursor = connect.cursor()    
            sqlQuery = "SELECT name, weight FROM products WHERE name LIKE '{}'".format(product_slot) 
            mycursor.execute(sqlQuery)
            results = mycursor.fetchall()

            product = results[0][0]
            weight = results[0][1]

            dispatcher.utter_message(response="utter_rep_weight", weight=weight)
        else:
            dispatcher.utter_message("Bạn cần xem trọng lượng sản phẩm nào vậy")

        return []

class action_give_name(Action):
    
    def name(self) -> Text:
        return "action_give_name"
    
    def run(self, dispatcher: "CollectingDispatcher",
            tracker: Tracker,
            domain: "Dict[Text, Any]") -> List[Dict[Text, Any]]:
        
        cust_sex = tracker.get_slot("cust_sex")
        cust_name_boy = tracker.get_slot("cust_name_boy")
        cust_name_girl = tracker.get_slot("cust_name_girl")

        if cust_sex == "Anh" or cust_sex == "anh":
            dispatcher.utter_message("Xin chào {} {}".format(cust_sex, cust_name_boy))
        else:
            dispatcher.utter_message("Xin chào {} {}".format(cust_sex, cust_name_girl))
            
        return[]
