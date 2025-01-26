import streamlit as st
import datetime
import calendar
import time
import pandas as pd
from workalendar.america import Brazil
from utils import load_custom_styles_and_info
from module_functions import (
    add_or_update_month_df_tp,
    create_df_tasks,
    create_df_tamanho_task,
    add_or_update_month_df_tamanho_task,
)
from helpers import (
    parse_month_year,
    format_month_year,
    next_month,
    init_session_states,
    last_month_in_df,
    persist_data,
)


def calculate_business_days(year: int, month: int) -> int:
    """
    Calculate the number of business days in a given month and year for Porto Alegre, Brazil.

    This function considers national holidays and can be extended to include municipal holidays.

    Parameters:
    year (int): The year for which business days need to be calculated.
    month (int): The month (1-12) for which business days need to be calculated.

    Returns:
    int: The number of business days within the given month.

    Complexity:
    Time: O(n), where n is the number of days in the given month.
    Space: O(1), constant space usage.
    """
    calendar_brazil = Brazil()

    first_day = datetime.date(year, month, 1)
    last_day = datetime.date(year, month, calendar.monthrange(year, month)[1])

    business_days = calendar_brazil.get_working_days_delta(first_day, last_day)
    return business_days


def add_new_month_form_df_tp():
    """
    Displays a form to add task quantity data for a given month/year in df_tp.

    This function guides the user through the process of adding task data for the next expected month, ensuring sequential consistency.

    Steps:
      - Identifies the **next expected month** (next_expected) based on the last registered month.
      - Displays an informative message with the last recorded month and the next **mandatory** month.
      - **Requires the user** to select the exact expected month/year; otherwise, an error message is shown.
      - Allows the user to enter values for "TP Adaptado (22 Dias Úteis)", displaying the calculated ideal and real values.
      - After validation, the data is saved and the DataFrame is updated.
      - Displays an **updated DataFrame view** after adding the new month.

    Returns:
    None

    Complexity:
    Time: O(n), where n is the number of months stored.
    Space: O(1), constant space usage aside from the updated DataFrame.
    """
    st.subheader(
        "Adicionar Informação de Quantidade de Tasks Feitas em um dado Mês/Ano"
    )
    """
      - Identifica o **PRÓXIMO mês esperado** (next_expected) com base no último mês cadastrado.
      - Exibe uma mensagem informativa com o último mês registrado e o próximo **obrigatório**.
      - **Obriga o usuário** a selecionar exatamente o mês/ano esperado; caso contrário, uma mensagem de erro é exibida.
      - Permite a inserção de valores para "TP Adaptado (22 Dias Úteis)", exibindo os valores ideais e reais calculados automaticamente.
      - Após a validação, os dados são salvos e o DataFrame atualizado.
      - Exibe uma **visualização atualizada do DataFrame** após a adição do novo mês.
    """

    last_month = last_month_in_df(st.session_state.df_tp)
    next_expected = next_month(last_month)

    st.info(
        f"O último mês cadastrado é **{last_month}**. O **próximo** mês obrigatório é **{next_expected}**."
    )

    year, month = parse_month_year(next_expected)
    default_date = datetime.date(year, month, 1)
    min_date = datetime.date(2025, 1, 1)

    chosen_date = st.date_input(
        "Selecione o Mês/Ano (Ignorar Dia)",
        value=default_date,
        min_value=min_date,
        help="Escolha exatamente o próximo mês em ordem. O dia não será considerado.",
    )
    chosen_mm_yy = format_month_year(chosen_date.year, chosen_date.month)

    c1, c2, c3 = st.columns(3)
    with c1:
        tp_adapt_22 = st.number_input(
            "TP Adaptado (22 Dias Úteis)", min_value=0, value=10, key="tp_adapt_update"
        )
    with c2:
        st.write("TP Ideal (15 Dias Úteis)")
        tp_ideal_22 = 15
        st.text(tp_ideal_22)
    with c3:
        business_days = calculate_business_days(chosen_date.year, chosen_date.month)
        st.write("Dias Úteis Reais")
        st.text(business_days)

    if st.button("Adicionar 🆕", key="button1"):
        if chosen_mm_yy != next_expected:
            st.error(
                f"Você tentou adicionar '{chosen_mm_yy}'. "
                f"O próximo mês obrigatório é '{next_expected}'. "
                f"Não é permitido pular meses!"
            )
            return
        st.session_state.work_days_dict[chosen_mm_yy] = business_days
        st.session_state.df_tp = add_or_update_month_df_tp(
            st.session_state.df_tp,
            st.session_state.df_tasks,
            st.session_state.work_days_dict,
            chosen_mm_yy,
            tp_adapt_22,
            tp_ideal_22,
            business_days,
        )
        st.success(
            f"Mês '{chosen_mm_yy}' adicionado com sucesso! Agora o último mês é {chosen_mm_yy}."
        )
    st.session_state.df_tp = recalculate_tp_row(chosen_mm_yy)
    st.markdown("#### Visualizar df_tp (após adição)")
    st.dataframe(st.session_state.df_tp)


