CREATE INDEX index_products_name on store.products (name); 
CREATE INDEX index_products_price on store.products (price);

CREATE INDEX index_customers_email on store.customers (email);
CREATE INDEX index_customers_phone_number on store.customers (phone_number);

CREATE INDEX index_addresses_customer_id on store.addresses (customer_id);

CREATE INDEX index_order_summary_customer_id on store.order_summary (customer_id);
CREATE INDEX index_order_summary_order_date on store.order_summary (order_date);




