#app.py

import streamlit as st
from api.api import FirecrawlAPI
from utils.extractUrlsfromText import extract_urls,extract_domain
from utils.extractUrlsfromHtml import extract_urls_from_html,matches_search_criteria
import pandas as pd
import time


def batchscrape(api_key,urls,outformat,wait_time):
    try:
        # Initialize API with your production key
        app = FirecrawlAPI(api_key=api_key)
        config={}
        config['formats']=[outformat]
        config['waitFor']=wait_time
        #st.write(config)
        # Call batch_process method
        scraped_data = app.batch_process(urls, config)
        return scraped_data
    except Exception as e:
        st.error(f"An error occurred while processing URLs: {str(e)}")

def process_with_params(supported_urls,api_key,format_option,wait_time,Domain):
    if supported_urls:
        with st.spinner("Processing...."):
            scraped_data = batchscrape(api_key, supported_urls, format_option, wait_time)
            
            # Display metadata from scraped_data
            #st.subheader("Scraped Data Metadata:")
            metadata_keys = ['success', 'status', 'completed', 'total', 'creditsUsed', 'expiresAt']
            metadata = {key: scraped_data[key] for key in metadata_keys}
            #st.write(metadata)
            
            # Process raw HTML in the scraped data
            st.subheader("Processed URLs from Scraped Data:")
            processed_urls = {}
            for idx, item in enumerate(scraped_data['data']):
                raw_html = item['rawHtml']
                urls = extract_urls_from_html(raw_html,Domain)
                processed_urls[idx] = urls
                
        #st.write(processed_urls)
        return processed_urls ,metadata

def create_url_dataframe(finalUrls,search_list):
    data = []
    for idx, url_list in finalUrls.items():
        for url in url_list:
            if matches_search_criteria(url, search_list):
                data.append({'Index': idx, 'URL': url})
    df = pd.DataFrame(data)
    return df


st.set_page_config(
layout="wide"
)
st.markdown("<h2 style='margin-bottom:0.2rem'>🔍 Urls Extractor</h2>", unsafe_allow_html=True)
# Initialize session states
if "text_data" not in st.session_state:
    st.session_state.text_data = None 
if "results" not in st.session_state:
    st.session_state.results = None 
if "metadata" not in st.session_state:
    st.session_state.metadata = None
if "params_changed" not in st.session_state:
    st.session_state.params_changed = False 
if "results_df" not in st.session_state:
    st.session_state.results_df = None    
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'supported_urls' not in st.session_state:
    st.session_state.supported_urls = None
if 'unsupported_urls' not in st.session_state:
    st.session_state.unsupported_urls = None     

# Function to track parameter changes
def param_changed():
    st.session_state.params_changed = True
    
st.sidebar.header("Configurations")

# Sidebar inputs
Domain = st.sidebar.selectbox("Distributor:", options=["iewc","tme","masterElectronics"], index=0,on_change=param_changed)
format_option = st.sidebar.selectbox("Extraction Format:", options=["rawHtml"], index=0,on_change=param_changed)
wait_time = st.sidebar.slider("Wait Time (ms):", min_value=2000, max_value=25000, value=10000, step=500,on_change=param_changed)
st.sidebar.header("API Key Input")

# Default API Key
api_key = st.sidebar.text_input(
    "Enter your API Key:",
    type="password",  # This enables the visibility toggle (eye symbol)
    placeholder="Enter your API key here"
)
st.sidebar.header("Search")
user_input = st.sidebar.text_input(
    "Enter comma-separated items (e.g., gxl,gxt):",
    value="",  # Default empty string
    help="Enter items separated by commas, without spaces"
)

# Convert the input string to a list
if user_input:
    search_list = [item.strip() for item in user_input.split(',')]
else:
    search_list = []  # Empty list if no input


# File uploader widget
uploaded_file = st.file_uploader("Upload a text file containing batch of comma-separated URLs", type=["txt"])
if uploaded_file is not None and uploaded_file != st.session_state.uploaded_file:
    st.session_state.uploaded_file = uploaded_file
    file_content = uploaded_file.read().decode("utf-8")
    if file_content:
        st.session_state.text_data = file_content
        st.session_state.results = None 
        st.session_state.metadata = None
        st.session_state.results_df = None
        st.session_state.params_changed = False 
    try:
        # Extract URLs from the content
        supported_urls, unsupported_urls = extract_urls(st.session_state.text_data)
        st.session_state.supported_urls = supported_urls
        st.session_state.unsupported_urls = unsupported_urls
        #st.write(f"Total Valid URLs for domain:{Domain} in the uploaded (.txt) file is: {len(supported_urls)}")
    except Exception as e:
        st.error(f"An error occurred while processing URLs: {str(e)}")
    # Process button in sidebar

if st.session_state.supported_urls is not None:
    st.write(f"Total Valid URLs for domain:{Domain} in the uploaded (.txt) file is: {len(st.session_state.supported_urls)}")
    
if st.sidebar.button("Submit"):
    start_time = time.time()
    finalUrls,metadata=process_with_params(st.session_state.supported_urls, api_key, format_option, wait_time,Domain)
    st.session_state.results = finalUrls
    st.session_state.metadata = metadata
    end_time = time.time()
    st.session_state.processing_time = end_time - start_time
    st.session_state.params_changed = False
    
# Create DataFrame from results
if st.session_state.results is not None:
    st.session_state.results_df = create_url_dataframe(st.session_state.results,search_list)

# Results area 
if st.session_state.text_data is not None:
    with st.expander("📋 Results", expanded=True):
        if st.session_state.results is not None:
            st.success("✅ Processing completed successfully!")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(st.session_state.metadata)
            with col2:
                st.write(f"Total URLs extracted: {st.session_state.results_df.shape[0]}")    
            with col3:    
                st.write(f"Processing time: {st.session_state.processing_time:.2f} seconds")
            
            # Display the DataFrame
            if 'results_df' in st.session_state:
                st.subheader("Extracted URLs")
                st.dataframe(st.session_state.results_df)
            
if st.session_state.text_data is not None and st.session_state.results is None:
    st.info("👈 Click 'Submit'to scrape the Urls")
    
if st.session_state.text_data is not None and st.session_state.unsupported_urls:
    st.warning("The following URLs are not supported:")
    st.write(unsupported_urls)
# Show an indicator if parameters have changed since last processing
if st.session_state.params_changed and st.session_state.results is not None:
    st.sidebar.warning("⚠️ Parameters changed. Re-process to apply new settings.")        


