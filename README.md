# Description

This is an exploratory project for detecting signs of fraud in a mock UK card portfolio, using SQL. Work through the questions and record your answers - I've left mine there if you get stuck!

All mock data was produced and refined with AI.

# Requirements

SQL environment (I used **psql** locally)

# Setup

To set up your environment,

* Run generate_dataset.py in the terminal to produce the dataset in data/

* Load into PostgreSQL via sql/schema.sql

# Solutions

Here are my solutions for this project

## Question 1

```sql
SELECT 
    category,
    SUM(is_fraud) AS fraud_count,
    AVG(is_fraud) AS fraud_rate
FROM 
    uk_cards_transactions
GROUP BY 
    category;
```

Electronics, Luxury Retail, and Gambling have high rates of fraud, with gambling having the highest (1 in 10 transactions). This is because there are many avenues for fraud in gambling: fast cash outs with a stolen card, account hacking and fund takeover, and the actual card holder could even falsely claim their bank card was stolen after losing a lot of money.

