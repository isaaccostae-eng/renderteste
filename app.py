import streamlit as st
import numpy as np
import pandas as pd
import time

st.header('Jogando uma moeda')

# Estado persistente
if 'experiment_no' not in st.session_state:
    st.session_state.experiment_no = 0
if 'df_experiment_results' not in st.session_state:
    st.session_state.df_experiment_results = pd.DataFrame(
        columns=['no', 'iterations', 'mean']
    )

# Controles
number_of_trials = st.slider('Número de tentativas?', 1, 1000, 10)
animate = st.checkbox('Animar (mais lento)', value=True)
start_button = st.button('Executar')

# Inicializa o chart com um nome de série consistente
chart = st.line_chart(pd.DataFrame({'mean': [0.5]}))

def run_experiment(n: int, animate: bool = True, delay: float = 0.05) -> float:
    """
    Gera n lançamentos (0/1) com p=0.5, calcula as médias cumulativas (vectorizado)
    e atualiza o gráfico. Retorna a média final.
    """
    # amostras vetoriais (muito mais rápido que bernoulli.rvs em loops)
    samples = np.random.binomial(n=1, p=0.5, size=n)
    cumsum = np.cumsum(samples)
    counts = np.arange(1, n + 1)
    means = cumsum / counts  # vetor de médias cumulativas

    # Atualiza o gráfico: animação opcional
    if animate and n <= 1000:
        for m in means:
            chart.add_rows(pd.DataFrame({'mean': [m]}))
            time.sleep(delay)
    else:
        # atualiza tudo de uma vez (rápido)
        chart.add_rows(pd.DataFrame({'mean': means}))

    return float(means[-1]) if n > 0 else 0.0

if start_button:
    st.session_state.experiment_no += 1
    mean = run_experiment(number_of_trials, animate=animate)
    # registra resultado
    new_row = pd.DataFrame(
        [[st.session_state.experiment_no, number_of_trials, mean]],
        columns=['no', 'iterations', 'mean']
    )
    st.session_state.df_experiment_results = pd.concat(
        [st.session_state.df_experiment_results, new_row],
        ignore_index=True
    )

st.write(st.session_state.df_experiment_results)
