import csv
import random
from datetime import datetime, timedelta

# Configuration
NUM_ROWS = 5000
START_DATE = datetime(2026, 6, 1)

# Base Lists for Generating Data
MERCHANTS = {
    'Groceries': ['Tesco', 'Sainsburys', 'Asda', 'Waitrose'],
    'Transport': ['TfL Tube', 'Uber London', 'Shell Petrol', 'Trainline'],
    'Entertainment': ['Netflix', 'Spotify', 'Cineworld', 'Pub Oxford St'],
    'Electronics': ['Apple Store', 'Currys PC World', 'Amazon UK'],
    'Gambling': ['Bet365', '888Casino', 'Ladbrokes'],
    'Luxury Retail': ['Harrods', 'Selfridges', 'Rolex London']
}

CITIES = ['London', 'Manchester', 'Birmingham',
          'Leeds', 'Edinburgh', 'Bristol']
COUNTRIES = ['GB'] * 95 + ['US', 'FR', 'DE', 'AE']  # 95% UK, 5% International

# Generate a pool of 200 Unique Card Numbers
CARD_POOL = [f"453271******{random.randint(1000, 9999)}" for _ in range(200)]

# Initialize file structure
headers = ['transaction_id', 'card_number', 'timestamp', 'amount',
           'category', 'merchant', 'city', 'country', 'is_fraud']

with open('data/uk_cards_transactions.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

    current_time = START_DATE

    # 1. GENERATE BASE GENUINE DATA
    rows = []
    for i in range(1, NUM_ROWS + 1):
        # Progress time realistically across rows
        current_time += timedelta(minutes=random.randint(1, 15))

        card = random.choice(CARD_POOL)
        category = random.choice(list(MERCHANTS.keys()))
        merchant = random.choice(MERCHANTS[category])
        country = random.choice(COUNTRIES)
        city = 'London' if country == 'GB' and random.random() > 0.4 else (
            random.choice(CITIES) if country == 'GB' else 'International')

        # Genuine amounts based on category
        if category in ['Groceries', 'Transport', 'Entertainment']:
            amount = round(random.uniform(5.00, 60.00), 2)
        elif category == 'Electronics':
            amount = round(random.uniform(100.00, 1200.00), 2)
        else:  # Default ranges
            amount = round(random.uniform(10.00, 150.00), 2)

        rows.append([f"TXN_{100000 + i}", card, current_time.strftime(
            '%Y-%m-%d %H:%M:%S'), amount, category, merchant, city, country, 0])

    # 2. SPRINKLE SPECIFIC FRAUD SCENARIOS (Modifying roughly 3-4% of data for realism)

    # Scenario A: Velocity Attacks (Rapid successive transactions on the same card)
    for _ in range(25):
        idx = random.randint(100, NUM_ROWS - 10)
        target_card = CARD_POOL[random.randint(0, 20)]  # Pick a specific card
        base_time = datetime.strptime(rows[idx][2], '%Y-%m-%d %H:%M:%S')

        # Inject 4 rapid gambling/electronics purchases within minutes
        for v in range(4):
            fraud_time = base_time + \
                timedelta(seconds=random.randint(10, 45) * (v + 1))
            rows[idx + v] = [
                f"TXN_V_{idx}_{v}",
                target_card,
                fraud_time.strftime('%Y-%m-%d %H:%M:%S'),
                round(random.uniform(200.00, 500.00), 2),
                'Gambling',
                random.choice(MERCHANTS['Gambling']),
                'London',
                'GB',
                1  # Flagged as Fraud
            ]

    # Scenario B: Geo-Velocity Anomalies (Impossible Physical Travel)
    for _ in range(25):
        idx = random.randint(100, NUM_ROWS - 5)
        # Force consecutive rows to have the same card but impossibly different geographies
        target_card = rows[idx][1]
        base_time = datetime.strptime(rows[idx][2], '%Y-%m-%d %H:%M:%S')

        # Row 1: Valid London transaction
        rows[idx] = [rows[idx][0], target_card, base_time.strftime(
            '%Y-%m-%d %H:%M:%S'), rows[idx][3], rows[idx][4], rows[idx][5], 'London', 'GB', 0]

        # Row 2: Same card, 15 minutes later, but in New York (Impossible Travel)
        fraud_time = base_time + timedelta(minutes=15)
        rows[idx + 1] = [
            f"TXN_G_{idx}",
            target_card,
            fraud_time.strftime('%Y-%m-%d %H:%M:%S'),
            round(random.uniform(400.00, 1500.00), 2),
            'Electronics',
            'Apple Store NY',
            'New York',
            'US',
            1  # Flagged as Fraud
        ]

    # Scenario C: Late-Night Luxury Spikes (High value anomalies when sleep patterns occur)
    for _ in range(30):
        idx = random.randint(100, NUM_ROWS - 1)
        base_time = datetime.strptime(rows[idx][2], '%Y-%m-%d %H:%M:%S')
        # Shift transaction to 3:30 AM
        fraud_time = base_time.replace(hour=3, minute=random.randint(10, 50))

        rows[idx] = [
            f"TXN_L_{idx}",
            rows[idx][1],
            fraud_time.strftime('%Y-%m-%d %H:%M:%S'),
            # Unusually high amount
            round(random.uniform(1500.00, 4500.00), 2),
            'Luxury Retail',
            random.choice(MERCHANTS['Luxury Retail']),
            'London',
            'GB',
            1  # Flagged as Fraud
        ]

    # Sort everything back by timestamp to keep chronological sense
    rows.sort(key=lambda x: x[2])
    writer.writerows(rows)

print("✅ Successfully generated uk_cards_transactions.csv with 5000 rows.")
