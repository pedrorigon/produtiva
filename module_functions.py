import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.subplots as sp

DATA_TP_CREATE = {
    "Mês/Ano": [
        "04/24",
        "05/24",
        "06/24",
        "07/24",
        "08/24",
        "09/24",
        "10/24",
        "11/24",
        "12/24",
        "01/25",
    ],
    "TP Adaptado (22 Dias Úteis)": [12, 9, 4, 19, 19, 2, 21, 17, 26, 10],
    "TP Ideal (22 Dias Úteis)": [15] * 10,
}

WORK_DAYS_POA_CREATE = {
    "04/24": 22,
    "05/24": 22,
    "06/24": 20,
    "07/24": 23,
    "08/24": 22,
    "09/24": 21,
    "10/24": 23,
    "11/24": 20,
    "12/24": 15,
    "01/25": 20,
}

DATA_TASKS_BASE = {
    "Mês/Ano": [
        "04/24",
        "05/24",
        "06/24",
        "07/24",
        "08/24",
        "09/24",
        "10/24",
        "11/24",
        "12/24",
        "01/25",
    ],
    "TP Tasks Revisadas": [0, 1, 0, 3, 4, 2, 7, 14, 11, 2],
    "TP Adaptado Tasks Revisadas": [0, 1, 0, 7, 4, 4, 12, 16, 19, 2],
}

DATA_TAMANHO_TASK_BASE = {
    "Mês/Ano": [
        "04/24",
        "05/24",
        "06/24",
        "07/24",
        "08/24",
        "09/24",
        "10/24",
        "11/24",
        "12/24",
        "01/25",
    ],
    "Task P": [6, 3, 1, 5, 1, 2, 5, 9, 10, 4],
    "Task M": [2, 2, 1, 3, 6, 0, 2, 1, 2, 2],
    "Task G": [0, 0, 0, 1, 0, 0, 2, 1, 2, 0],
}


def create_df_tp():
    """
    Creates a DataFrame containing task productivity data for specific months.

    This function initializes a DataFrame with predefined values for monthly productivity,
    calculates adjusted productivity based on actual working days, and returns the finalized DataFrame.

    Returns:
    pd.DataFrame: A DataFrame containing the columns 'Mês/Ano', 'TP Adaptado (22 Dias Úteis)',
    'TP Ideal (22 Dias Úteis)', 'Dias Úteis', 'TP Ajustado (Dias Úteis Reais)',
    and 'TP Ideal Ajustado (Dias Úteis Reais)'.

    Complexity:
    Time: O(n), where n is the number of months.
    Space: O(n), for storing the productivity data.
    """
    df_tp = pd.DataFrame(DATA_TP_CREATE)
    df_tp["Dias Úteis"] = df_tp["Mês/Ano"].map(WORK_DAYS_POA_CREATE)

    df_tp["TP Ajustado (Dias Úteis Reais)"] = df_tp["TP Adaptado (22 Dias Úteis)"] * (
        22 / df_tp["Dias Úteis"]
    )
    df_tp["TP Ideal Ajustado (Dias Úteis Reais)"] = df_tp[
        "TP Ideal (22 Dias Úteis)"
    ] * (df_tp["Dias Úteis"] / 22)

    return df_tp


def get_layout_config():
    """
    Generates a dictionary with layout configurations for Plotly charts.

    This function returns a dictionary containing styling parameters for axis titles,
    fonts, legend, and chart title placement to ensure consistency across visualizations.

    Returns:
    dict: A dictionary with customized layout settings for Plotly charts.

    Complexity:
    Time: O(1), constant time to return the predefined configuration.
    Space: O(1), constant space for the layout dictionary.
    """
    return dict(
        xaxis_title="Mês/Ano",
        yaxis_title="Produtividade",
        hovermode="x unified",
        xaxis=dict(
            title_font=dict(
                size=26, family="Arial, sans-serif", color="black", weight="bold"
            ),
            tickfont=dict(size=20, family="Arial, sans-serif", color="black"),
        ),
        yaxis=dict(
            title_font=dict(
                size=26, family="Arial, sans-serif", color="black", weight="bold"
            ),
            tickfont=dict(size=20, family="Arial, sans-serif", color="black"),
        ),
        title=dict(
            x=0.5,
            xanchor="center",
            font=dict(
                size=34, family="Arial, sans-serif", color="black", weight="bold"
            ),
        ),
        legend=dict(
            font=dict(size=20, family="Arial, sans-serif", color="black", weight="bold")
        ),
    )


