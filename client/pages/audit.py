import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))
import streamlit as st
import pandas as pd
from database import engine

with st.container():
    st.header("🔍 Audit Log")
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        table_filter = st.selectbox(
            "Table",
            ["Toutes", "operation", "flotteur", "human_result", "operation_stat"],
        )

    with col2:
        op_filter = st.selectbox("Opération", ["Toutes", "INSERT", "UPDATE", "DELETE"])

    with col3:
        limit = st.number_input("Lignes max", min_value=10, max_value=5000, value=200, step=50)

    where_clauses = []
    params: dict = {}

    if table_filter != "Toutes":
        where_clauses.append("table_name = %(table_name)s")
        params["table_name"] = table_filter

    if op_filter != "Toutes":
        where_clauses.append("operation = %(operation)s")
        params["operation"] = op_filter

    where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

    query = f"""
        SELECT id, table_name, operation, record_id, changed_data, created_at
        FROM audit_log
        {where_sql}
        ORDER BY created_at DESC
        LIMIT {int(limit)}
    """

    df = pd.read_sql_query(query, con=engine, params=params if params else None)

    st.markdown(f"**{len(df)} entrées** (les plus récentes en premier)")

    if df.empty:
        st.info("Aucune entrée d'audit trouvée.")
    else:
        def highlight_op(val):
            colours = {"INSERT": "#2D9B48", "UPDATE": "#8534b4", "DELETE": "#a83740"}
            bg = colours.get(val, "")
            return f"background-color: {bg}"

        st.dataframe(
            df.style.map(highlight_op, subset=["operation"]),
            use_container_width=True,
            height=600,
        )

        st.download_button(
            "⬇️ Télécharger CSV",
            data=df.to_csv(index=False).encode(),
            file_name="audit_log.csv",
            mime="text/csv",
        )
