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
benefits = df[df["jobTitle"]==st.session_state["job"]]["Benefits (Metadata)"].values[0].replace('\n', '<br>')
st.markdown(benefits,unsafe_allow_html=True)

st.subheader("Description")
st.markdown(df[df["jobTitle"]==st.session_state["job"]]["Description (Metadata)"].values[0].replace('\n', '<br>'))
