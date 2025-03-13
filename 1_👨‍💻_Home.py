import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.app_logo import add_logo

if "data" not in st.session_state:
    df = pd.read_csv("desmatamento_prodes.csv")
    #df = df.sort_values(by="referencia", ascending=True)
    st.session_state["data"] = df
# if "data" not in st.session_state:
#     df = pd.read_excel("Dados_InstagramCliente_AULA_3ESP.xlsx", index_col="Post ID")
#     df = df.sort_values(by="Reach", ascending=False)
#     st.session_state["data"] = df


st.set_page_config(page_title="Dashboard de Desmatamento da Região Norte do Brasil", layout="wide")
st.logo("logo.png")
st.image("logo.png", width=150)
st.markdown(
    "[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rafael-cristofali)"
    "[![GitHub](https://img.shields.io/badge/GitHub-0D1117?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Rafafaaa)"
)

# Criando as sub-abas (pages)
pages = st.sidebar.selectbox("", [
    "👨‍💻 Home",
    "📄 Formação e Experiência",
    "💻 Skillss",
])

if (pages == '👨‍💻 Home'):
    st.title("Rafael Cristofali")

    st.markdown('- 📝 Estudo programação desde 2018.')
    st.markdown('- 👔 Trabalho na área desde 2021.')
    st.markdown('- 💻 Tenho conhecimento Full Stack, mas gosto mais do Front-end.')
elif (pages == '📄 Formação e Experiência'):
    st.title('Experiência Profissional')
    st.markdown("- Engenheiro de software em Solid Gestão Empresarial (jan/2021 - o momento)")

    st.title('Formação Acadêmica')
    st.markdown("- Bacharelado em Engenharia de Software em FIAP (ago/2023 - jul/2027) ")
    st.markdown("- Curso Técnico de Informática em ETEC Lauro Gomes (jan/2018 - dez/2020) ")

    st.title('Licenças e Certificados')
    st.markdown("- FIAP - Web & Game Developing (mar/2025)")
    st.markdown("- FIAP - Design Thinking - Process (out/2023)")
    st.markdown("- FIAP - Gestão de Infraestrutura de TI (out/2023)")
    st.markdown("- Alura - Design System: projetando elementos (ago/2023)")
    st.markdown("- Google - Inovação e empreendedorismo com tecnologia Startup in School - Edição Online Google Brasil EAD categoria App Inventor (out/2019)")
elif (pages == '💻 Skills'):
    st.title('Tecnologias')
    st.markdown('- HTML')
    st.markdown('- CSS')
    st.markdown('- JavaScript')
    st.markdown('- React JS')
    st.markdown('- SQL')
    st.markdown('- C#')
    st.markdown('- Git')

st.sidebar.markdown("Desenvolvido por [Rafael Cristofali](https://github.com/Rafafaaa)")

# https://www.kaggle.com/datasets/fidelissauro/desmatamento-brasil

# distribuições binomial e normal