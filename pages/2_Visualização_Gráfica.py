import streamlit as st
from module_functions import (
    create_df_tasks,
    create_df_tamanho_task,
    create_df_produtividade_geral,
    get_layout_config,
    create_fig_tp,
    create_fig_tasks,
    create_fig_produtividade_geral,
    create_fig_tamanho_task,
    create_fig_all,
)
from helpers import init_session_states, persist_data
from utils import load_chart_tabs_styles


def prepare_dataframes():
    """
    Prepare and return the necessary dataframes from session state.

    Returns:
    tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        df_tp (productivity data), df_tasks (tasks data), df_tamanho (size data)

    Complexity:
    Time: O(n)
    Space: O(1)
    """
    df_tp = st.session_state.df_tp

    df_tasks = st.session_state.df_tasks
    if df_tasks is None or df_tasks.empty:
        df_tasks = create_df_tasks(df_tp)

    df_tamanho = st.session_state.df_tamanho
    if df_tamanho is None or df_tamanho.empty:
        df_tamanho = create_df_tamanho_task(df_tp)

    st.session_state.df_tasks = df_tasks
    st.session_state.df_tamanho = df_tamanho

    return df_tp, df_tasks, df_tamanho


def display_dataframes(df_tp, df_tasks, df_tamanho):
    """
    Display the final dataframes in an expandable section.

    Parameters:
    df_tp (pd.DataFrame): Productivity data
    df_tasks (pd.DataFrame): Tasks data
    df_tamanho (pd.DataFrame): Size data

    Returns:
    None

    Complexity:
    Time: O(1)
    Space: O(1)
    """
    st.markdown(
        """
    <style>
    .dataframe-container {
        overflow-x: auto;
        border: 1px solid #ccc; 
        border-radius: 8px;  
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Poppins', sans-serif; 
        font-size: 15px;
    }

    /* Cabeçalho da tabela */
    thead th {
        border: 1px solid #ccc !important;
        text-align: center !important;
        vertical-align: middle !important;
        padding: 12px !important;
        font-size: 18px !important;
        max-width: 120px !important; 
        white-space: normal !important; 
        word-wrap: break-word !important; 
        background-color: #000 !important;  /* Fundo preto */
        color: #fff !important;  /* Texto branco */
        font-weight: bold !important;
        text-transform: uppercase !important;
    }

    /* Interseção do cabeçalho com os índices (linha 0, coluna 0) */
    thead th:first-child {
        background-color: #000 !important;  /* Fundo preto */
        color: #fff !important;  /* Texto branco */
    }

    /* Células da tabela */
    tbody td {
        border: 1px solid #ddd !important;
        text-align: center !important;
        vertical-align: middle !important;
        padding: 10px !important;
        font-size: 18px !important;
        max-width: 100px !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        color: #1f1f1f !important;  
    }

    /* Centralizar os valores dos índices (primeira coluna) */
    tbody td:first-child {
        text-align: center !important;  /* Centraliza horizontalmente */
        vertical-align: middle !important; /* Centraliza verticalmente */
    }

    /* Alternância de cores na coluna de índices */
    tbody tr:nth-child(even) td:first-child {
        background-color: #c2bebe !important;  /* Cinza claro */
        font-weight: bold !important;  
        color: #000000 !important;  
    }

    tbody tr:nth-child(odd) td:first-child {
        background-color: #ffffff !important;  /* Branco */
        font-weight: bold !important;  
        color: #000000 !important;  
    }

    /* Linhas pares */
    tbody tr:nth-child(even) {
        background-color: #c2bebe !important; 
    }

    /* Linhas ímpares */
    tbody tr:nth-child(odd) {
        background-color: #ffffff !important;  
    }

    /* Efeito hover nas linhas pares */
    tbody tr:nth-child(even):hover {
        background-color: #92d18a !important; /* Cor de destaque no hover */
        outline: 3px solid #000000 !important; /* Borda visível ao redor */
        border-radius: 30px !important;
        transition: all 0.3s ease-in-out;
    }

    /* Efeito hover nas linhas ímpares */
    tbody tr:nth-child(odd):hover {
        background-color: #92d18a !important; /* Cor de destaque no hover */
        outline: 3px solid #000000 !important; /* Borda visível ao redor */
        border-radius: 30px !important;
        transition: all 0.3s ease-in-out;
    }

    /* Texto em negrito ao passar o mouse */
    tbody tr:hover td {
        font-weight: bold !important;
        transition: all 0.3s ease-in-out;
    }
    
    </style>
    """,
        unsafe_allow_html=True,
    )

    def format_floats(df):
        float_cols = df.select_dtypes(include=["float"]).columns
        return df.style.format({col: "{:.2f}" for col in float_cols})

    df_tp = format_floats(df_tp)
    df_tasks = format_floats(df_tasks)
    df_tamanho = format_floats(df_tamanho)

    st.markdown("## DataFrames Resultantes")
    with st.expander("DataFrames Resultantes"):
        st.markdown("### 📊 **Dataframe Tasks Realizadas/Mês-Ano**")
        st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
        st.table(df_tp)
        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📊 **Dataframe Tasks Revisadas/Mês-Ano**")
            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
            st.table(df_tasks)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("### 📊 **Dataframe Tamanho Tasks Realizadas/Mês-Ano**")
            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
            st.table(df_tamanho)
            st.markdown("</div>", unsafe_allow_html=True)


def render_charts(df_tp, df_tasks, df_tamanho, layout_config):
    """
    Generate and display charts in tabs.

    Parameters:
    df_tp (pd.DataFrame): Productivity data
    df_tasks (pd.DataFrame): Tasks data
    df_tamanho (pd.DataFrame): Size data
    layout_config (dict): Chart layout configuration

    Returns:
    None

    Complexity:
    Time: O(n)
    Space: O(1)
    """
    load_chart_tabs_styles()
    fig_tp = create_fig_tp(df_tp, layout_config)
    fig_tasks = create_fig_tasks(df_tasks, layout_config)
    df_prod_geral = create_df_produtividade_geral(df_tp, df_tasks)
    fig_produtividade_geral = create_fig_produtividade_geral(
        df_prod_geral, layout_config
    )
    fig_tamanho_task = create_fig_tamanho_task(df_tamanho)
    fig_all = create_fig_all(
        fig_tp, fig_tasks, fig_produtividade_geral, fig_tamanho_task
    )

    tab_names = [
        "Consolidado 🔗",
        "Produtividade Tasks 🔄",
        "Tasks Revisadas 🔍",
        "Produtividade Geral ⚙️",
        "Tamanho da Task 📏",
    ]

    figures = [fig_all, fig_tp, fig_tasks, fig_produtividade_geral, fig_tamanho_task]
    for tab, fig in zip(st.tabs(tab_names), figures):
        with tab:
            st.plotly_chart(fig, use_container_width=True)


def main():
    st.set_page_config(page_title="Visualização Gráfica", page_icon="📊", layout="wide")
    st.title("Visualização Gráfica 📊")

    init_session_states()
    layout_config = get_layout_config()

    df_tp, df_tasks, df_tamanho = prepare_dataframes()
    render_charts(df_tp, df_tasks, df_tamanho, layout_config)
    display_dataframes(df_tp, df_tasks, df_tamanho)
    persist_data()


if __name__ == "__main__":
    main()
