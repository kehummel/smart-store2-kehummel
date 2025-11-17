DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,           -- from TransactionID
    date TEXT,                             -- from SaleDate (ISO 8601 format)
    customer_id TEXT,                      -- from CustomerID
    product_id TEXT,                       -- from ProductID
    store_id TEXT,                         -- from StoreID
    campaign_id TEXT,                      -- from CampaignID
    sales_amount REAL,                     -- from SaleAmount
    number_of_items INTEGER, 
    city TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);