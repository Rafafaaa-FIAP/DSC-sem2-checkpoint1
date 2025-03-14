import pandas as pd
from scipy.stats import binom
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

st.set_page_config(page_title="Distribuições Probabilísticas", layout="wide")
st.logo("logo.png")

data = st.session_state["data"]

tab1, tab2 = st.tabs(
    ["Distribuição Binomial", "Distribuição Normal"])

with tab1:
    df = data

    def binomial_analysis(df, threshold):
        states = df.drop(['referencia', 'area_total_desmatamento'], axis=1)
        
        n = len(df)
        
        mean_deforestation = states.mean()
        
        p = (states > threshold).mean()
        
        binomial_results = {}
        for state in states.columns:
            k = (states[state] > threshold).sum()
            binomial_prob = binom.pmf(k, n, p[state])
            binomial_results[state] = {
                'successes': k,
                'probability': binomial_prob,
                'mean_deforestation': mean_deforestation[state]
            }
        
        return binomial_results, p

    st.title('Análise de Desmatamento na Amazônia com Distribuição Binomial')

    st.header('Parâmetros da Análise')
    threshold = st.slider('Limiar de Desmatamento (km²)', 
                                min_value=100, 
                                max_value=10000, 
                                value=1000,
                                step=100)

    results, probabilities = binomial_analysis(df, threshold)

    st.header('Interpretação')
    st.write("A análise de desmatamento na Amazônia utilizando a distribuição binomial é uma ferramenta crucial para entender padrões e probabilidades de eventos extremos de desmatamento em diferentes estados ao longo do tempo.")
    st.write("Ao estabelecer um limiar (threshold) de área desmatada, essa abordagem permite identificar a frequência com que cada estado supera esse limite, oferecendo uma perspectiva estatística sobre a gravidade e a consistência do problema em cada região. Isso é particularmente importante para a conservação ambiental, pois ajuda a priorizar áreas que necessitam de intervenções mais urgentes, além de fornecer uma base quantitativa para o planejamento de políticas públicas e a alocação de recursos.")
    st.write("Compreender as probabilidades associadas ao desmatamento excessivo também auxilia na avaliação de tendências históricas e na previsão de riscos futuros, contribuindo para estratégias de mitigação mais eficazes e informadas, essenciais para a preservação da biodiversidade e o combate às mudanças climáticas.")

    st.write(f"""
    Esta análise utiliza a distribuição binomial para modelar a probabilidade de desmatamento 
    acima de {threshold} km² em cada estado. 
    - 'successes': Número de anos em que o desmatamento excedeu o limiar.
    - 'probability': Probabilidade binomial associada.
    - 'mean_deforestation': Média anual de desmatamento por estado.
    """)

    st.header('Resultados da Análise')

    results_df = pd.DataFrame(results).T
    st.write('Resumo por Estado:')
    st.dataframe(results_df.style.format({
        'probability': '{:.4f}',
        'mean_deforestation': '{:.2f}'
    }))

    fig1 = px.bar(results_df, 
                x=results_df.index, 
                y='successes',
                title=f'Número de Anos com Desmatamento > {threshold} km² por Estado',
                labels={'x': 'Estado', 'successes': 'Número de Anos'},
                color='successes',
                color_continuous_scale='YlOrRd')
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1)

    fig2 = px.line(df, 
                x='referencia', 
                y='area_total_desmatamento',
                title='Desmatamento Total por Ano',
                labels={'referencia': 'Ano', 'area_total_desmatamento': 'Área Desmatada (km²)'})
    st.plotly_chart(fig2)

    heatmap_data = df.drop('area_total_desmatamento', axis=1).set_index('referencia')
    fig3 = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='YlOrRd'
    ))
    fig3.update_layout(
        title='Mapa de Calor do Desmatamento por Estado e Ano',
        xaxis_title='Estado',
        yaxis_title='Ano'
    )
    st.plotly_chart(fig3)
