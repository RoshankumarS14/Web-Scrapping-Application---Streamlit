import streamlit as st
import requests
import json
from stqdm import stqdm
import pandas as pd

st.set_page_config(
    page_title="Web Scrapping",
    page_icon="📈🌐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

url = "https://api.scrapingdog.com/indeed"
api_key = "65b27bd80ff088077baa70cb"

if "Scrape" not in st.session_state:
    st.session_state["Scrape"] = False

if "Save_Button" not in st.session_state:
    st.session_state["Save_Button"] = False

st.subheader("Click the button to scrape today's jobs from indeed")
st.session_state["Scrape"] = st.button("Scrape!")   

if st.session_state["Scrape"]:
    jobs_list = []
    for i in stqdm(range(1,54)):
        # job_search_url = f"https://www.indeed.com/jobs?q=CDL A Drivers&l=United States&start={i*10}&vjk=8bf2e735050604df"
        job_search_url = f"https://www.indeed.com/jobs?q=CDL+A+Drivers&l=United+States&sc=0kf%3Aattr%28VU74M%29%3B&radius=50&start={i*10}&vjk=b45f8bcb33974bc3"

        # Set up the parameters
        params = {"api_key": api_key, "url": job_search_url}
        # Make the HTTP GET request
        response = requests.get(url, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON content
            json_response = response.json()
            jobs_list.append(json_response)
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    jobs_data = pd.DataFrame([i for j in jobs_list for i in j])
    jobs_data.drop(["totalJobs","jobDescription"],axis=1,inplace=True)
    st.session_state["Save_Button"] = True

if st.session_state["Save_Button"]:
    st.dataframe(jobs_data)
    st.subheader("Do you want to save the data ?")
    st.download_button("Download Output! (PDF)",jobs_data.to_csv(index=False).encode('utf-8'),"Jobs List (21-01-2024).csv","text/csv")
