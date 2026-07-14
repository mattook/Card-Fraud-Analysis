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

## Question 3

### SQL

```sql
-- I'm not very confident with window functions so I used AI here
WITH sequential_transactions AS (
    SELECT 
        card_number,
        transaction_id,
        timestamp AS current_txn_time,
        city AS current_city,
        country AS current_country,
        amount,
        is_fraud,
        -- Get previous transaction details on the exact same card
        LAG(timestamp) OVER(PARTITION BY card_number ORDER BY timestamp) AS prev_txn_time,
        LAG(city) OVER(PARTITION BY card_number ORDER BY timestamp) AS prev_city,
        LAG(country) OVER(PARTITION BY card_number ORDER BY timestamp) AS prev_country
    FROM 
        uk_cards_transactions
)
SELECT 
    card_number,
    prev_txn_time,
    current_txn_time,
    EXTRACT(EPOCH FROM (current_txn_time - prev_txn_time)) AS time_diff_seconds,
    (current_txn_time - prev_txn_time) AS time_diff_interval,
    prev_city,
    current_city,
    prev_country,
    current_country,
    amount,
    is_fraud
FROM 
    sequential_transactions
WHERE 
    prev_txn_time IS NOT NULL
ORDER BY 
```

### Comments

You get a wide range of transaction time intervals ranging from below zero seconds to several hours. A lot of the very short time intervals were London->London transactions, implying people are spamming the same website with a bot. There are very few of these impossibly fast transactions but nobody is filling out their card details across several forms in less than 5 seconds, and even if somebody has loaded up their card details across many different tabs and pressed purchase at the same time on all of them -- why?

## Question 4

### Comments

This one can be answered with the same SQL from question 3. Once you get to half an hour intervals, you begin to see a lot of UK->International activity, which is still impossible because - assuming they are travelling by plane - just boarding to takeoff takes about half an hour. I found the cluster of London->New York activity at 15 minutes quite interesting because even the concorde took 3.5 hours to make this same trip, so there are 2 clear possibilities for this: a teleporter, or fraud.

## Question 5

### SQL

```sql
SELECT 1-AVG(is_fraud) AS fraud_ratio
FROM uk_cards_transactions
WHERE EXTRACT(HOUR FROM timestamp) = 3;

SELECT 1-AVG(is_fraud) AS fraud_ratio
FROM uk_cards_transactions
WHERE EXTRACT(HOUR FROM timestamp) BETWEEN 6 AND 8;
```

### Comments

You can use AVG() to find the ratio of people committing fraud because is_fraud can only be 0 or 1. 84 percent of transactions at 3AM are not fraud, and the figure is 93 percent between 6 and 8. Althought these are very high, they still contribute to a significant amount of fraud activity, with 16 percent of all recorded transactions being fraud at 3AM. If this were a trend throughout the whole night, I'd support the decision to block late night activity, but because its a doesn't make sense to block this single time because criminals would just move their bot triggers to another hour.