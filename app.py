import streamlit as st
import requests
from datetime import datetime, timedelta
import os

# Streamlit configuration
st.set_page_config(page_title="Data Downloader", layout="wide")

def download_data(start_datetime, end_datetime):
    base_url = "http://opendata.kwater.or.kr/pubdata/kppm/kppm1Hr.do"
    date_format = "%Y%m%d%H"
    time_interval = timedelta(hours=3)
    
    start_dt = datetime.strptime(start_datetime, date_format)
    end_dt = datetime.strptime(end_datetime, date_format)

    files_to_download = []

    current_dt = start_dt
    while current_dt <= end_dt:
        formatted_dt = current_dt.strftime(date_format)
        file_url = f"{base_url}?searchTm={formatted_dt}"
        filename = f"RN_KPPM01_NetCDF_{formatted_dt}.NC"
        
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(filename, "wb") as file:
                file.write(response.content)
            files_to_download.append(filename)
            st.write(f"Downloaded: {filename}")
        else:
            st.write(f"Failed to download: {filename}")

        current_dt += time_interval

    return files_to_download

def main():
    st.title("Data Downloader")
    
    start_date = st.date_input("Start Date")
    start_time = st.time_input("Start Time")

    end_date = st.date_input("End Date")
    end_time = st.time_input("End Time")
    
    start_datetime = f"{start_date.strftime('%Y%m%d')}{start_time.strftime('%H')}"
    end_datetime = f"{end_date.strftime('%Y%m%d')}{end_time.strftime('%H')}"
    
    if st.button("Download Data"):
        downloaded_files = download_data(start_datetime, end_datetime)
        if downloaded_files:
            st.success("Download completed!")

            st.write("Downloaded Files:")
            for filename in downloaded_files:
                st.markdown(f"Download [**{filename}**](https://raw.githubusercontent.com/newcave/NetCDF2_download/data/{filename})")

if __name__ == "__main__":
    main()
