import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Dados", layout="wide")
st.sidebar.markdown("Desenvolvido por [Rafael Cristofali](https://github.com/Rafafaaa)")
st.logo("logo.png")

st.title("Desmatamento da Região Norte do Brasil")

st.write("O desmatamento na Região Norte do Brasil é um dos desafios ambientais mais urgentes, ameaçando a biodiversidade, os povos indígenas e o equilíbrio climático global. Impulsionado por atividades como a expansão agropecuária, a extração ilegal de madeira e a mineração, o desmatamento tem avançado rapidamente, resultando na perda de milhares de hectares de floresta por ano.")

st.write("Além de comprometer os ecossistemas, a degradação da Amazônia intensifica as emissões de gases de efeito estufa, impactando o regime de chuvas e aumentando os riscos de mudanças climáticas. O combate ao desmatamento exige políticas públicas eficazes, fiscalização rigorosa e o incentivo a práticas sustentáveis que conciliem desenvolvimento econômico e preservação ambiental.")

st.write("Os dados utilizado para a análise foram coletados a partir do PRODES, um projeto da INPE (Instituto Nacional de Pesquisas Espaciais) - http://www.obt.inpe.br/OBT/assuntos/programas/amazonia/prodes")

st.write("Os dados apresentam a área desmatada em km² desde 1988 até 2022 nos estados da região norte do Brasil")

st.write("Com esses dados podemos responder as seguintes perguntas:")
st.markdown("- Como o desmatamento total variou ao longo dos anos?")
st.markdown("- Quais foram os anos com maiores e menores índices de desmatamento?")

df = st.session_state["data"]
st.dataframe(df)