def create_fig_tp(df_tp, layout_config):
    """
    Generates a line chart to visualize task productivity trends.

    This function processes the input productivity DataFrame by transforming it into a long format,
    allowing visualization of different productivity metrics over time.

    Parameters:
    df_tp (pd.DataFrame): DataFrame containing productivity data with columns 'Mês/Ano',
        'TP Adaptado (22 Dias Úteis)', 'TP Ajustado (Dias Úteis Reais)',
        'TP Ideal (22 Dias Úteis)', 'TP Ideal Ajustado (Dias Úteis Reais)'.
    layout_config (dict): Dictionary containing layout configurations for the chart.

    Returns:
    plotly.graph_objs._figure.Figure: A Plotly figure object representing the task productivity trends.

    Complexity:
    Time: O(n), where n is the number of rows in df_tp.
    Space: O(n), since a melted version of the DataFrame is created.
    """
    df_tp_melted = df_tp.melt(
        id_vars=["Mês/Ano"],
        value_vars=[
            "TP Adaptado (22 Dias Úteis)",
            "TP Ajustado (Dias Úteis Reais)",
            "TP Ideal (22 Dias Úteis)",
            "TP Ideal Ajustado (Dias Úteis Reais)",
        ],
        var_name="Tipo de TP",
        value_name="Valor",
    )

    color_map = {
        "TP Adaptado (22 Dias Úteis)": "#2F4F4F",
        "TP Ajustado (Dias Úteis Reais)": "#8B0000",
        "TP Ideal (22 Dias Úteis)": "#000080",
        "TP Ideal Ajustado (Dias Úteis Reais)": "#00FF00",
    }

    fig = px.line(
        df_tp_melted,
        x="Mês/Ano",
        y="Valor",
        color="Tipo de TP",
        markers=True,
        title="Produtividade Tasks",
        line_shape="spline",
        color_discrete_map=color_map,
    )
    fig.update_traces(line=dict(width=4))
    fig.update_layout(**layout_config, title_text="Produtividade Tasks", title_x=0.36)

    return fig


def create_df_tasks(df_tp):
    """
    Generates a tasks DataFrame by merging base data with existing months in df_tp.

    This function returns a DataFrame containing the months from df_tp and merges it with predefined task data.
    If there are new months in df_tp, they will be included with default values of 0.

    Parameters:
    df_tp (pd.DataFrame): DataFrame containing months to be merged with the task base data.

    Returns:
    pd.DataFrame: A DataFrame containing task productivity per month/year.

    Complexity:
    Time: O(n), where n is the number of months.
    Space: O(n), for storing the task data.
    """
    df_tasks_base = pd.DataFrame(DATA_TASKS_BASE)

    df_tasks_merged = pd.merge(
        df_tp[["Mês/Ano"]], df_tasks_base, on="Mês/Ano", how="left"
    )
    df_tasks_merged["TP Tasks Revisadas"] = df_tasks_merged[
        "TP Tasks Revisadas"
    ].fillna(0)
    df_tasks_merged["TP Adaptado Tasks Revisadas"] = df_tasks_merged[
        "TP Adaptado Tasks Revisadas"
    ].fillna(0)

    return df_tasks_merged


def create_fig_tasks(df_tasks, layout_config):
    """
    Generates a line chart for reviewed task productivity.

    This function creates a Plotly line chart by transforming the input DataFrame into a long format,
    allowing visualization of the number of reviewed and adapted tasks over different months.

    Parameters:
    df_tasks (pd.DataFrame): DataFrame containing reviewed task data with columns 'Mês/Ano', 'TP Tasks Revisadas', and 'TP Adaptado Tasks Revisadas'.
    layout_config (dict): Dictionary containing layout configurations for the chart.

    Returns:
    plotly.graph_objs._figure.Figure: A Plotly figure object representing the reviewed task productivity trends.

    Complexity:
    Time: O(n), where n is the number of rows in df_tasks.
    Space: O(n), since a melted version of the DataFrame is created.
    """
    df_tasks_melted = df_tasks.melt(
        id_vars=["Mês/Ano"],
        value_vars=["TP Tasks Revisadas", "TP Adaptado Tasks Revisadas"],
        var_name="Tipo de TP",
        value_name="Valor",
    )

    color_map = {
        "TP Tasks Revisadas": "#006400",
        "TP Adaptado Tasks Revisadas": "#8B0000",
    }

    fig = px.line(
        df_tasks_melted,
        x="Mês/Ano",
        y="Valor",
        color="Tipo de TP",
        markers=True,
        title="Produtividade Tasks Revisadas",
        line_shape="spline",
        color_discrete_map=color_map,
    )
    fig.update_traces(line=dict(width=4))
    fig.update_layout(
        **layout_config, title_text="Produtividade Tasks Revisadas", title_x=0.37
    )

    return fig


