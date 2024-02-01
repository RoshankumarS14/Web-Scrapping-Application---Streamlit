import streamlit as st
import pandas as pd

df = pd.read_csv("Sample data (Craigslist).csv")

if "job" not in st.session_state:
    st.session_state["job"] = ""

st.session_state["job"] = st.selectbox("Select the Job Title:",df["Title"])

st.subheader("Job Title")
st.write(st.session_state["job"])

st.subheader("Company")
st.write(df[df["Title"]==st.session_state["job"]]["Company"].values[0])

st.subheader("Location")
st.write(df[df["Title"]==st.session_state["job"]]["Location"].values[0])

st.subheader("Salary")
st.write(df[df["Title"]==st.session_state["job"]]["Price"].values[0])

st.subheader("Posted Date")
st.write(df[df["Title"]==st.session_state["job"]]["date"].values[0])

st.subheader("Description")
description = df[df["Title"]==st.session_state["job"]]["Meta Data"].values[0].replace('\n', '<br>').replace("$","")
st.markdown(description,unsafe_allow_html=True)
