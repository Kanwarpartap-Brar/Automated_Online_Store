#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""



"""

import psycopg
import random
import time

#Establish a connection to the database

with psycopg.connect("dbname=postgres user=postgres password=Applebuy1") as conn:
    
    #create a cursor object to get all product names from products table
    
    def product_names(conn):
        with conn.cursor() as cur:
            cur.execute('SELECT name FROM store.products') #SQL Query to get product names
            rows = cur.fetchall() #fetch all records
            product_name_results = [row[0] for row in rows] #put into list instead of having tuple
            return rows

#generate random names

bot_names = ['Paul George', 'Chris Bumstead', 'Ja Morant', 'Bo Nickel', 'Jose Aldo'] 

#function to generate bot to fill customer table (name, email, phone number)

def bot_customer():
    name = random.choice(bot_names) #pick random name from list of generated names
    email = f"{name.lower().replace(' ', '')}{random.randint(1, 100)}@gmail.com"  #generate email using customer name 
    phone_number = f"+1{random.randint(1000000000,9999999999)}" #random phone number
    return name, email, phone_number


#function to create orders with random products (1-3) and quantities up to 1000

def random_order(conn): #using conn allows for products to be used from the products table instead of creating them again
    product_types = product_names(conn) #fetch product names for order
    num_products = random.randint(1,3) #select 1-3 products per order
    products = random.sample(product_types,num_products) #select random product names (does not repeat b/c it is unique)
    order = [(product, random.randint(1, 1000)) for product in products] #gets what products and how much quanitity (1-1000 units)
    return order

#Using the functions created, make a bot

def bot_order(conn):
    with conn.cursor() as cur: #create a cursor to generate random bot customers 
        name, email, phone_number = bot_customer() #bot customer created
        order_details = random_order(conn) #bot random order created
        
        #insert bot customer into database table
        cur.execute("""INSERT INTO store.customers (name, email, phone_number) VALUES (%s, %s, %s) RETURNING customer_id""",(name, email, phone_number))
        #insert bot details into fields of customer table
        #%s acts as the id holer 
        customer_id = cur.fetchone()[0] #return customer_id which is primary key
        
        #Now doing same thing but generating for the address table
        
        street_address = f"{random.randint(1, 500)} Hofstra Ave" #generate random address
        city = random.choice(['Hempstead','West Hempstead','Garden City','Mineola','Lynbrook','Baldwin','New Hyde Park']) #choose random city from this list
        state = random.choice(['NY','CA','TX','PA','FL','GA','MD']) #choose random state
        zip_code = f"{random.randint(10000, 99999)}" #generate random zip code 
        country = random.choice(['USA', 'Spain', 'England']) #random country
        #insert into table using SQL query
        cur.execute("""INSERT INTO store.addresses (customer_id, street_address, city, state, zip_code, country) VALUES (%s, %s, %s, %s, %s, %s) RETURNING address_id""",
            (customer_id, street_address, city, state, zip_code, country))
        
        address_id = cur.fetchone()[0] #return address_id which is primary key 
        
        #fill in order_summary table
        
      
        cur.execute(
            """INSERT INTO store.order_summary (customer_id, order_date, delivery_status, payment_status, order_total, address_id) 
            VALUES (%s, CURRENT_TIMESTAMP, %s, %s, %s, %s) RETURNING order_id""",
            (
                customer_id,  #link to the customer
                "Processing",  #initial delivery status
                "Pending",  #initial payment status
                0.0,  #price
                address_id,  #link to the address
                ),
            )
        order_id = cur.fetchone()[0]  

        #set up order_details table
        
        product_ids = [] #list for differnt product ids in order
        quantities = [] #list for quantities
        total_price = 0 #initial price in order_details
        for product, quantity in order_details:
            cur.execute("""SELECT product_id, price FROM store.products WHERE name = %s""", product,), #fetch all product details
            product = cur.fetchone() #product details
            
            #if product exists add product_id, update quanity, and update total price based on quantity
            
            if product:
                product_id, price = product
                product_ids.append(product_id)
                quantities.append(quantity)
                total_price += price * quantity
                
        #insert everything into order_details
        
        cur.execute("""INSERT INTO store.order_details (order_id, product_id, quantity, total_price) VALUES (%s, %s, %s, %s)""",
            (order_id, product_id, quantity, total_price))

        
        #update total price in order_summary
        cur.execute(
            """UPDATE store.order_summary SET order_total = %s WHERE order_id = %s""",
            (total_price, order_id),)
        
        conn.commit()  # Commit all changes to the database
        print(f"Order {order_id} created for customer {name} with address ID {address_id}.")  # Print confirmation
        
       
    
        
 #run with this        
# creates a purchase bot and places an order every 10 seconds        
 
    
if __name__ == "__main__":
    with psycopg.connect("dbname=postgres user=postgres password=Applebuy1") as conn:
        while True:  #infinite loop to create purhcase bots every 10 seconds
            bot_order(conn)  
            time.sleep(10)  #10 second sleep (acts as a delay)
        
        
        
        
        
        
    

        







































































