import pandas as pd
import os

_sales_df = None
_schema_description = ""

def load_sales_data(data_dir: str) -> tuple[pd.DataFrame, str]:
    global _sales_df, _schema_description
    if _sales_df is not None:
        return _sales_df, _schema_description

    try:
        dim_product = pd.read_csv(os.path.join(data_dir, "dim_product.csv"))
        dim_customer = pd.read_csv(os.path.join(data_dir, "dim_customer.csv"))
        fact_billing = pd.read_csv(os.path.join(data_dir, "fact_billing.csv"))

        # Merge them
        df = pd.merge(fact_billing, dim_product, on="product_id", how="left")
        df = pd.merge(df, dim_customer, on="customer_id", how="left")
        
        _sales_df = df
        
        # Build schema description
        schema_lines = []
        for col, dtype in df.dtypes.items():
            schema_lines.append(f"{col} ({dtype})")
        _schema_description = ", ".join(schema_lines)
        
        return _sales_df, _schema_description
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame(), ""
