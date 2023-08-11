import streamlit as st
import requests
from datetime import datetime, timedelta
import os  # 추가된 import

# Streamlit configuration
st.set_page_config(page_title="Data Downloader", layout="wide")

def download_data(start_datetime, end_datetime, save_path):
    base_url = "http://opendata.kwater.or.kr/pubdata/kppm/kppm1Hr.do"
    date_format = "%Y%m%d%H"
    time_interval = timedelta(hours=3)
    
    start_dt = datetime.strptime(start_datetime, date_format)
    end_dt = datetime.strptime(end_datetime, date_format)

    current_dt = start_dt
    while current_dt <= end_dt:
        formatted_dt = current_dt.strftime(date_format)
        file_url = f"{base_url}?searchTm={formatted_dt}"
        filename = f"RN_KPPM01_NetCDF_{formatted_dt}.NC"
        
        response = requests.get(file_url)
        if response.status_code == 200:
            file_path = os.path.join(save_path, filename)  # 로컬 저장 경로 추가
            with open(file_path, "wb") as file:
                file.write(response.content)
            st.write(f"Downloaded: {filename}")
        else:
            st.write(f"Failed to download: {filename}")

        current_dt += time_interval

def main():
    st.title("Data Downloader")
    
    start_date = st.date_input("Start Date")
    start_time = st.time_input("Start Time")

    end_date = st.date_input("End Date")
    end_time = st.time_input("End Time")
    
    save_path = st.text_input("Save Path", value=os.getcwd())  # 로컬 저장 경로 입력란
    
    start_datetime = f"{start_date.strftime('%Y%m%d')}{start_time.strftime('%H')}"
    end_datetime = f"{end_date.strftime('%Y%m%d')}{end_time.strftime('%H')}"
    
    if st.button("Download Data"):
        download_data(start_datetime, end_datetime, save_path)
        st.success("Download completed!")

if __name__ == "__main__":
    main()
