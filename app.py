#pip install numpy==1.19.5
#pip install streamlit==0.74.1
#pip install pandas==1.2.0
#pip install openpyxl==3.0.6
#pip install plotly.express

import numpy as np
import streamlit as st
import pandas as pd
import openpyxl
#import plotly.express as px

def check_dup(df, cols = ['Location', 'Date']):
	if df.duplicated(subset = cols).any(): st.warning('WARNING: There are duplicated records!')
def check_missing_worker(df):
	if df[(df['Tips'] > 0) & (df['Worker'].isna())].shape[0] > 0: st.warning('WARNING: There are records with missing workers!')
def show_assumptions(value):
	if value == 'Tips': st.warning('NOTE: Assume tips are divided equally among workers in the same date and store')
	elif value == 'Hours': st.warning('NOTE: This is cumulative hours for all workers.')
st.set_page_config(page_title = 'Tuktuk App')
st.title('Resource Summarizer')
st.subheader('Feed me with your excel file')

uploaded_file = st.file_uploader('Choose an XLSX file', type = 'xlsx')

if uploaded_file:
	st.markdown('---')

	df = pd.read_excel(uploaded_file) #engine = 'openpyxl'
	df['Date'] = df['Date'].astype(str)
	df = df[~df['Location'].isna()]
	check_dup(df)

	df['Worker'] = df['Worker'].str.split(', ')
	df['numWorker'] = df['Worker'].str.len()
	df = df.explode('Worker').reset_index(drop = True)
	df['numWorker'] = df['numWorker'].fillna(value = 1)
	df['Tips'] = df['Tips'] / df['numWorker']
	df.drop('numWorker', axis = 1, inplace = True)
	check_missing_worker(df)
	
	#st.dataframe(df)
	groupby_col = st.selectbox(
		'Group by',
		('Worker', 'Location', 'Date')
	)
	output_col = st.selectbox(
		'Output',
		('Tips', 'Hours')
	)
	
	show_assumptions(output_col)
	df_grouped = df.groupby([groupby_col], as_index = False)[output_col].sum()
	st.dataframe(df_grouped)