def create_df_produtividade_geral(df_tp, df_tasks):
    """
    Generates a productivity DataFrame by merging task data with productivity data.

    This function calculates adjusted productivity values by combining the existing productivity data
    with reviewed task data. The resulting DataFrame is transformed into a long format for visualization purposes.

    Parameters:
    df_tp (pd.DataFrame): DataFrame containing productivity data with columns related to task productivity.
    df_tasks (pd.DataFrame): DataFrame containing reviewed task data.

    Returns:
    pd.DataFrame: A melted DataFrame containing productivity values per month/year and task type.

    Complexity:
    Time: O(n), where n is the number of rows in df_tp.
    Space: O(n), since a new DataFrame is created.
    """
    df_tp["TP Adaptado (22 Dias Úteis) + Revisão Task"] = (
        df_tp["TP Adaptado (22 Dias Úteis)"] + df_tasks["TP Tasks Revisadas"]
    )
    df_tp["TP Ajustado (Dias Úteis Reais) + Revisão Task"] = (
        df_tp["TP Ajustado (Dias Úteis Reais)"] + df_tasks["TP Tasks Revisadas"]
    )

    df_produtividade_geral = df_tp.melt(
        id_vars=["Mês/Ano"],
        value_vars=[
            "TP Adaptado (22 Dias Úteis)",
            "TP Ajustado (Dias Úteis Reais)",
            "TP Ideal (22 Dias Úteis)",
            "TP Ideal Ajustado (Dias Úteis Reais)",
            "TP Adaptado (22 Dias Úteis) + Revisão Task",
            "TP Ajustado (Dias Úteis Reais) + Revisão Task",
        ],
        var_name="Tipo de TP",
        value_name="Valor",
    )
    return df_produtividade_geral


def create_fig_produtividade_geral(df_produtividade_geral, layout_config):
    """
    Generates a line chart for general productivity tasks.

    This function creates a Plotly line chart representing various types of productivity values
    over months/years, with different colors and markers for each type of TP (Task Productivity).

    Parameters:
    df_produtividade_geral (pd.DataFrame): DataFrame containing productivity data with columns 'Mês/Ano', 'Valor', and 'Tipo de TP'.
    layout_config (dict): Dictionary containing layout configurations for the chart.

    Returns:
    plotly.graph_objs._figure.Figure: A Plotly figure object representing the productivity trends.

    Complexity:
    Time: O(n), where n is the number of rows in df_produtividade_geral.
    Space: O(1), constant space aside from the figure object.
    """
    color_map = {
        "TP Adaptado (22 Dias Úteis)": "#2F4F4F",
        "TP Ajustado (Dias Úteis Reais)": "#8B0000",
        "TP Ideal (22 Dias Úteis)": "#000080",
        "TP Ideal Ajustado (Dias Úteis Reais)": "#00FF00",
        "TP Adaptado (22 Dias Úteis) + Revisão Task": "#C71585",
        "TP Ajustado (Dias Úteis Reais) + Revisão Task": "#FF4500",
    }

    fig = px.line(
        df_produtividade_geral,
        x="Mês/Ano",
        y="Valor",
        color="Tipo de TP",
        markers=True,
        title="Produtividade Geral Tasks",
        line_shape="spline",
        color_discrete_map=color_map,
    )
    fig.update_traces(line=dict(width=4))
    fig.update_layout(
        **layout_config, title_text="Produtividade Geral Tasks", title_x=0.33
    )

    return fig


def create_df_tamanho_task(df_tp):
    """
    Generates a DataFrame containing task size information for specific months.

    This function merges a base dataset with the provided df_tp DataFrame, ensuring that
    all months in df_tp are present and filling missing values with zero.

    Parameters:
    df_tp (pd.DataFrame): DataFrame containing months to be merged with the task size base data.

    Returns:
    pd.DataFrame: A DataFrame containing task size details per month/year.

    Complexity:
    Time: O(n), where n is the number of months.
    Space: O(n), for storing the task size data.
    """
    df_tamanho_task_base = pd.DataFrame(DATA_TAMANHO_TASK_BASE)

    df_tamanho_task_merged = pd.merge(
        df_tp[["Mês/Ano"]], df_tamanho_task_base, on="Mês/Ano", how="left"
    )
    df_tamanho_task_merged["Task P"] = df_tamanho_task_merged["Task P"].fillna(0)
    df_tamanho_task_merged["Task M"] = df_tamanho_task_merged["Task M"].fillna(0)
    df_tamanho_task_merged["Task G"] = df_tamanho_task_merged["Task G"].fillna(0)

    return df_tamanho_task_merged


