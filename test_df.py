from src.database.crud import get_individual_engagement_scores
import pandas as pd
df = get_individual_engagement_scores()
print(df.isna().sum())
