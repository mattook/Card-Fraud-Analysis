CREATE TABLE uk_cards_transactions (
    transaction_id VARCHAR(50) PRIMARY KEY,
    card_number VARCHAR(20),
    timestamp TIMESTAMP,
    amount NUMERIC(10, 2),
    category VARCHAR(50),
    merchant VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(5),
    is_fraud INT
);