def create_fig_tamanho_task(df_tamanho_task):
    """
    Generates a grouped bar chart representing task size productivity over months.

    This function creates a Plotly figure with bar charts for different task sizes (P, M, G),
    ensuring numerical consistency and proper layout configurations.

    Parameters:
    df_tamanho_task (pd.DataFrame): DataFrame containing task size data per month/year.

    Returns:
    plotly.graph_objs._figure.Figure: A Plotly figure object representing the task size distribution.

    Complexity:
    Time: O(n * k), where n is the number of months and k is the number of task types (P, M, G).
    Space: O(n), for storing the figure data.
    """
    bar_width = 0.20
    fig_tamanho_task = go.Figure()

    fig_tamanho_task.add_trace(
        go.Bar(
            x=df_tamanho_task["Mês/Ano"],
            y=df_tamanho_task["Task P"],
            name="Task P",
            marker_color="#FFD700",
            offsetgroup="group1",
            width=bar_width,
        )
    )
    fig_tamanho_task.add_trace(
        go.Bar(
            x=df_tamanho_task["Mês/Ano"],
            y=df_tamanho_task["Task M"],
            name="Task M",
            marker_color="#2F4F4F",
            offsetgroup="group2",
            width=bar_width,
        )
    )
    fig_tamanho_task.add_trace(
        go.Bar(
            x=df_tamanho_task["Mês/Ano"],
            y=df_tamanho_task["Task G"],
            name="Task G",
            marker_color="#8B0000",
            offsetgroup="group3",
            width=bar_width,
        )
    )

    for index, row in df_tamanho_task.iterrows():
        fig_tamanho_task.add_trace(
            go.Bar(
                x=[row["Mês/Ano"]],
                y=[row["Task P"]],
                name="TP Normal (P)",
                marker_color="#FFD700",
                offsetgroup="group4",
                base=0,
                width=bar_width,
                showlegend=False,
            )
        )
        fig_tamanho_task.add_trace(
            go.Bar(
                x=[row["Mês/Ano"]],
                y=[row["Task M"]],
                name="TP Normal (M)",
                marker_color="#2F4F4F",
                offsetgroup="group4",
                base=row["Task P"],
                width=bar_width,
                showlegend=False,
            )
        )
        fig_tamanho_task.add_trace(
            go.Bar(
                x=[row["Mês/Ano"]],
                y=[row["Task G"]],
                name="TP Normal (G)",
                marker_color="#8B0000",
                offsetgroup="group4",
                base=row["Task P"] + row["Task M"],
                width=bar_width,
                showlegend=False,
            )
        )

    for i in range(len(df_tamanho_task["Mês/Ano"]) - 1):
        midpoint = i + 0.5
        fig_tamanho_task.add_shape(
            type="line",
            x0=midpoint,
            x1=midpoint,
            y0=0,
            y1=max(
                df_tamanho_task["Task P"]
                + df_tamanho_task["Task M"]
                + df_tamanho_task["Task G"]
            ),
            line=dict(color="black", width=2, dash="dot"),
        )

    fig_tamanho_task.update_layout(
        barmode="group",
        title_text="Produtividade Tamanho da Task",
        xaxis_title="Mês/Ano",
        yaxis_title="Quantidade",
        legend_title_text="Tipo de Task",
        bargap=0.15,
        bargroupgap=0.1,
        xaxis=dict(
            title_font=dict(
                size=26, family="Arial, sans-serif", color="black", weight="bold"
            ),
            tickfont=dict(size=20, family="Arial, sans-serif", color="black"),
            tickmode="array",
            tickvals=list(range(len(df_tamanho_task["Mês/Ano"]))),
            ticktext=df_tamanho_task["Mês/Ano"],
        ),
        yaxis=dict(
            title_font=dict(
                size=26, family="Arial, sans-serif", color="black", weight="bold"
            ),
            tickfont=dict(size=20, family="Arial, sans-serif", color="black"),
        ),
        title=dict(
            x=0.44,
            xanchor="center",
            font=dict(
                size=34, family="Arial, sans-serif", color="black", weight="bold"
            ),
        ),
        legend=dict(
            font=dict(size=20, family="Arial, sans-serif", color="black", weight="bold")
        ),
    )

    return fig_tamanho_task


