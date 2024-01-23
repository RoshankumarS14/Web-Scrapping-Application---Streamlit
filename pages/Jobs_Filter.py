import streamlit as st
import os
import pandas as pd

files_dict = {}
for filename in os.listdir("Dataset/"):
    if filename.endswith(".csv"):
        df = pd.read_csv(os.path.join("Dataset/", filename)).iloc[:,1:]
        files_dict[filename[:-4]] = df

selected_df = st.multiselect("Select the datasets to analyse:",["All"]+list(files_dict.keys()),default=["All"])

dfs = []

if selected_df==["All"]:
    for df in files_dict.keys():
        dfs.append(files_dict[df])
else:
    for df in selected_df:
        dfs.append(files_dict[df])

df = pd.concat(dfs,ignore_index=True)
df.index = list(range(1,len(df)+1))

# Search box
keyword = st.text_input('Enter a keyword to search for jobs')
location = st.multiselect("State:",["All"]+list(df["companyLocation"].unique()))
st.session_state["Search"] = st.button("Search!")

if st.session_state["Search"]:
    df.drop(df['jobTitle'].isnull().index,inplace=True)
    st.write(df['jobTitle'].isnull().sum())
    if not location or "All" in location:
        filtered_df = df[df['jobTitle'].str.contains(keyword, case=False)]
    else:
        # Filter DataFrame based on jobTitle and companyLocation
        filtered_df = df[(df['jobTitle'].str.contains(keyword, case=False)) & (df['companyLocation'].isin(location))]
        
    df_html = filtered_df[["jobTitle","companyLocation","Salary"]].to_html(classes='table table-striped',index=False)
    df_html = df_html.replace('<table ','<table style="text-align:right; margin-bottom:40px; margin-top:50px; width:95%;" ')
    st.markdown(df_html,unsafe_allow_html=True)
