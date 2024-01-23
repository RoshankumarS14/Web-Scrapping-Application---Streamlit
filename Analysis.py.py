import streamlit as st
import pandas as pd
import os
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Job Analysis",
    page_icon="📈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

# Define your pages
PAGES = {
    "Analysis": "analysis.py",
    "Scrap Jobs": "web scrapper"
}

if "selected_page" not in st.session_state:
    st.session_state["selected_page"]=False

# # Create an option menu in the main section
# st.session_state["selected_page"] = option_menu("", list(PAGES.keys()),icons=["list-task"],
#     menu_icon="cast", default_index=0, orientation="horizontal")

# if st.session_state["selected_page"]:
#     if st.session_state["selected_page"] != "Analysis":
#         switch_page(PAGES[st.session_state["selected_page"]])
#     st.rerun()
        
files_dict = {}
for filename in os.listdir("Dataset/"):
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
    

    
