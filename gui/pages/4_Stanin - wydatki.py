import streamlit as st

import plotly.graph_objects as go
import pandas as pd
import json

from io import StringIO
import plotly.express as px



df_stanin = pd.read_csv('../data/staniny2022.csv')

df_kpi = pd.read_csv('../data/SIO_30_09_2022_schools_with_kpi.csv')

# df_kpi['school_subsidize']
# df_kpi['school_subsidize_per_student']

df_polaczone = pd.merge(df_stanin, df_kpi, on='Regon')
# st.dataframe(df_stanin)


# st.dataframe(df_kpi)
st.dataframe(df_polaczone)

df_polaczone.to_csv('kpi_stanin.csv', index=False)

