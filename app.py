import requests
import pandas as pd
import json
import streamlit as st

# Metadaten über BGDI abfragen
url = "https://api3.geo.admin.ch/rest/services/api/MapServer?searchText=ch.bafu"
response = requests.get(url).json()

# Downloadlink und Layer ID holen
Layers = []
for layer in response['layers']:
  try:
    layerBodId = layer['layerBodId']
    downloadUrl = layer['attributes']['downloadUrl']
    Layers.append({'layerBodId': layerBodId, 'downloadUrl': downloadUrl})
  except:
    Layers.append({'layerBodId': layerBodId, 'downloadUrl': ''})

# Layer Details als Dataframe speichern und filtern
dfLayers = pd.DataFrame(Layers)
dfLayers_filtered = dfLayers[~dfLayers['downloadUrl'].str.contains("https://data.geo.admin.ch/browser")]

# Anteil der noch nicht migrierten Layer berechnen
AnteilMigriert = len(dfLayers_filtered) / len(dfLayers) * 100
AnteilMigriert = round(AnteilMigriert)
AnteilMigriert = f"{AnteilMigriert}% der BAFU Layer sind auf STAC."

# App
# Streamlit app
st.title("BAFU Geodaten welche noch nicht in die STAC API migriert wurden")
st.markdown("Das BAFU migriert alle Geodaten in der BGDI in die STAC API. Diese Applikation zeigt auf, welche Layer noch migriert werden müssen.")
st.subheader("Anteil bereits migrierter Layer")
st.badge(AnteilMigriert, color="green", width=20)

st.subheader("Layer welche noch nicht migriert sind")
st.dataframe(dfLayers_filtered)  
