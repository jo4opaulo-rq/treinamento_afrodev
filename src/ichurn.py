import streamlit as st
import pandas as pd
import pickle
import shap
import numpy as np
from xgboost.sklearn import XGBClassifier
import plotly.graph_objects as go
import plotly.express as px

#Carregando arquivos iniciais
@st.cache
def read_data():

    """
    ler os arquivos e modelos
    """

    dados_treino = pd.read_pickle('../data/streamlit/train.pkl')
    features = pd.read_csv('../data/streamlit/features.txt', header=None)[0].tolist()

    return dados_treino, features


with open('../data/streamlit/classificador.pkl', 'rb') as file:
    modelo = pickle.load(file)

#expaliner do shap
explainer = shap.Explainer(modelo)


st.title('Bem vindos ao Churn Detector')
dados_treino, features = read_data()
limites = dados_treino[features].apply([min, max, 'mean']).to_dict() #limites das variáveis do modelo


#----------------------------------configurando as variáveis de entrada do modelo--------------------------------
st.sidebar.title('Variáveis do modelo')

prediction = {} #esse dicionario vai guardar todas as variáveis necessárias para fazer uma predição do modelo

prediction['Age'] = st.sidebar.slider(
    label = 'Idade', 
    min_value = limites['Age']['min'], 
    max_value = limites['Age']['max'],
    value= limites['Age']['mean']
)

prediction['Balance'] = st.sidebar.slider(
    label = 'Balanço na conta', 
    min_value = limites['Balance']['min'], 
    max_value = limites['Balance']['max'],
    value= limites['Balance']['mean']
)


prediction['NumOfProducts'] = st.sidebar.slider(
    label = 'Numero de Produtos', 
    min_value = int(limites['NumOfProducts']['min']), 
    max_value = int(limites['NumOfProducts']['max']),
    value= int(limites['NumOfProducts']['min']),
    step=1
)


membro_ativo = st.sidebar.radio(
    label = "É membro ativo?", 
    options=['Sim', 'Não']
)

prediction['IsActiveMember'] = 1 if membro_ativo == "Sim" else 0


nacionalidade = st.sidebar.radio(
    label = "Nacionalidade do Cliente", 
    options=['França', 'Alemanha']
)

prediction['Geography_isFrance'] = 1 if nacionalidade == 'França' else 0
prediction['Geography_isGermany'] = 1 if nacionalidade == 'Alemanha' else 0


genero = st.sidebar.radio(
    label = "Gênero", 
    options=['Homem', 'Mulher']
)

prediction['Gender_isFemale'] = 1 if genero == 'Mulher' else 0


c1, c2 = st.beta_columns(2)

#----------------------------------------------------Realizando uma predição----------------------------------------------
if st.sidebar.button('Calcular'):
    
    preds = pd.DataFrame([prediction])
    probabilidades = modelo.predict_proba(preds)
    predicao_classe_churn = modelo.predict(preds)

    probabilidade_de_fazer_churn = np.round(100*probabilidades[0, 1],2)

    pronome = "O" if prediction['Gender_isFemale'] == 0 else "A"


    if predicao_classe_churn[0] == 1:
        st.error(f'Oh não....{pronome} cliente quer deixar a empresa :( Mas ainda dá tempo de fazer alguma coisa!')
    else:
        st.success(f'{pronome} cliente parece estar satisfeito com a empresa e não vai nos deixar!')
    
    st.text(f"A probabilidade desse cliente deixar a empresa é de {probabilidade_de_fazer_churn}%")

    shap_values = explainer(preds)

    def fazer_grafico_cascata(shap_values, features):

        """
        Transformamos a cascata do nosso exemplo da regressão numa função:

        recebe um shap_values e uma lista de features. Retorna um objeto gráfico do plotly

        """

        explicacao_shap = pd.DataFrame(
            data = zip(
                features,
                shap_values[0].data,
                shap_values[0].values),
            columns = [
                'feature',
                'valor_da_feature',
                'impacto_shap'
        ])

        explicacao_shap = explicacao_shap.sort_values(
            by='impacto_shap', 
            ascending=False, 
            key=abs).reset_index(drop=True) # key=abs para ordenar pelo módulo

        explicacao_shap['measure'] = 'relative'

        #criando a primeira barra da ponte
        df_base_value = pd.DataFrame(
        data = [{
            'feature': 'Valor Base',
            'valor_da_feature': "Valor Base",
            'impacto_shap' : shap_values[0].base_values,
            'measure': 'absolute'
        }])


        #criando a ultima barra da ponte
        df_valor_final = pd.DataFrame(
        data = [{
            'feature': 'Predição final',
            'valor_da_feature': 'Valor final',
            'impacto_shap' : df_base_value['impacto_shap'][0] + explicacao_shap['impacto_shap'].sum(),
            'measure': 'total'
        }])

        tabela_para_cascata = pd.concat([df_base_value, explicacao_shap, df_valor_final], ignore_index=True)

        fig = go.Figure(go.Waterfall(
            name = "20", orientation = "v",
            measure = tabela_para_cascata['measure'].tolist(),
            x = tabela_para_cascata['feature'],
            textposition = "outside",
            hovertext = tabela_para_cascata['valor_da_feature'],
            y = tabela_para_cascata['impacto_shap'],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
            decreasing = {"marker":{"color":"Green"}},
            increasing = {"marker":{"color":"Red"}},
            totals = {"marker": {"color": "Grey"}}
        ))

        fig.update_layout({
            'title': 'Quais fatores estão direcionando essa decisão do cliente?',
            'xaxis_title': 'Variável',
            'yaxis_title': 'Impacto SHAP'
        })

        
        return fig

    fig = fazer_grafico_cascata(shap_values, features)
    st.plotly_chart(fig)