def create_fig_all(fig_tp, fig_tasks, fig_produtividade_geral, fig_tamanho_task):
    """
    Combines multiple productivity charts into a single subplot layout.

    This function creates a 2x2 subplot figure combining task productivity charts
    and manages legend visibility to avoid repetition.

    Parameters:
    fig_tp (plotly.graph_objs.Figure): Figure for task productivity.
    fig_tasks (plotly.graph_objs.Figure): Figure for reviewed tasks.
    fig_produtividade_geral (plotly.graph_objs.Figure): Figure for general productivity.
    fig_tamanho_task (plotly.graph_objs.Figure): Figure for task sizes.

    Returns:
    plotly.graph_objs._figure.Figure: A combined figure with all productivity charts.

    Complexity:
    Time: O(n), where n is the number of traces in the figures.
    Space: O(1), constant space for storing the figure references.
    """
    subplot_titles = [
        "Produtividade Tasks",
        "Produtividade Tasks Revisadas",
        "Produtividade Geral Tasks",
        "Produtividade Tamanho da Task",
    ]

    fig_all = sp.make_subplots(
        rows=2,
        cols=2,
        subplot_titles=subplot_titles,
        shared_xaxes=False,
        shared_yaxes=False,
        vertical_spacing=0.1,
        horizontal_spacing=0.1,
    )

    figures = [
        (fig_tp, 1, 1),
        (fig_tasks, 1, 2),
        (fig_produtividade_geral, 2, 1),
        (fig_tamanho_task, 2, 2),
    ]

    for fig, row, col in figures:
        fig_all.add_traces(fig.data, rows=row, cols=col)

    unique_traces = set()
    for trace in fig_all.data:
        trace.showlegend = (
            trace.name not in unique_traces and "TP Normal" not in trace.name
        )
        unique_traces.add(trace.name)

    fig_all.update_layout(
        height=1000,
        width=1500,
        title="Produtividade: Pedro Henrique Casarotto Rigon",
        showlegend=True,
    )
    return fig_all


def add_or_update_month_df_tp(
    df_tp, df_tasks, work_days_dict, month_year, tp_adaptado_22, tp_ideal_22, dias_uteis
):
    """
    Adds or updates a month entry in the df_tp DataFrame.

    This function updates productivity values for a given month, including adjustments
    based on working days and reviewed tasks.

    Parameters:
    df_tp (pd.DataFrame): DataFrame containing productivity data per month/year.
    df_tasks (pd.DataFrame): DataFrame containing reviewed tasks data.
    work_days_dict (dict): Dictionary storing working days for each month.
    month_year (str): The month/year identifier in the format 'MM/YY'.
    tp_adaptado_22 (int): Adapted TP for 22 business days.
    tp_ideal_22 (int): Ideal TP for 22 business days.
    dias_uteis (int): Actual number of business days for the given month.

    Returns:
    pd.DataFrame: Updated df_tp DataFrame with new or modified month data.

    Complexity:
    Time: O(n), where n is the number of rows in df_tp.
    Space: O(1), modifying the existing DataFrame.
    """
    work_days_dict[month_year] = dias_uteis

    if month_year in df_tp["Mês/Ano"].values:
        idx = df_tp.index[df_tp["Mês/Ano"] == month_year][0]
        df_tp.at[idx, "TP Adaptado (22 Dias Úteis)"] = tp_adaptado_22
        df_tp.at[idx, "TP Ideal (22 Dias Úteis)"] = tp_ideal_22
    else:
        task_row = df_tasks.loc[
            df_tasks["Mês/Ano"] == month_year, "TP Tasks Revisadas"
        ].sum()
        new_data = {
            "Mês/Ano": month_year,
            "TP Adaptado (22 Dias Úteis)": tp_adaptado_22,
            "TP Ideal (22 Dias Úteis)": tp_ideal_22,
            "Dias Úteis": dias_uteis,
            "TP Ajustado (Dias Úteis Reais)": tp_adaptado_22 * (22 / dias_uteis),
            "TP Ideal Ajustado (Dias Úteis Reais)": tp_ideal_22 * (dias_uteis / 22),
            "TP Adaptado (22 Dias Úteis) + Revisão Task": tp_adaptado_22 + task_row,
            "TP Ajustado (Dias Úteis Reais) + Revisão Task": (
                tp_adaptado_22 * (22 / dias_uteis)
            )
            + task_row,
        }
        df_tp = pd.concat([df_tp, pd.DataFrame([new_data])], ignore_index=True)

    df_tp["Dias Úteis"] = df_tp["Mês/Ano"].map(work_days_dict)
    df_tp["TP Ajustado (Dias Úteis Reais)"] = df_tp["TP Adaptado (22 Dias Úteis)"] * (
        22 / df_tp["Dias Úteis"]
    )
    df_tp["TP Ideal Ajustado (Dias Úteis Reais)"] = df_tp[
        "TP Ideal (22 Dias Úteis)"
    ] * (df_tp["Dias Úteis"] / 22)
    df_tp["TP Adaptado (22 Dias Úteis) + Revisão Task"] = (
        df_tp["TP Adaptado (22 Dias Úteis)"] + df_tasks["TP Tasks Revisadas"]
    )
    df_tp["TP Ajustado (Dias Úteis Reais) + Revisão Task"] = (
        df_tp["TP Ajustado (Dias Úteis Reais)"] + df_tasks["TP Tasks Revisadas"]
    )
    return df_tp


