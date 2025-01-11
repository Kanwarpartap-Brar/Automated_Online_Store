CREATE TABLE IF NOT EXISTS store.products
(
    product_id integer NOT NULL DEFAULT nextval('store.products_product_id_seq'::regclass),
    name text COLLATE pg_catalog."default" NOT NULL,
    price numeric NOT NULL,
    description text COLLATE pg_catalog."default" NOT NULL,
    delivery_return_details text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT products_pkey PRIMARY KEY (product_id)
)

CREATE TABLE IF NOT EXISTS store.order_summary
(
    order_id integer NOT NULL DEFAULT nextval('store.order_summary_order_id_seq'::regclass),
    customer_id integer NOT NULL,
    order_date timestamp with time zone NOT NULL,
    delivery_status text COLLATE pg_catalog."default" NOT NULL,
    payment_status text COLLATE pg_catalog."default" NOT NULL,
    order_total numeric NOT NULL,
    address_id integer,
    CONSTRAINT order_summary_pkey PRIMARY KEY (order_id)
)

CREATE TABLE IF NOT EXISTS store.order_details
(
    order_detail_id integer NOT NULL DEFAULT nextval('store.order_details_order_detail_id_seq'::regclass),
    order_id integer NOT NULL,
    total_price numeric NOT NULL,
    quantity integer,
    product_id integer[],
    CONSTRAINT order_details_pkey PRIMARY KEY (order_detail_id)
)

CREATE TABLE IF NOT EXISTS store.customers
(
    customer_id integer NOT NULL DEFAULT nextval('store.customers_customer_id_seq'::regclass),
    name text COLLATE pg_catalog."default" NOT NULL,
    email text COLLATE pg_catalog."default" NOT NULL,
    phone_number text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT customers_pkey PRIMARY KEY (customer_id)
)

CREATE TABLE IF NOT EXISTS store.addresses
(
    address_id integer NOT NULL DEFAULT nextval('store.addresses_address_id_seq'::regclass),
    customer_id integer NOT NULL,
    street_address text COLLATE pg_catalog."default" NOT NULL,
    city text COLLATE pg_catalog."default" NOT NULL,
    state text COLLATE pg_catalog."default" NOT NULL,
    zip_code text COLLATE pg_catalog."default" NOT NULL,
    country text COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT addresses_pkey PRIMARY KEY (address_id)
)







