import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

def execute_plotly_code(code: str, df: pd.DataFrame) -> dict | None:
    # Remove markdown codeblocks if they exist
    code = code.replace('```python', '').replace('```', '').strip()
    
    local_env = {"df": df, "pd": pd, "px": px, "go": go}
    try:
        exec(code, {}, local_env)
        fig = local_env.get("fig")
        if fig is not None:
            # Parse json back into dict to prevent serialization issues
            return json.loads(fig.to_json())
        return None
    except Exception as e:
        print(f"Error executing plotly code: {e}")
        return None
