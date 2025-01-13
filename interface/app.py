import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Chatbot de Análise de Dados",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Chatbot de Análise de Dados")
st.markdown("""
### Objetivo
Este chatbot foi desenvolvido para auxiliar usuários em tarefas de análise de dados demográficos e estatísticos de um conjunto de dados específico.
É importante que suas perguntas esteja relacionadas aos dados fornecidos. Para mais informações sobre os dados, clique na seção "Sobre os Dados 📊" na barra lateral.

---

### O que você pode perguntar?
- Qual o estado com maior taxa de inadimplência?
- Qual o percentual de mulheres que faleceram em cada estado?
- Qual a idade média por estado?
""")

with st.sidebar:
    with st.expander("Sobre os Dados 📊"):
        st.markdown("""
        Este chatbot utiliza um conjunto de dados relacionados a pessoas e registros demográficos. 

        **Descrição das colunas principais:**
        - **Data:** Data de referência do registro (janeiro a agosto de 2017).
        - **Sexo:** Masculino ou Feminino.
        - **Idade:** Idade em anos.
        - **UF:** Unidade Federativa (estado brasileiro).
        - **Indicativo Óbito:** Indica se o indivíduo registrado faleceu.
        - **Classe Social:** Classe estimada do indivíduo.

        **Exemplo de perguntas:**
        - "Qual estado tem mais pessoas falecidas?"
        - "Qual a idade média por estado?"
        - "Quantas pessoas faleceram com mais de 50 anos?"
        """)

    st.markdown("Desenvolvido por [Arthur Almeida](https://github.com/arthuraal)")

st.markdown("---")
col1, col2 = st.columns([2, 1])
with col1:
    st.header("Faça sua Pergunta")
    question = st.text_input("Digite sua pergunta:", placeholder="Exemplo: Qual o estado com mais registros de óbito?")
with col2:
    st.header("Configurações")
    model = st.selectbox("Escolha o modelo:", ["GPT-4o mini", "Llama 3.3 70B Instruct"])

if st.button("Enviar"):
    if question:
        with st.spinner("Processando..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/query/",
                    json={"question": question, "model": model}
                )
                if response.status_code == 200:
                    result = response.json().get("result", {})
                    st.success("Resposta gerada com sucesso!")
                    st.markdown("---")
                    st.header("Resposta:")
                    st.markdown(result.get("message", "Nenhum dado encontrado."))
                else:
                    st.error("O backend não está disponível. Por favor, verifique.")

            except Exception as e:
                st.error(f"Erro ao conectar com o backend: {e}")
    else:
        st.warning("Por favor, digite uma pergunta.")

st.markdown("---")
st.markdown("🔍 Precisa de ajuda? Consulte [a documentação](https://github.com/arthuraal/data-analyst-chatbot?tab=readme-ov-file)")

