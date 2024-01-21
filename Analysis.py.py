import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Job Analysis",
    page_icon="📈🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

files_dict = {}
for filename in os.listdir("dataset/"):
    if filename.endswith(".csv"):
        df = pd.read_csv(os.path.join("Dataset/", filename)).iloc[:,1:]
        files_dict[filename[:-4]] = df

selected_df = st.multiselect("Select the datasets to analyse:",files_dict.keys())

dfs = []

for df in selected_df:
    dfs.append(files_dict[df])

if "analyze" not in st.session_state:
    st.session_state["analyze"]=False

if len(dfs)!=0:
    df = pd.concat(dfs,ignore_index=True)
    df.index = list(range(1,len(df)+1))
    st.dataframe(df)
    st.session_state["analyze"] = st.button("Analyze Job Titles!")

if st.session_state["analyze"]:
    st.subheader("Words Frequency")
    words = []
    for index in df.index:
        words.append(df.loc[index,"jobTitle"].split())
    words = [i for j in words for i in j]
    words = [i.lower() for i in words]
    st.dataframe(pd.DataFrame(pd.Series(words).value_counts()).rename(columns={0:"Count"}))
    

    