def add_or_update_month_df_tasks(
    df_tasks, month_year, tp_tasks_revisadas, tp_adaptado_tasks_revisadas
):
    """
    Adds or updates a month's data in the df_tasks DataFrame.

    This function updates productivity values for a given month or adds a new row if the month does not exist.

    Parameters:
    df_tasks (pd.DataFrame): DataFrame containing task review data per month/year.
    month_year (str): The month/year identifier in the format 'MM/YY'.
    tp_tasks_revisadas (int): Number of reviewed tasks.
    tp_adaptado_tasks_revisadas (int): Number of adjusted reviewed tasks.

    Returns:
    pd.DataFrame: Updated df_tasks DataFrame with new or modified month data.

    Complexity:
    Time: O(n), where n is the number of rows in df_tasks.
    Space: O(1), modifying the existing DataFrame.
    """
    if month_year in df_tasks["Mês/Ano"].values:
        idx = df_tasks.index[df_tasks["Mês/Ano"] == month_year][0]
        df_tasks.at[idx, "TP Tasks Revisadas"] = tp_tasks_revisadas
        df_tasks.at[idx, "TP Adaptado Tasks Revisadas"] = tp_adaptado_tasks_revisadas
    else:
        new_data = {
            "Mês/Ano": month_year,
            "TP Tasks Revisadas": tp_tasks_revisadas,
            "TP Adaptado Tasks Revisadas": tp_adaptado_tasks_revisadas,
        }
        df_tasks = pd.concat([df_tasks, pd.DataFrame([new_data])], ignore_index=True)
    return df_tasks


def add_or_update_month_df_tamanho_task(df_tamanho, month_year, task_p, task_m, task_g):
    """
    Adds or updates a month's data in the df_tamanho DataFrame.

    This function updates the task size values (P, M, G) for a given month/year.
    If the month does not exist, a new row is added.

    Parameters:
    df_tamanho (pd.DataFrame or None): DataFrame containing task size data per month/year.
    month_year (str): The month/year identifier in the format 'MM/YY'.
    task_p (int): Number of small tasks (P).
    task_m (int): Number of medium tasks (M).
    task_g (int): Number of large tasks (G).

    Returns:
    pd.DataFrame: Updated df_tamanho DataFrame with new or modified month data.

    Complexity:
    Time: O(n), where n is the number of rows in df_tamanho.
    Space: O(1), modifying the existing DataFrame.
    """
    if df_tamanho is None:
        df_tamanho = pd.DataFrame(columns=["Mês/Ano", "Task P", "Task M", "Task G"])

    if month_year in df_tamanho["Mês/Ano"].values:
        idx = df_tamanho.index[df_tamanho["Mês/Ano"] == month_year][0]
        df_tamanho.at[idx, "Task P"] = task_p
        df_tamanho.at[idx, "Task M"] = task_m
        df_tamanho.at[idx, "Task G"] = task_g
    else:
        new_row = {
            "Mês/Ano": month_year,
            "Task P": task_p,
            "Task M": task_m,
            "Task G": task_g,
        }
        df_tamanho = pd.concat([df_tamanho, pd.DataFrame([new_row])], ignore_index=True)

    return df_tamanho
