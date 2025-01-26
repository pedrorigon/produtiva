import streamlit as st


def main():
    st.set_page_config(page_title="Página Inicial", page_icon="🏠")

    st.title("Bem-vindo ao Produtiva 📝")
    st.markdown(
        """
        ### Sobre o Programa
        O **Produtiva APP** é uma ferramenta para gerenciar e visualizar
        dados de produtividade de Tarefas em diferentes períodos de tempo. 
        
        ### Funcionalidades Principais
        - **Atualizar Dados:**
            - Adicione novos meses e valores de produtividade, como TP (Task Performance) e número de tasks realizadas.
            - Atualize informações existentes para manter os dados sempre corretos e atualizados.
        
        - **Visualizar Gráficos:**
            - Gere gráficos interativos que permitem analisar o desempenho ao longo do tempo.
            - Compare diferentes métricas de produtividade para identificar tendências e padrões.
        
        ### Como Navegar
        Utilize o **menu lateral** para acessar as funcionalidades do aplicativo:
        1. **Adicionar ou Atualizar Dados:** Insira ou edite dados de produtividade com facilidade.
        2. **Analisar Gráficos:** Visualize insights detalhados por meio de gráficos interativos.
        
        Para começar, selecione a opção desejada no menu lateral e explore as possibilidades!
        """
    )


if __name__ == "__main__":
    main()
