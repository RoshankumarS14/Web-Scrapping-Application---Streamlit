import streamlit as st

# List of jobs
jobs = ['Software Engineer', 'Data Scientist', 'Product Manager', 'UX Designer', 'Systems Analyst', 'Web Developer']

# Search box
keyword = st.text_input('Enter a keyword to search for jobs')

# Filter jobs
filtered_jobs = [job for job in jobs if keyword.lower() in job.lower()]

# Display jobs
for job in filtered_jobs:
    st.write(job)
