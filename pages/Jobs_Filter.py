import streamlit as st

# List of jobs
jobs = ['Software Engineer', 'Data Scientist', 'Product Manager', 'UX Designer', 'Systems Analyst', 'Web Developer']

# Search box
keyword = st.text_input('Enter a keyword to search for jobs')

df_html = state_wise_pop.to_html(classes='table table-striped',index=False)
df_html = df_html.replace('<table ','<table style="text-align:right; margin-bottom:40px; margin-top:50px; width:95%;" ')

# Filter jobs
filtered_jobs = [job for job in jobs if keyword.lower() in job.lower()]

# Display jobs
for job in filtered_jobs:
    st.write(job)
