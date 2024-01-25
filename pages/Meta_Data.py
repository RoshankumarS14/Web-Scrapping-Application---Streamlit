import streamlit as st
import pandas as pd

df = pd.read_csv("Sample (Meta Data).csv")

if "job" not in st.session_state:
    st.session_state["job"] = ""

st.session_state["job"] = st.selectbox("Select the Job Title:",df["jobTitle"])

st.subheader("Job Title")
st.write(st.session_state["job"])

st.subheader("Salary")
st.write(df[df["jobTitle"]==st.session_state["job"]]["Salary (Metadata)"].values[0])

st.subheader("Benefits")
st.write(df[df["jobTitle"]==st.session_state["job"]]["Benefits (Metadata)"].values[0])

st.subheader("Description")
st.write(df[df["jobTitle"]==st.session_state["job"]]["Description (Metadata)"].values[0])
