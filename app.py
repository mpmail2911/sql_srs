# pylint: disable=missing-module-docstring
import io

import duckdb
import pandas as pd
import streamlit as st

st.write(
    """
# SQL SRS
Spaced Repetition System SQL practice
"""
)

CSV = """
beverage, price
orange juice, 2.5
expresso, 2
tea, 3
"""
beverages = pd.read_csv(io.StringIO(CSV))

CSV2 = """
food_item, food_price
cookie, 2.5
chocolatine, 2
muffin, 3
"""
food_items = pd.read_csv(io.StringIO(CSV2))

ANSWER_STR = """
SELECT * FROM beverages
CROSS JOIN food_items
"""

solution_df = duckdb.sql(ANSWER_STR).df()

with st.sidebar:
    option = st.selectbox(
        "What would you like to review?",
        ("Joins", "GroupBy", "WFunctions"),
        index=None,
        placeholder="Select a theme",
    )

st.header("enter your code:")
query = st.text_area(label="votre code SQL ici", key="user_input")


if query:
    result = duckdb.sql(query).df()
    st.dataframe(result)

# if len(result.columns) != len(
#    solution_df.columns
# ):
#    st.write("Some columns are missing")

try:
    result = result[solution_df.columns]
    st.dataframe(result.compare(solution_df))
except KeyError as e:
    st.write("Some columns are missing")

n_lines_difference = result.shape[0] - solution_df.shape[0]
if n_lines_difference != 0:
    st.write(f"result has a {n_lines_difference} lines difference with the solution")


tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("table: beverages")
    st.dataframe(beverages)
    st.write("table: food_items")
    st.dataframe(food_items)
    st.write("expected:")
    st.dataframe(solution_df)

with tab3:
    st.write(ANSWER_STR)
