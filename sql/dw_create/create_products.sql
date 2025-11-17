DROP TABLE IF EXISTS products;

CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    unit_price REAL,
    stock_quantity INTEGER,
    purchase_type TEXT
);