import pandas as pd
import numpy as np
import os

def generate_data():
    os.makedirs("data", exist_ok=True)
    
    # dim_product (20 products)
    products = []
    for i in range(1, 21):
        products.append({
            "product_id": f"P{i:03d}",
            "product_name": f"Machine Part {i}",
            "category": np.random.choice(["Engine", "Hydraulics", "Electronics", "Chassis"]),
            "sub_category": f"Sub-{i%5}"
        })
    df_prod = pd.DataFrame(products)
    df_prod.to_csv("data/dim_product.csv", index=False)
    
    # dim_customer (15 customers across 4 regions)
    customers = []
    for i in range(1, 16):
        customers.append({
            "customer_id": f"C{i:03d}",
            "customer_name": f"Manufacturing Co {i}",
            "region": np.random.choice(["North", "South", "East", "West"]),
            "segment": np.random.choice(["Enterprise", "Mid-Market", "SMB"])
        })
    df_cust = pd.DataFrame(customers)
    df_cust.to_csv("data/dim_customer.csv", index=False)
    
    # fact_billing (~200 rows spanning 2024-01 to 2025-03)
    dates = pd.date_range("2024-01-01", "2025-03-31", periods=200)
    bills = []
    for i in range(1, 201):
        qty = np.random.randint(1, 100)
        u_price = np.random.randint(500, 5000)
        bills.append({
            "bill_id": f"B{i:05d}",
            "bill_date": dates[i-1].strftime("%Y-%m-%d"),
            "customer_id": np.random.choice(df_cust["customer_id"]),
            "product_id": np.random.choice(df_prod["product_id"]),
            "quantity": qty,
            "unit_price": u_price,
            "total_amount": qty * u_price
        })
    df_bill = pd.DataFrame(bills)
    df_bill.to_csv("data/fact_billing.csv", index=False)
    print("Synthetic data generated in data/")

if __name__ == "__main__":
    generate_data()
