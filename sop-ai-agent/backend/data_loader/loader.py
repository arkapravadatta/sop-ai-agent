import pandas as pd
import os
from utils.logger import get_logger

logger = get_logger("loader")

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
        
        # Read static textual schema priority if it exists
        schema_path = os.path.join(os.path.dirname(__file__), "schema.txt")
        if os.path.exists(schema_path):
            with open(schema_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                valid_lines = [l for l in lines if not l.startswith("#") and l.strip()]
                if valid_lines:
                    _schema_description = "".join(valid_lines).strip()

        # Fallback to dynamic dtypes if schema.txt was effectively empty
        if not _schema_description:
            schema_lines = []
            for col, dtype in df.dtypes.items():
                schema_lines.append(f"{col} ({dtype})")
            _schema_description = ", ".join(schema_lines)
            
        return _sales_df, _schema_description
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        return pd.DataFrame(), ""