def recalculate_tp_row(chosen_mm_yy: str):
    """
    Recalculates the TP values for a given month/year in the session state DataFrame.

    This function updates the columns by adding the revised task values from df_tasks to the respective month.

    Parameters:
    chosen_mm_yy (str): The month/year in 'MM/YY' format to be recalculated.

    Returns:
    DataFrame: The updated df_tp DataFrame stored in the session state.

    Complexity:
    Time: O(n), where n is the number of rows in df_tp.
    Space: O(1), constant space usage aside from the DataFrame storage.
    """
    df_tp = st.session_state.df_tp
    df_tasks = st.session_state.df_tasks
    row_index = df_tp[df_tp["Mês/Ano"] == chosen_mm_yy].index

    if not row_index.empty:
        idx = row_index[0]
        df_tasks_value = (
            df_tasks.at[idx, "TP Tasks Revisadas"]
            if chosen_mm_yy in df_tasks["Mês/Ano"].values
            else 0
        )
        df_tp.at[idx, "TP Adaptado (22 Dias Úteis) + Revisão Task"] = (
            df_tp.at[idx, "TP Adaptado (22 Dias Úteis)"] + df_tasks_value
        )
        df_tp.at[idx, "TP Ajustado (Dias Úteis Reais) + Revisão Task"] = (
            df_tp.at[idx, "TP Ajustado (Dias Úteis Reais)"] + df_tasks_value
        )
        st.session_state.df_tp = df_tp
    return st.session_state.df_tp


def update_existing_month_form_df_tp(callback=None):
    """
    Displays a form to update an existing month in the df_tp DataFrame stored in session state.

    This function allows users to select an existing month, modify values, and update the dataset.

    Parameters:
    callback (function, optional): A callback function to execute after updating the data.

    Returns:
    bool: True if the update was successful, False otherwise.

    Complexity:
    Time: O(n log n) due to sorting.
    Space: O(1), constant space usage.
    """
    st.subheader(
        "Atualizar Informação de Quantidade de Tasks Feitas em um dado Mês/Ano"
    )

    st.markdown(
        """
        Nesta seção, é possível atualizar os dados de um mês já cadastrado no sistema.
        
        - **Selecione um mês existente** na lista.
        - Modifique os valores de "TP Adaptado (22 Dias Úteis)", "TP Ideal (22 Dias Úteis)", e "Dias Úteis Reais".
        - Confirme a atualização para salvar as alterações.
        """
    )

    if st.session_state.df_tp.empty:
        st.warning("Não há nenhum mês cadastrado ainda!")
        return

    lista_meses = st.session_state.df_tp["Mês/Ano"].unique().tolist()
    lista_meses.sort(key=lambda x: parse_month_year(x))  # Sort chronologically
    mes_selecionado = st.selectbox(
        "Escolha um mês já cadastrado para atualizar",
        options=["-- Selecione --"] + lista_meses,
    )

    if mes_selecionado == "-- Selecione --":
        st.warning("Selecione um mês para prosseguir.")
        return

    df_tp = st.session_state.df_tp
    idx = df_tp.index[df_tp["Mês/Ano"] == mes_selecionado][0]
    val_adapt = int(df_tp.at[idx, "TP Adaptado (22 Dias Úteis)"])
    val_ideal = int(df_tp.at[idx, "TP Ideal (22 Dias Úteis)"])
    val_dias = st.session_state.work_days_dict.get(mes_selecionado, 22)

    st.info(f"Atualizando dados do mês {mes_selecionado}")

    c1, c2, c3 = st.columns(3)
    with c1:
        new_tp_adapt_22 = st.number_input(
            "TP Adaptado (22 Dias Úteis)", min_value=0, value=val_adapt
        )
    with c2:
        st.write("TP Ideal (22 Dias Úteis)")
        new_tp_ideal_22 = val_ideal
        st.text(val_ideal)
    with c3:
        new_dias_uteis = val_dias
        st.write("Dias Úteis Reais")
        st.text(new_dias_uteis)

    if st.button("Atualizar 🔄"):
        st.session_state.df_tp = add_or_update_month_df_tp(
            st.session_state.df_tp,
            st.session_state.df_tasks,
            st.session_state.work_days_dict,
            mes_selecionado,
            new_tp_adapt_22,
            new_tp_ideal_22,
            new_dias_uteis,
        )
        st.success(f"Mês '{mes_selecionado}' foi atualizado com sucesso!")
        st.session_state.df_tp = recalculate_tp_row(mes_selecionado)
        st.markdown("#### Visualizar df_tp (após atualização)")
        st.dataframe(st.session_state.df_tp)
        if callback:
            callback()
        return True

    st.markdown("#### Visualizar df_tp (após atualização)")
    st.dataframe(st.session_state.df_tp)
    return False


