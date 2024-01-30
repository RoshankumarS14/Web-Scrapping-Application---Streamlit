import streamlit as st
import pandas as pd
import numpy as np
import os
from streamlit_extras.switch_page_button import switch_page
import asana
import requests
from io import StringIO

st.set_page_config(
    page_title="Job Analysis",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

personal_access_token = '2/1206474259581486/1206474150741575:63af673ccea40cb54a89691b17afc264'
section_id = '1206473999726567'
client = asana.Client.access_token(personal_access_token)

if "selected_page" not in st.session_state:
    st.session_state["selected_page"]=False

if "range" not in st.session_state:
    st.session_state["range"] = (company_counts["count"].min(), company_counts["count"].max())
    
if "jobs_data" not in st.session_state:
    tasks = client.tasks.get_tasks_for_section(section_gid=section_id, opt_fields='name')
    jobs_data = {}  # Dictionary to store DataFrames

    for task in tasks:
        # Retrieve attachments for each task
        attachments = client.attachments.find_by_task(task['gid'], opt_fields='name')

        for attachment in attachments:
            # Check if the attachment is a CSV file
            if attachment['name'].endswith('.csv'):
                # Request the specific attachment by its gid to get the download URL
                attachment_details = client.attachments.get_attachment(attachment['gid'], opt_fields='download_url')
                download_url = attachment_details['download_url']

                # Download the CSV content
                response = requests.get(download_url)
                if response.status_code == 200:
                    # Read the content into a DataFrame
                    csv_string = StringIO(response.content.decode('utf-8'))
                    df = pd.read_csv(csv_string)
                    jobs_data[attachment['name'].replace(".csv","")] = df
    st.session_state["jobs_data"]=jobs_data

selected_df = st.multiselect("Select the datasets to analyse:",st.session_state["jobs_data"].keys())

dfs = []

for df in selected_df:
    dfs.append(st.session_state["jobs_data"][df])

if "analyze" not in st.session_state:
    st.session_state["analyze"]=False

if len(dfs)!=0:
    df = pd.concat(dfs,ignore_index=True)
    df.index = list(range(1,len(df)+1))
    st.dataframe(df[["jobTitle","companyName","companyLocation"]])
    st.session_state["analyze"] = st.button("Analyze Jobs!")

if st.session_state["analyze"]:
    c1,c2 = st.columns([1,1,])
    words = []
    for index in df.index:
        words.append(df.loc[index,"jobTitle"].split())
    words = [i for j in words for i in j]
    words = [i.lower() for i in words]
    with c1:
        st.subheader("Words Frequency")
        st.dataframe(pd.DataFrame(pd.Series(words).value_counts()).rename(columns={0:"Count"}))
        pass
    with c2:
        st.subheader("Companies")
        company_counts = pd.DataFrame(df["companyName"].value_counts())
        st.session_state["range"] = st.slider("Select range for count of companies",
                                              company_counts["count"].min(), company_counts["count"].max(),
                                              st.session_state["range"])
        filtered_companies = company_counts[(company_counts["count"] >= st.session_state["range"][0]) & 
                                            (company_counts["count"] <= st.session_state["range"][1])]
        st.dataframe(filtered_companies)
                                      
    

    
