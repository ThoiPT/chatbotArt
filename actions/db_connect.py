import mysql.connector

from actions.settinghost import connect

db_name = "decor_data"
table_category = "product_categories"
table_product = "products"



## Lấy toàn bộ dữ liệu sản phẩm
def DataProduct(name_products):
    mycursor = connect.cursor()
    sql = f'SELECT name from {db_name}.{table_product};'

    try:
        mycursor.execute(sql)
        results = mycursor.fetchall()
        name = results
        return name

    except:
        return "Không có danh mục bạn cần tìm"


#
# def DataProduct12(name_products):
#     mycursor = connect.cursor()
#     sql = f'SELECT name from {db_name}.{table_product};'
#
#     try:
#         mycursor.execute(sql)
#         results = mycursor.fetchall()
#         name = results
#         return name
#
#     except:
#         return "Không có sản phẩm bạn cần tìm"
