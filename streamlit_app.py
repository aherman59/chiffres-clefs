import requests
import pandas as pd
import plotly.express as px
import streamlit as st

####

# UTILS

####

def ask(url):
    try:
        response = requests.get(url)
        if response.status_code == 200: 
            return response.json()
    except Exception as e:
        return None

def get_departements():
    url = f"https://geo.api.gouv.fr/departements/"
    return ask(url)


def graphe_nb_ventes(code_dep, nom_dep):
    url = f"https://apidf-preprod.cerema.fr/indicateurs/dv3f/departements/annuel/{code_dep}"
    response  = ask(url)
    indicateurs = pd.DataFrame.from_dict(response["results"])
    fig = px.bar(indicateurs, 
                x='annee', 
                y=['nbtrans_cod111', 'nbtrans_cod121'], 
                title = f"Evolution annuelle du nombre de ventes de logements pour {nom_dep}", 
                labels={"annee" : "Année de mutation", 
                        "value" : "Nombre de ventes",},
                )
    noms={"nbtrans_cod111": "Maison individuelle", 
        "nbtrans_cod121": "Appartement individuel"}
    fig.update_layout(legend_title_text="Nombre de ventes")
    fig.for_each_trace(lambda t: t.update(hovertemplate = t.hovertemplate.replace(t.name, noms[t.name]), name=noms[t.name]))
    return fig


######

## APP

######

st.set_page_config(page_title="Chiffre-clefs", page_icon=None, layout="centered",)

st.sidebar.title("Chiffre-clefs")

bdd = st.sidebar.selectbox("Base de données", ["Fichiers fonciers", "DV3F", "Lovac"])

departements = get_departements()
departement = st.sidebar.selectbox("Choix du département", [d["nom"] for d in departements])
coddep = [d["code"] for d in departements if d["nom"] == departement][0]


st.subheader("Nombre de ventes de logements")
with st.spinner("Chargement..."):
    fig = graphe_nb_ventes(coddep, departement)
    st.plotly_chart(fig, use_container_width=True)

df = pd.read_csv("test.csv")
st.dataframe(df)