def add_df_rev_form(callback=None):
    """
    Displays a form to add or update the number of reviewed tasks for a given month/year.

    This function allows users to input and save data related to reviewed tasks in a sequential manner.

    Parameters:
    callback (function, optional): A callback function to execute after updating the data.

    Returns:
    bool: True if the update was successful, False otherwise.
    """
    st.subheader(
        "Adicionar Informação de Quantidade de Tasks Revisadas em um dado Mês/Ano"
    )
    st.markdown(
        """
        Nesta seção, é possível adicionar ou atualizar a quantidade de tasks revisadas para um mês específico.
        
        - **TP Tasks Revisadas**: Número de tasks revisadas durante o mês.
        - **TP Adaptado Tasks Revisadas**: Número de tasks revisadas ajustadas para 22 dias úteis.
        
        O sistema exige que os dados sejam adicionados em ordem cronológica para garantir a consistência.
        """
    )
    df_tasks = st.session_state.df_tasks
    if df_tasks is None:
        df_tasks = create_df_tasks(st.session_state.df_tp)
        st.session_state.df_tasks = df_tasks

    last_m = last_month_in_df(df_tasks)
    next_expected = next_month(last_m)

    st.info(
        f"Último mês cadastrado em df_tamanho_task é **{last_m}**. Agora só pode adicionar **{next_expected}**."
    )

    ano, mes = parse_month_year(next_expected)
    default_date = datetime.date(ano, mes, 1)

    chosen_date = st.date_input(
        "Selecione o Mês/Ano (ignorar dia)",
        value=default_date,
        key="tam_date_input_rev",
    )
    chosen_mm_yy = format_month_year(chosen_date.year, chosen_date.month)

    c1, c2 = st.columns(2)
    with c1:
        rev_task = st.number_input(
            "TP Tasks Revisadas", min_value=0, value=15, key="rev_tasks"
        )
    with c2:
        rev_task_adapt = st.number_input(
            "TP Adaptado Tasks Revisadas", min_value=0, value=15, key="adapt_rev_tasks"
        )

    if st.button("Adicionar 🆕", key="button2"):
        if chosen_mm_yy != next_expected:
            st.error(f"Você deve adicionar exatamente o mês {next_expected}.")
            return

        st.session_state.df_tasks = add_or_update_month_df_task(
            st.session_state.df_tasks,
            month_year=chosen_mm_yy,
            rev_task=rev_task,
            rev_task_adapt=rev_task_adapt,
        )
        st.success(f"Mês '{chosen_mm_yy}' adicionado/atualizado em df_tamanho_task.")
        st.session_state.df_tp = recalculate_tp_row(chosen_mm_yy)
        st.markdown("### df_tasks Atual")
        st.dataframe(st.session_state.df_tasks)
        if callback:
            callback()
        return True
    st.markdown("### df_tasks Atual")
    st.dataframe(st.session_state.df_tasks)
    return False


def add_or_update_month_df_task(
    df_tasks: pd.DataFrame, month_year: str, rev_task: int, rev_task_adapt: int
) -> pd.DataFrame:
    """
    Adds or updates a specific month entry in the df_tasks DataFrame.

    If the month/year already exists, it updates the respective task values; otherwise, it adds a new row.

    Parameters:
    df_tasks (pd.DataFrame): The DataFrame containing task data.
    month_year (str): The month/year in 'MM/YY' format to add or update.
    rev_task (int): The value to be set for "TP Tasks Revisadas".
    rev_task_adapt (int): The value to be set for "TP Adaptado Tasks Revisadas".

    Returns:
    pd.DataFrame: The updated DataFrame with the new or modified month entry.

    Complexity:
    Time: O(n), where n is the number of rows in df_tasks.
    Space: O(1), constant space usage aside from the DataFrame storage.
    """
    if month_year in df_tasks["Mês/Ano"].values:
        df_tasks.loc[df_tasks["Mês/Ano"] == month_year, "TP Tasks Revisadas"] = rev_task
        df_tasks.loc[
            df_tasks["Mês/Ano"] == month_year, "TP Adaptado Tasks Revisadas"
        ] = rev_task_adapt
    else:
        new_row = pd.DataFrame(
            {
                "Mês/Ano": [month_year],
                "TP Tasks Revisadas": [rev_task],
                "TP Adaptado Tasks Revisadas": [rev_task_adapt],
            }
        )
        df_tasks = pd.concat([df_tasks, new_row], ignore_index=True)
    return df_tasks


