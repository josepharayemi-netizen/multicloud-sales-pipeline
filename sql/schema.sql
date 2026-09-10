CREATE TABLE sales (
    transaction_id VARCHAR(50) PRIMARY KEY,
    order_date DATE NOT NULL,
    region VARCHAR(100) NOT NULL,
    product VARCHAR(150) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(14,2) NOT NULL,
    unit_cost DECIMAL(14,2) NOT NULL,
    revenue DECIMAL(14,2) NOT NULL,
    profit DECIMAL(14,2) NOT NULL
);
