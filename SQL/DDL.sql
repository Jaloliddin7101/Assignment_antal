##CUSTOMERS TABLE

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    email_address VARCHAR(255) UNIQUE NOT NULL,
    country VARCHAR(100) NOT NULL
);

##PRODUCTS TABLE

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    category VARCHAR(100) NOT NULL
);

##SALES TRANSACTIONS

CREATE TABLE sales_transactions (
    transaction_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    product_id INT REFERENCES products(product_id),
    purchase_date DATE NOT NULL,
    quantity_purchased INT NOT NULL
);

##SHIPPING DETAILS

CREATE TABLE shipping_details (
    shipping_id SERIAL PRIMARY KEY,
    transaction_id INT REFERENCES sales_transactions(transaction_id),
    shipping_date DATE NOT NULL,
    shipping_address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL
);
