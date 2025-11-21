
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

st.title("Eine Analyse von Artikeln von RT")

# Datensatz laden
dataset_url = "https://github.com/polcomm-passau/computational_methods_python/raw/refs/heads/main/RT_D_Small.xlsx"
df = pd.read_excel(dataset_url)

# 'date' Spalte in Datumsformat umwandeln
df['date'] = pd.to_datetime(df['date'])

# Spalten für Reaktionen, Shares und Kommentare definieren
reaction_columns = ['haha', 'like', 'wow', 'angry', 'sad', 'love', 'hug']
engagement_columns = ['shares', 'comments_num']
all_metrics_columns = reaction_columns + engagement_columns

# Eingabefeld für den Suchbegriff
search_term = st.text_input("Bitte gib deinen Suchbegriff ein:", "grün")

# Filterbedingung für den Suchbegriff
search_condition = pd.Series([False] * len(df)) # Standardmäßig False
if search_term:
    search_condition = df['text'].fillna('').str.contains(search_term, case=False, na=False) | \
                       df['fulltext'].fillna('').str.contains(search_term, case=False, na=False)

# Filterung der DataFrames
filtered_df_with_term = df[search_condition]
filtered_df_without_term = df[~search_condition]

# --- Liniendiagramm (Prozentualer Anteil) ---
if search_term:
    total_posts_per_day = df['date'].value_counts().sort_index()

    if not filtered_df_with_term.empty:
        filtered_posts_per_day = filtered_df_with_term['date'].value_counts().sort_index()

        percentage_per_day = (filtered_posts_per_day / total_posts_per_day) * 100
        percentage_per_day = percentage_per_day.fillna(0) # Fülle NaN, falls an einem Tag keine Posts sind

        st.subheader(f"Prozentualer Anteil der Artikel mit '{search_term}' im Zeitverlauf")

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(percentage_per_day.index, percentage_per_day.values, marker='o', linestyle='-', color='skyblue')
        ax.set_title(f'Prozentualer Anteil der Posts pro Tag mit "{search_term}"')
        ax.set_xlabel('Datum')
        ax.set_ylabel('Prozentualer Anteil (%)')
        ax.grid(True)
        ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

    else:
        st.warning(f"Keine Artikel gefunden, die '{search_term}' im Text oder Fulltext enthalten.")
else:
    st.info("Bitte gib einen Suchbegriff ein, um die Analyse anzuzeigen.")

# --- Vergleich der durchschnittlichen Metriken ---
st.subheader("Vergleich der durchschnittlichen Metriken")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"### Artikel mit '{search_term}'")
    if not filtered_df_with_term.empty:
        st.metric(label="Gesamtzahl der Treffer", value=len(filtered_df_with_term))
        mean_metrics_with_term = filtered_df_with_term[all_metrics_columns].mean().round(2)
        st.dataframe(mean_metrics_with_term)
    else:
        st.info("Keine passenden Artikel gefunden.")

with col2:
    st.markdown(f"### Artikel ohne '{search_term}'")
    if not filtered_df_without_term.empty:
        st.metric(label="Gesamtzahl der Treffer", value=len(filtered_df_without_term))
        mean_metrics_without_term = filtered_df_without_term[all_metrics_columns].mean().round(2)
        st.dataframe(mean_metrics_without_term)
    else:
        st.info("Alle Artikel enthalten den Suchbegriff oder es wurde kein Suchbegriff eingegeben.")

with col3:
    st.markdown("### Unterschied (mit - ohne Suchbegriff)")
    if search_term and not filtered_df_with_term.empty and not filtered_df_without_term.empty:
        differences = mean_metrics_with_term - mean_metrics_without_term

        # Farben basierend auf dem Vorzeichen der Differenz zuweisen
        colors = ['red' if x > 0 else 'green' for x in differences.values]

        fig_diff, ax_diff = plt.subplots(figsize=(10, 6))
        sns.barplot(x=differences.values, y=differences.index, ax=ax_diff, palette=colors)
        ax_diff.set_title('Unterschiede der durchschnittlichen Metriken')
        ax_diff.set_xlabel('Differenz')
        ax_diff.set_ylabel('Metrik')
        ax_diff.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig_diff)
    else:
        st.info("Geben Sie einen Suchbegriff ein, um die Unterschiede anzuzeigen.")

st.subheader("Originale Daten (Auszug)")
st.dataframe(df.head())
