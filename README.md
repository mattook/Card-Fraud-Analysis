# Description

This is an exploratory project for detecting signs of fraud in a mock UK card portfolio, using SQL. Work through the questions and record your answers - I've left mine in this file!

All mock data was produced and refined with AI.

# Requirements

SQL environment (I used **psql** locally)

# Setup

To set up your environment,

* Run generate_dataset.py in the terminal to produce the dataset in data/

* Load into PostgreSQL via sql/schema.sql

# Solutions

Here are my solutions for this project.

## Question 1

### SQL

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

### Comments

Electronics, Luxury Retail, and Gambling have high rates of fraud, with gambling having the highest (1 in 10 transactions). This is because there are many avenues for fraud in gambling: fast cash outs with a stolen card, account hacking and fund takeover, and the actual card holder could even falsely claim their bank card was stolen after losing a lot of money.

## Question 2

### SQL 

```sql
SELECT 
    EXTRACT(HOUR FROM timestamp) AS hour_24, 
    SUM(is_fraud) AS fraud_count
FROM uk_cards_transactions 
GROUP BY hour_24 
ORDER BY hour_24 ASC;
```

### Comments

The first spike at 3AM is the largest spike. This is because most people will be asleep and so be likely to miss criminal activity happening on their account. There is more fraud activity from 6AM to 8AM - which coincides with the morning rush, where everyone is spending money on food and travel. Criminals may prefer to act at these hours, in the hopes that their transactions get lost in the morning slurry of activity.