def add_df_tamanho_form(callback=None):
    """
    Displays a form to update the existing month in the df_tamanho_task DataFrame stored in session state.

    This function allows users to add or update the next expected month in the DataFrame.

    Parameters:
    callback (function, optional): A callback function to execute after updating the data.

    Returns:
    bool: True if the update was successful, False otherwise.

    Complexity:
    Time: O(n), where n is the number of rows in df_tamanho_task.
    Space: O(1), constant space usage aside from the DataFrame storage.
    """
    st.subheader("Adicionar Informação do Tamanho das Tasks Feitas em um dado Mês/Ano")

    st.markdown(
        """
        Nesta seção, é possível adicionar informações sobre o tamanho das tasks feitas para um Mês/Ano específico.
        
        - **Task P**: Pequena (TP Adaptado = 1)
        - **Task M**: Média   (TP Adaptado = 3)
        - **Task G**: Grande  (TP Adaptado = 5)
        
        O sistema exige que os dados sejam adicionados sequencialmente em relação ao Mês/ANo, garantindo consistência nos registros.
        """
    )

    if st.session_state.df_tamanho is None or st.session_state.df_tamanho.empty:
        st.warning("df_tamanho_task está vazio, não há o que atualizar.")
        return

    last_m = last_month_in_df(st.session_state.df_tamanho)  # If empty, returns 01/25
    next_expected = next_month(last_m)

    st.info(
        f"Último mês cadastrado em df_tamanho_task é **{last_m}**. Agora só pode adicionar **{next_expected}**."
    )

    year, month = parse_month_year(next_expected)
    default_date = datetime.date(year, month, 1)

    chosen_date = st.date_input(
        "Selecione o Mês/Ano (ignorar dia)", value=default_date, key="tam_date_input"
    )
    chosen_mm_yy = format_month_year(chosen_date.year, chosen_date.month)

    c1, c2, c3 = st.columns(3)
    with c1:
        new_p = st.number_input("Task P", min_value=0, value=3, key="update_tamP")
    with c2:
        new_m = st.number_input("Task M", min_value=0, value=5, key="update_tamM")
    with c3:
        new_g = st.number_input("Task G", min_value=0, value=1, key="update_tamG")

    if st.button("Adicionar 🆕", key="button3"):
        st.session_state.df_tamanho = add_or_update_month_df_tamanho_task(
            st.session_state.df_tamanho, chosen_mm_yy, new_p, new_m, new_g
        )
        st.success(f"Mês '{chosen_mm_yy}' atualizado em df_tamanho_task.")
        st.session_state.df_tp = recalculate_tp_row(chosen_mm_yy)
        st.markdown("### df_tamanho_task Atual")
        st.dataframe(st.session_state.df_tamanho)
        if callback:
            callback()
        return True
    st.markdown("### df_tamanho_task Atual")
    st.dataframe(st.session_state.df_tamanho)
    return False


def main():
    st.set_page_config(
        page_title="Adicionar/Atualizar Dados", page_icon="📝", layout="wide"
    )
    st.title("Adicionar ou Atualizar Dados de Produtividade 📝")

    init_session_states()

    if st.session_state.df_tasks is None or st.session_state.df_tasks.empty:
        st.session_state.df_tasks = create_df_tasks(st.session_state.df_tp)

    if st.session_state.df_tamanho is None or st.session_state.df_tamanho.empty:
        st.session_state.df_tamanho = create_df_tamanho_task(st.session_state.df_tp)

    load_custom_styles_and_info()

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🆕 Adicionar Dados Tasks 📋",
            "🆕 Adicionar Dados Tamanho Tasks 📏",
            "🆕 Adicionar Dados Tasks Revisadas 📑",
            "🔄 Atualizar Dados Tasks 📋",
        ]
    )

    def rerun_callback():
        st.session_state.need_rerun = True

    with tab1:
        add_new_month_form_df_tp()
        persist_data()

    with tab2:
        if add_df_tamanho_form(callback=rerun_callback):
            persist_data()

    with tab3:
        if add_df_rev_form(callback=rerun_callback):
            persist_data()

    with tab4:
        if update_existing_month_form_df_tp(callback=rerun_callback):
            persist_data()

    st.markdown("<br><br>", unsafe_allow_html=True)

    if st.session_state.get("need_rerun", False):
        st.session_state.need_rerun = False
        st.rerun()


if __name__ == "__main__":
    main()
