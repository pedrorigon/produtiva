import streamlit as st


def load_custom_styles_and_info():
    content = """
    <style>
    /* Aumenta o espaço acima das abas para evitar cortes */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        gap: 20px;
        padding: 30px 0 20px;
        justify-content: center;
        position: relative;
    }

    /* Gradiente ajustado com transição entre vermelho, roxo e azul para abas */
    .stTabs [data-baseweb="tab"]:nth-child(1) {
        background: linear-gradient(to right, #8B0000, #B22222);
        box-shadow: 0px 12px 35px rgba(139, 0, 0, 0.7);
    }

    .stTabs [data-baseweb="tab"]:nth-child(2) {
        background: linear-gradient(to right, #B22222, #800080);
        box-shadow: 0px 12px 35px rgba(178, 34, 34, 0.7);
    }

    .stTabs [data-baseweb="tab"]:nth-child(3) {
        background: linear-gradient(to right, #800080, #00008B);
        box-shadow: 0px 12px 35px rgba(128, 0, 128, 0.7);
    }

    .stTabs [data-baseweb="tab"]:nth-child(4) {
        background: linear-gradient(to right, #00008B, #000033);
        box-shadow: 0px 12px 35px rgba(0, 0, 139, 0.7);
    }

    .stTabs [data-baseweb="tab"] {
        border: 1px solid #ccc;
        padding: 14px 38px;
        border-radius: 40px;
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 1px 1px 4px rgba(0,0,0,1);
        transition: all 0.3s ease-in-out;
        cursor: pointer;
        position: relative;
    }

    /* Hover específico para cada aba */
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-3px);
    }

    /* Botão personalizado */
    .stButton.normal-button button {
        background: linear-gradient(to right, #3decb7, #1bc47d);
        box-shadow: 0px 4px 15px rgba(50, 205, 50, 0.5);
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 12px 40px;
        border-radius: 25px;
        border: none;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        transition: all 0.3s ease-in-out;
        cursor: pointer;
        outline: none;
    }

    .stButton.normal-button button:hover {
        font-weight: bolder;
        border: 5px solid white;
        box-shadow: 0px 15px 50px rgba(50, 205, 50, 0.9);
        color: white;
        font-size: 24px;
    }

    /* Responsividade */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            padding: 10px 25px;
            font-size: 16px;
        }
        .stButton.normal-button button {
            font-size: 18px;
            padding: 10px 35px;
        }
    }

    .stButton > button {
        background: linear-gradient(to right, #3decb7, #1bc47d);
        box-shadow: 0px 3px 8px rgba(50, 205, 50, 0.3);
        color: white !important;
        font-size: 20px;
        font-weight: bold;
        padding: 10px 35px;
        border-radius: 25px;
        border: none;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.4);
        transition: background 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        cursor: pointer;
        outline: none;
    }

    /* Hover: mudança sutil de tonalidade e borda preta na fonte para visibilidade */
    .stButton > button:hover {
        background: linear-gradient(to right, #2ecc71, #27ae60);
        border: 2px solid #ffffff;
        box-shadow: 0px 6px 15px rgba(50, 205, 50, 0.5);
        color: white !important;
        text-shadow: 
            -1px -1px 2px black, 
            1px -1px 2px black, 
            -1px 1px 2px black, 
            1px 1px 2px black;
    }
    </style>
    """
    st.markdown(content, unsafe_allow_html=True)


def load_chart_tabs_styles():
    content = """
    <style>
    /* Aumenta o espaço acima das abas para evitar cortes */
    .stTabs [data-baseweb="tab-list"] {
        display: flex;
        gap: 20px;
        padding: 30px 0 20px;
        justify-content: center;
        position: relative;
    }

    /* Gradiente ajustado para 5 abas com transições suaves */
    .stTabs [data-baseweb="tab"]:nth-child(1) {
        background: linear-gradient(to right, #8B0000, #B22222);
        box-shadow: 0px 12px 35px rgba(139, 0, 0, 0.7);
    }

    .stTabs [data-baseweb="tab"]:nth-child(2) {
        background: linear-gradient(to right, #B22222, #800080);
        box-shadow: 0px 12px 35px rgba(178, 34, 34, 0.7);
    }

    .stTabs [data-baseweb="tab"]:nth-child(3) {
        background: linear-gradient(to right, #800080, #4B0082);
        box-shadow: 0px 12px 35px rgba(128, 0, 128, 0.7);
    }

    .stTabs [data-baseweb="tab"]:nth-child(4) {
        background: linear-gradient(to right, #4B0082, #00008B);
        box-shadow: 0px 12px 35px rgba(75, 0, 130, 0.7);
    }

    .stTabs [data-baseweb="tab"]:nth-child(5) {
        background: linear-gradient(to right, #00008B, #000033);
        box-shadow: 0px 12px 35px rgba(0, 0, 139, 0.7);
    }

    /* Estilo geral das abas */
    .stTabs [data-baseweb="tab"] {
        border: 1px solid #ccc;
        padding: 14px 38px;
        border-radius: 40px;
        font-size: 18px;
        font-weight: bold;
        color: #ffffff;
        text-shadow: 1px 1px 4px rgba(0,0,0,1);
        transition: all 0.3s ease-in-out;
        cursor: pointer;
        position: relative;
    }

    /* Efeito hover para cada aba */
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-3px);
    }

    .stTabs [data-baseweb="tab"]:nth-child(1):hover {
        box-shadow: 0px 20px 50px rgba(139, 0, 0, 0.9);
    }

    .stTabs [data-baseweb="tab"]:nth-child(2):hover {
        box-shadow: 0px 20px 50px rgba(178, 34, 34, 0.9);
    }

    .stTabs [data-baseweb="tab"]:nth-child(3):hover {
        box-shadow: 0px 20px 50px rgba(128, 0, 128, 0.9);
    }

    .stTabs [data-baseweb="tab"]:nth-child(4):hover {
        box-shadow: 0px 20px 50px rgba(75, 0, 130, 0.9);
    }

    .stTabs [data-baseweb="tab"]:nth-child(5):hover {
        box-shadow: 0px 20px 50px rgba(0, 0, 139, 0.9);
    }
    </style>
    """
    st.markdown(content, unsafe_allow_html=True)