with tab2:
    df = data

    st.header("Filtros")
    estado = st.selectbox("Selecione o estado", 
                                ['Todos'] + list(df.columns[1:-1]))
    ano_inicio = st.slider("Ano inicial", 1988, 2022, 1988)
    ano_fim = st.slider("Ano final", 1988, 2022, 2022)

    if estado == 'Todos':
        dados_filtrados = df['area_total_desmatamento'][(df['referencia'] >= ano_inicio) & (df['referencia'] <= ano_fim)]
    else:
        dados_filtrados = df[estado][(df['referencia'] >= ano_inicio) & (df['referencia'] <= ano_fim)]

    st.title('Análise de Desmatamento na Amazônia com Distribuição Normal')

    st.subheader("Estatísticas Básicas")
    st.write(f"Média: {dados_filtrados.mean():.2f} km²")
    st.write(f"Desvio Padrão: {dados_filtrados.std():.2f} km²")
    st.write(f"Mínimo: {dados_filtrados.min()} km²")
    st.write(f"Máximo: {dados_filtrados.max()} km²")

    stat, p_value = stats.shapiro(dados_filtrados)
    st.subheader("Teste de Normalidade")
    st.write(f"Estatística do teste: {stat:.4f}")
    st.write(f"Valor p: {p_value:.4f}")
    if p_value > 0.05:
        st.write("Os dados parecem seguir uma distribuição normal (p > 0.05)")
    else:
        st.write("Os dados não seguem uma distribuição normal (p ≤ 0.05)")

    st.subheader("Interpretação dos Resultados")
    mean = dados_filtrados.mean()
    std = dados_filtrados.std()
    min_val = dados_filtrados.min()
    max_val = dados_filtrados.max()

    st.write("A análise de desmatamento na Amazônia utilizando a distribuição normal é fundamental para avaliar se os padrões de desmatamento em um estado ou na região como um todo seguem uma variação previsível e simétrica em torno de uma média, o que pode revelar a natureza dos processos subjacentes.")
    st.write("Essa abordagem permite identificar se o desmatamento é influenciado por fatores consistentes, como atividades econômicas regulares, ou por eventos extremos e imprevisíveis, como mudanças abruptas em políticas ambientais ou desastres naturais.")
    st.write("O teste de normalidade, aliado às visualizações como histogramas e Q-Q plots, oferece uma base estatística robusta para compreender a estabilidade e a variabilidade dos dados ao longo do tempo, enquanto as estatísticas descritivas (média, desvio padrão, mínimo e máximo) fornecem insights sobre a magnitude e a dispersão do problema. Essa análise é essencial para tomadores de decisão, pois ajuda a direcionar esforços de conservação, monitorar a eficácia de políticas ambientais e prever cenários futuros, contribuindo para a gestão sustentável da Amazônia e a mitigação de impactos climáticos e ecológicos.")

    interpretation = f"""
    Analisando os dados de desmatamento para {estado} entre {ano_inicio} e {ano_fim}:

    1. **Média ({mean:.2f} km²)**: Representa o valor médio de área desmatada por ano no período selecionado. 
    {'Isso indica um nível relativamente alto de desmatamento anual' if mean > 10000 else 'Isso sugere um desmatamento moderado a baixo em média'}.

    2. **Desvio Padrão ({std:.2f} km²)**: Mostra a variabilidade anual do desmatamento. 
    {'Um valor alto indica grandes flutuações ano a ano' if std > mean/2 else 'Um valor baixo sugere consistência nos níveis de desmatamento'}.

    3. **Mínimo ({min_val} km²) e Máximo ({max_val} km²)**: Refletem os extremos de desmatamento no período. 
    A diferença de {max_val - min_val} km² mostra a amplitude da variação.

    4. **Teste de Normalidade (p = {p_value:.4f})**: 
    {'Os dados seguem uma distribuição normal, sugerindo que os valores de desmatamento variam de forma simétrica em torno da média, o que pode indicar um processo natural ou políticas consistentes de controle' if p_value > 0.05 
    else 'Os dados não seguem uma distribuição normal, o que pode indicar eventos extremos, políticas inconsistentes ou influências externas significativas afetando o desmatamento'}.

    **Contexto**: {'Períodos com alta variabilidade podem estar associados a mudanças em políticas ambientais ou eventos específicos (ex.: secas, queimadas intencionais)' if std > mean/2 else 'A consistência sugere um padrão estável de desmatamento, possivelmente influenciado por fatores constantes como atividades econômicas regulares'}.
    """
    st.write(interpretation)

    st.subheader("Visualizações")

    hist_data = go.Histogram(
        x=dados_filtrados,
        histnorm='probability density',
        name='Histograma',
        opacity=0.7
    )
    mu, sigma = dados_filtrados.mean(), dados_filtrados.std()
    x = np.linspace(min(dados_filtrados), max(dados_filtrados), 100)
    y = stats.norm.pdf(x, mu, sigma)
    normal_curve = go.Scatter(
        x=x,
        y=y,
        name='Curva Normal',
        line=dict(color='red')
    )
    fig1 = go.Figure(data=[hist_data, normal_curve])
    fig1.update_layout(
        title=f"Distribuição do Desmatamento - {estado}",
        xaxis_title="Área Desmatada (km²)",
        yaxis_title="Densidade",
        bargap=0.2
    )
    st.plotly_chart(fig1)

    qq = stats.probplot(dados_filtrados, dist="norm")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=qq[0][0],
        y=qq[0][1],
        mode='markers',
        name='Dados'
    ))
    fig2.add_trace(go.Scatter(
        x=qq[0][0],
        y=qq[0][0],
        mode='lines',
        name='Linha Teórica',
        line=dict(color='red')
    ))
    fig2.update_layout(
        title=f"Q-Q Plot - {estado}",
        xaxis_title="Quantis Teóricos",
        yaxis_title="Quantis Observados"
    )
    st.plotly_chart(fig2)

    if estado == 'Todos':
        fig3 = px.line(df, x='referencia', y='area_total_desmatamento',
                    title="Desmatamento Total por Ano")
        fig3.update_layout(
            xaxis_title="Ano",
            yaxis_title="Área Desmatada (km²)"
        )
        st.plotly_chart(fig3)
    else:
        fig3 = px.line(df, x='referencia', y=estado,
                    title=f"Desmatamento em {estado} por Ano")
        fig3.update_layout(
            xaxis_title="Ano",
            yaxis_title="Área Desmatada (km²)"
        )
        st.plotly_chart(fig3)

st.sidebar.markdown("Desenvolvido por [Rafael Cristofali](https://github.com/Rafafaaa)")