
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

st.title("Analyse der RT-Facebook-Post-Metriken")
st.write("Dieses Dashboard zeigt durchschnittliche Reaktionen, Shares und Kommentare der Facebook-Posts.")

# Datensatz laden (wie im Notebook)
dataset_url = "https://github.com/polcomm-passau/computational_methods_python/raw/refs/heads/main/RT_D_Small.xlsx"
df = pd.read_excel(dataset_url)

# Spalten für Reaktionen, Shares und Kommentare auswählen
reaction_columns = ['haha', 'like', 'wow', 'angry', 'sad', 'love', 'hug']
engagement_columns = ['shares', 'comments_num']

all_columns = reaction_columns + engagement_columns

# Durchschnittliche Werte berechnen
mean_values = df[all_columns].mean()

# Balkendiagramm erstellen
st.subheader("Anzahl von Reaktionen, Shares und Kommentare pro Post")
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=mean_values.index, y=mean_values.values, hue=mean_values.index, palette='viridis', legend=False, ax=ax)
ax.set_title('Durchschnittliche Anzahl von Reaktionen, Shares und Kommentare')
ax.set_xlabel('Metrik')
ax.set_ylabel('Durchschnittlicher Wert')
ax.tick_params(axis='x', rotation=45)
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
st.pyplot(fig)

st.subheader("Rohdaten (Auszug)")
st.dataframe(df.head())
