import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Simple Data Dashboard")

uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

        st.subheader("🔍 Data Preview")
        st.write(df.head())

        st.subheader("📊 Data Summary")
        st.write(df.describe())

        st.subheader("🎯 Filter Data")
        column = df.columns.tolist()

        if column:
            selected_column = st.selectbox("Select Column", column)
            selected_value = st.selectbox("Select Value", df[selected_column].dropna().unique())

            if selected_value:
                filtered_data = df[df[selected_column] == selected_value]

                if not filtered_data.empty:
                    st.write(filtered_data)
                else:
                    st.warning("⚠ No data found for the selected value!")

                st.subheader("📈 Plot Data")
                numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()

                if numeric_columns:
                    x_column = st.selectbox("Select X-axis", numeric_columns, key="x_axis")
                    y_column = st.selectbox("Select Y-axis", numeric_columns, key="y_axis")
                    chart_type = st.radio("Select Chart Type", ["Line Chart", "Bar Chart", "Scatter Plot"])

                    if st.button("Generate Plot"):
                        fig, ax = plt.subplots(figsize=(8, 5))

                        if chart_type == "Line Chart":
                            ax.plot(filtered_data[x_column], filtered_data[y_column], marker='o', linestyle='-')
                        elif chart_type == "Bar Chart":
                            ax.bar(filtered_data[x_column], filtered_data[y_column])
                        elif chart_type == "Scatter Plot":
                            ax.scatter(filtered_data[x_column], filtered_data[y_column])

                        ax.set_xlabel(x_column)
                        ax.set_ylabel(y_column)
                        ax.set_title(f"{chart_type} of {x_column} vs {y_column}")

                        st.pyplot(fig)
                    else:
                        st.info("⏳ Waiting for user action...") 
                else:
                    st.warning("⚠ No numeric columns available for plotting!")

    except Exception as e:
        st.error(f"❌ Error loading file: {e}")
