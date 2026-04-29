# engine.py - Risk Calculation Engine
import pandas as pd

def calculate_risk_score(df):
    df = df.copy()
    df['Risk_Score'] = (
        df['Geopolitical_Risk'] * 35 +
        df['Climate_Anomaly'] * 25 +
        df['Transport_Risk'] * 25 +
        df['Demand_Fluctuation'] / 100 * 15
    ).round(1)
    
    df['Risk_Level'] = pd.cut(df['Risk_Score'], 
                             bins=[0, 40, 65, 100], 
                             labels=['Low ', 'Medium', 'High'])
    return df
