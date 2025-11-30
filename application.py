import streamlit as st
import joblib
import pandas as pd

class CaseUniformizer:
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X.apply(lambda col: col.str.lower() if col.dtype == 'object' else col)

try:
    model = joblib.load('Model.pkl')
except FileNotFoundError:
    st.error("...")

import streamlit as st
import joblib
import pandas as pd
import numpy as np

try:
    model = joblib.load('Model.pkl')
except FileNotFoundError:
    st.error("Erreur: le fichier 'Model.pkl' n'a pas été trouvé. Assurez-vous qu'il a été sauvegardé correctement")
    st.stop()

st.title(" 🩺 prédiction du risque de maladie cardiaque (CHD)")
st.write(" veuillez entrer les caractéristiques cliniques pour obtenir la prédiction du risque")

with st.form(" prediction_form"):
    st.header(" caractéristiques cliniques")

    sbp = st.slider("Pression Sanguine Systolique (sbp)", min_value=90, max_value=200, value=130)
    ldl = st.number_input("Taux de LDL (ldl)", min_value=0.0, max_value=800.0, value=300.0)
    adiposity = st.number_input("Adiposité", min_value=0.0, max_value=50.0, value=25.0)
    famhist = st.selectbox("Antécédents familiaux (famhist)", options=['present', 'absent'])
    obesity = st.number_input("Obésité (Mesure)", min_value=0.0, max_value=50.0, value=25.0)
    age = st.slider("Âge", min_value=18, max_value=80, value=45)

    submitted = st.form_submit_button("Prédire le Risque")

if submitted:
    new_data = pd.DataFrame({
        'sbp': [sbp],
        'ldl': [ldl],
        'adiposity': [adiposity],
        'famhist': [famhist],
        'obesity': [obesity],
        'age': [age]
    })
    
    prediction = model.predict(new_data)[0]
    
    try:
        probability = model.predict_proba(new_data)[0]
    except AttributeError:
        probability = None

    st.subheader("Résultats de la Prédiction")

    if prediction == 1:
        st.error("Risque de Maladie Cardiaque (CHD) : PRÉSENT")
        if probability is not None:
            st.write(f" probabilité d'avoir la maladie : {probability[1]*100:.2f}%")
    else:
        st.success(" risque de maladie cardiaque (CHD) : ABSENT")
        if probability is not None:
            st.write(f" probabilité d'être en bonne santé : {probability[0]*100:.2f}%")
    st.info("Pour déployer l'application, enregistrez ce code dans 'app.py' et lancez 'streamlit run app.py' localement, puis utilisez un service de cloud comme Streamlit Cloud.")