import datetime
import streamlit as st
from module_functions import create_df_tp
import os
import pickle

DEFAULT_WORK_DAYS = {
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


def save_to_binary(filename: str, data: object) -> None:
    """
    Saves data to a binary file in the 'bin' directory.

    Parameters:
    filename (str): The name of the file to save the data.
    data (object): The data to be saved.

    Returns:
    None

    Complexity:
    Time: O(n), where n is the size of the data.
    Space: O(1), constant space usage aside from the file storage.
    """
    os.makedirs("bin", exist_ok=True)
    filepath = os.path.join("bin", filename)
    with open(filepath, "wb") as file:
        pickle.dump(data, file)


def load_from_binary(filename: str, default_data: object) -> object:
    """
    Loads data from a binary file in the 'bin' directory, returning default data if the file does not exist or cannot be read.

    Parameters:
    filename (str): The name of the file to load the data from.
    default_data (object): The default data to return if loading fails.

    Returns:
    object: The loaded data or the default data.

    Complexity:
    Time: O(n), where n is the size of the data.
    Space: O(1), constant space usage aside from the loaded data.
    """
    filepath = os.path.join("bin", filename)
    if os.path.exists(filepath):
        with open(filepath, "rb") as file:
            try:
                data = pickle.load(file)
                return data if data is not None else default_data
            except (EOFError, pickle.UnpicklingError):
                return default_data
    return default_data


def parse_month_year(str_mm_yy: str) -> tuple[int, int]:
    """
    Converts a date string in 'MM/YY' format to a tuple of integers (year, month).

    Parameters:
    str_mm_yy (str): A string representing month and year in 'MM/YY' format.

    Returns:
    tuple[int, int]: A tuple containing the year (YYYY) and month (MM).

    Complexity:
    Time: O(1), constant time operations.
    Space: O(1), constant space usage.
    """
    mm, yy = str_mm_yy.split("/")
    return (2000 + int(yy), int(mm))


def format_month_year(year: int, month: int) -> str:
    """
    Converts a year and month tuple to a date string in 'MM/YY' format.

    Parameters:
    year (int): The year in YYYY format.
    month (int): The month as an integer (1-12).

    Returns:
    str: A string representing the month and year in 'MM/YY' format.

    Complexity:
    Time: O(1), constant time operations.
    Space: O(1), constant space usage.
    """
    return f"{month:02d}/{str(year)[-2:]}"


def next_month(str_mm_yy: str) -> str:
    """
    Given a date string in 'MM/YY' format, returns the next month in the same format.

    Parameters:
    str_mm_yy (str): A string representing month and year in 'MM/YY' format.

    Returns:
    str: The next month/year in 'MM/YY' format.

    Complexity:
    Time: O(1), constant time operations.
    Space: O(1), constant space usage.
    """
    year, month = parse_month_year(str_mm_yy)
    month += 1
    if month > 12:
        month = 1
        year += 1
    return format_month_year(year, month)


def last_month_in_df(df_tp):
    """
    Returns the most recent month/year present in df_tp, assuming it's sorted in ascending order.
    If empty, returns the current month/year in MM/YY format.

    Parameters:
    df_tp (DataFrame): A pandas DataFrame containing a column "Mês/Ano".

    Returns:
    str: The most recent month/year in MM/YY format.

    Complexity:
    Time: O(n log n) due to sorting.
    Space: O(n), storing unique values.
    """
    if df_tp.empty:
        return datetime.datetime.now().strftime("%m/%y")

    df_tp_sorted = sorted(df_tp["Mês/Ano"].unique(), key=lambda x: parse_month_year(x))
    return df_tp_sorted[-1]


def init_session_states() -> None:
    """
    Initialize session state variables in Streamlit with default values or load from binary files.

    Returns:
    None

    Complexity:
    Time: O(n), where n is the size of the data being loaded.
    Space: O(1), constant space usage aside from loaded data.
    """
    default_values = {
        "df_tp": lambda: load_from_binary("df_tp.pkl", create_df_tp()),
        "df_tasks": lambda: load_from_binary("df_tasks.pkl", None),
        "df_tamanho": lambda: load_from_binary("df_tamanho.pkl", None),
        "need_rerun": lambda: False,
        "work_days_dict": lambda: load_from_binary(
            "work_days_dict.pkl", DEFAULT_WORK_DAYS
        ),
    }

    for key, value_loader in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = value_loader()


def persist_data() -> None:
    """
    Save session state data to binary files in the 'bin' directory.

    Returns:
    None

    Complexity:
    Time: O(n), where n is the total size of all data being saved.
    Space: O(1), constant space usage aside from the file storage.
    """
    save_to_binary("df_tp.pkl", st.session_state.df_tp)
    save_to_binary("df_tasks.pkl", st.session_state.df_tasks)
    save_to_binary("df_tamanho.pkl", st.session_state.df_tamanho)
    save_to_binary("work_days_dict.pkl", st.session_state.work_days_dict)
