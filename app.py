import streamlit as st 
import pandas as pd 
from ydata_profiling  import ProfileReport 
from streamlit_pandas_profiling import st_profile_report 
import sys 
import os 

st.set_page_config(page_title='Data Profiler', layout='wide')

def get_filesize(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes / (1024**2)
    return size_mb

# sidebar 
with st.sidebar:
    uploaded_file = st.file_uploader("Uploaded .csv, .xlsx files not exceeding 10 MB"
                            , type=['.csv', 'xlsx'])
    
    if uploaded_file is not None:
        st.write('Mode of Operation')
        minimal = st.checkbox('Do you want minimal report?')
        display_mode = st.radio('Display mode:',
                        options=('Primary', 'Dark', 'Orange'))
        if display_mode == 'Dark':
            dark_mode = True 
            orange_mode = False 
        elif display_mode == 'Orange':
            dark_mode = False 
            orange_mode = True
        else:
            dark_mode = False 
            orange_mode = False 
    
if uploaded_file is not None:
    filesize = get_filesize(uploaded_file)
    if filesize <= 10:
        # Get the file extension
        ext = uploaded_file.name.split('.')[-1]
        if ext == '.csv':
            # time being led load csv 
            df = pd.read_csv(uploaded_file)
        else: 
            xl_file = pd.ExcelFile(uploaded_file)
            sheet_tuple = tuple(xl_file.sheet_names)
            sheet_name = st.sidebar.selectbox('Select the sheet', sheet_tuple)
            df = xl_file.parse(sheet_name)
            
        # generate report 
        with st.spinner('Generating Report'):
            pr = ProfileReport(df, minimal=minimal, 
                            dark_mode=dark_mode,
                            orange_mode=orange_mode
                            )
            
        st_profile_report(pr)
    else:
        st.error('Maximum allowed filesize is 10 MB. But received {filesize} MB')
else:
    st.title('Data Profiler')
    st.info('Upload your data in the left sidebar to generate profiling')