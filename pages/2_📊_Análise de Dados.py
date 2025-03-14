import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Dados", layout="wide")
st.sidebar.markdown("Desenvolvido por [Rafael Cristofali](https://github.com/Rafafaaa)")
st.logo("logo.png")

df = st.session_state["data"]

st.title("Desmatamento da Região Norte do Brasil")

st.write("O desmatamento na Região Norte do Brasil é um dos desafios ambientais mais urgentes, ameaçando a biodiversidade, os povos indígenas e o equilíbrio climático global. Impulsionado por atividades como a expansão agropecuária, a extração ilegal de madeira e a mineração, o desmatamento tem avançado rapidamente, resultando na perda de milhares de hectares de floresta por ano.")

st.write("Além de comprometer os ecossistemas, a degradação da Amazônia intensifica as emissões de gases de efeito estufa, impactando o regime de chuvas e aumentando os riscos de mudanças climáticas. O combate ao desmatamento exige políticas públicas eficazes, fiscalização rigorosa e o incentivo a práticas sustentáveis que conciliem desenvolvimento econômico e preservação ambiental.")

st.write("Os dados utilizado para a análise foram coletados a partir do PRODES, um projeto da INPE (Instituto Nacional de Pesquisas Espaciais) - http://www.obt.inpe.br/OBT/assuntos/programas/amazonia/prodes")

st.write("Os dados apresentam a área desmatada em km² desde 1988 até 2022 nos estados da região norte do Brasil")

st.subheader("Tipos de variáveis:")

dfTpVar = pd.DataFrame([['referencia', 'o ano de referencia', 'Quantitativa Discreta'],
                        ['area de desmatamento', 'todos os valores de cada estado', 'Quantitativa Contínua']],
                        columns=['Nome', 'Descrição', 'Tipo'])
st.dataframe(dfTpVar)

st.subheader("Durante toda a análise vamos conseguir responder algumas pergunta como:")
st.markdown("- Qual é a média anual de desmatamento em um estado específico ou em toda a Amazônia em um período determinado?")
st.markdown("- Qual é a variabilidade (desvio padrão) do desmatamento em uma região ao longo do tempo?")
st.markdown("- Quantos anos um estado excedeu um limiar específico de desmatamento, como 1000 km²?")
st.markdown("- Qual é a probabilidade de um estado ultrapassar um certo nível de desmatamento em um ano típico?")
st.markdown("- Os dados de desmatamento de um estado ou da Amazônia total seguem uma distribuição normal?")
st.markdown("- Quão simétricos ou consistentes são os valores de desmatamento em torno da média?")

st.header("Estatísticas e Visualizações")
st.subheader("Filtros")
estado = st.selectbox("Selecione o estado", 
                     ['Todos'] + list(df.columns[1:-1]))
ano_inicio = st.slider("Ano inicial", 1988, 2022, 1988)
ano_fim = st.slider("Ano final", 1988, 2022, 2022)

if estado == 'Todos':
    dados_filtrados = df[['referencia', 'area_total_desmatamento']][(df['referencia'] >= ano_inicio) & (df['referencia'] <= ano_fim)]
    coluna_plot = 'area_total_desmatamento'
else:
    dados_filtrados = df[['referencia', estado]][(df['referencia'] >= ano_inicio) & (df['referencia'] <= ano_fim)]
    coluna_plot = estado

st.write(f"Média: {dados_filtrados[coluna_plot].mean():.2f} km²")
st.write(f"Desvio Padrão: {dados_filtrados[coluna_plot].std():.2f} km²")
st.write(f"Mínimo: {dados_filtrados[coluna_plot].min()} km²")
st.write(f"Máximo: {dados_filtrados[coluna_plot].max()} km²")

fig_linha = px.line(dados_filtrados, 
                   x='referencia', 
                   y=coluna_plot,
                   title=f'Evolução do Desmatamento - {estado}',
                   labels={'referencia': 'Ano', 
                          coluna_plot: 'Área Desmatada (km²)'})
fig_linha.update_layout(
    xaxis_title="Ano",
    yaxis_title="Área Desmatada (km²)",
    template="plotly_white"
)

st.write("Quando todos os estados estão selecionados podemos identificar que houve 2 picos, um em 1995 e o outro em 2004, após esse ano houve uma queda, voltando a subir somente 2015 e voltou a diminuir somente em 2021 onde estava num nível parecido com o ano de 2008.")

fig_dispersao = px.scatter(dados_filtrados, 
                         x='referencia', 
                         y=coluna_plot,
                         title=f'Dispersão do Desmatamento - {estado}',
                         labels={'referencia': 'Ano', 
                                coluna_plot: 'Área Desmatada (km²)'},
                         size=coluna_plot,
                         hover_data=['referencia', coluna_plot])
fig_dispersao.update_layout(
    xaxis_title="Ano",
    yaxis_title="Área Desmatada (km²)",
    template="plotly_white"
)

st.plotly_chart(fig_linha)
st.plotly_chart(fig_dispersao)

st.subheader("Dados utilizados")

st.dataframe(df)
