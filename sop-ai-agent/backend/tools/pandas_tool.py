import pandas as pd

def execute_pandas_query(code: str, df: pd.DataFrame) -> str:
    # Remove markdown codeblocks if they exist
    code = code.replace('```python', '').replace('```', '').strip()
    
    local_env = {"df": df, "pd": pd}
    try:
        exec(code, {}, local_env)
        result = local_env.get("result", "No result variable assigned.")
        return str(result)
    except Exception as e:
        return f"Error executing query: {str(e)}"
