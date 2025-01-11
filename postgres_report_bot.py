#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""



import psycopg
import time

#connect to the postgres database
with psycopg.connect("dbname=postgres user=postgres password=Applebuy1") as conn:

#function to make a sales report

    def sales_report(conn):
    
        with conn.cursor() as cur: #cursosr object to interact with the database and perform executions
        #add total units sold for each product name as well as total revenue for each product name
        #then join products and order_details on product_id to group by proddcut name and order by revenue, units sold, and name
            cur.execute("""SELECT products.name AS product_name,
                    SUM(order_details.quantity) AS units_sold,
                    SUM(order_details.total_price) as total_revenue
                    FROM store.products JOIN store.order_details ON products.product_id = order_details.product_id
                    GROUP BY products.name 
                    ORDER BY total_revenue DESC, units_sold DESC, product_name ASC
                    """)

            results = cur.fetchall() #fetch all results
                    
            print('Sales Report: ')
            #print('\n')
            for product_name, units_sold, total_revenue in results:
                print(f"{product_name} sold {units_sold} units, total revenue ${total_revenue:,.2f}")
            print('\n')
        
                    

if __name__ == "__main__":
    #run while loop to generate sales report every one second by putting the function to sleep every 1 second
    while True:
        with psycopg.connect("dbname=postgres user=postgres password=Applebuy1") as conn: #conection remains open in the while loop
            sales_report(conn)
            time.sleep(1)
        











































