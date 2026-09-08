import streamlit as st
import numpy as np
import pandas as pd
import time

st.header('Jogando uma moeda')

if 'experiment_no' not in st.session_state:
    st.session_state.experiment_no = 0
if 'df_experiment_results' not in st.session_state:
    st.session_state.df_experiment_results = pd.DataFrame(columns=['no', 'iterations', 'mean'])

number_of_trials = st.slider('Número de tentativas?', 1, 1000, 10)
animate = st.checkbox('Animar (mais lento)', value=True)
start_button = st.button('Executar')

# placeholder pro gráfico - CORREÇÃO do add_rows
chart_placeholder = st.empty()
chart_placeholder.line_chart(pd.DataFrame({'mean': [0.5]}))

def run_experiment(n: int, animate: bool = True, delay: float = 0.05) -> float:
    samples = np.random.binomial(n=1, p=0.5, size=n)
    means = np.cumsum(samples) / np.arange(1, n + 1)

    if animate and n <= 200: # limitei pra 200 pra não travar
        chart_data = []
        for m in means:
            chart_data.append(m)
            chart_placeholder.line_chart(pd.DataFrame({'mean': chart_data}))
            time.sleep(delay)
    else:
        chart_placeholder.line_chart(pd.DataFrame({'mean': means}))

    return float(means[-1]) if n > 0 else 0.0

if start_button:
    st.session_state.experiment_no += 1
    mean = run_experiment(number_of_trials, animate=animate)
    
    new_row = pd.DataFrame([[st.session_state.experiment_no, number_of_trials, mean]],
                           columns=['no', 'iterations', 'mean'])
    
    st.session_state.df_experiment_results = pd.concat(
        [st.session_state.df_experiment_results, new_row], ignore_index=True
    )

st.write(st.session_state.df_experiment_results)
