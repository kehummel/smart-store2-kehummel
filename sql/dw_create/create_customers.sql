DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    name TEXT,
    region TEXT,
    join_date TEXT, -- use ISO format: 'YYYY-MM-DD'
    number_of_purchases INTEGER, 
    contact_preferences TEXT
);