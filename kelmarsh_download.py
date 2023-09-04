import requests
import os
import hashlib

from pathlib import Path
from zipfile import ZipFile
import pandas as pd


def download_file(url,outfile):
    # download a file from the web based on its url
    
    get_response = requests.get(url,stream=True)
    
    chunk_number = 0
    with open(outfile, 'wb') as f:
        
        for chunk in get_response.iter_content(chunk_size=1024*1024):
            
            chunk_number = chunk_number + 1
            
            print(str(chunk_number) + ' MB downloaded', end='\r')
            
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)  


def download_zenodo_data(record_id,outfile_path):
    # download data from zenodo based on the zenodo record_id
    #
    # outputs:
    # 1. record_details.json, which details the zenodo api details
    # 2. all files available for the record_id
    
    
    url_zenodo = r'https://zenodo.org/api/records/'

    record_id = str(record_id)
    
    r = requests.get(url_zenodo + record_id)
    
    r_json = r.json()
    
    
    print('======')
    print('Title: ' + r_json['metadata']['title'])
    print('Version: ' + r_json['metadata']['version'])
    print('URL: ' + r_json['links']['latest_html'])
    print('Record DOI: ' + r_json['doi'])
    print('License: ' + r_json['metadata']['license']['id'])
    print('======\n')
    
       
    # create outfile_path if it does not exist
    if not os.path.exists(outfile_path):
        os.makedirs(outfile_path)
    
    
    # save record details to json file
    outfile = outfile_path + 'record_details.json'
    
    with open(outfile, 'wb') as f:
        f.write(r.content)

        
    # download all files
    files = r_json['files']
    for f in files:
        
        url_file = f['links']['self']
        
        file_name = f['key']
                
        outfile = outfile_path + file_name
        
        
        # check if file exists
        if os.path.exists(outfile):
            
            
            # if it does check the checksum is correct
            with open(outfile, 'rb') as f_check:
                file_hash = hashlib.md5()
                while chunk := f_check.read(8192):
                    file_hash.update(chunk)
        
            if f['checksum'][4:]==file_hash.hexdigest():
                print('File already exists: ' + file_name)
            
            
            # download if the checksum isn't correct
            else:
                
                print('Downloading: ' + file_name)
                print('File size: ' + str(round(f['size']/(1024*1024),2)) + 'MB')       

                download_file(url_file,outfile)

                print('Saved to: ' + outfile + '\n')
        
        
        # download if the file doesn't exist
        else:
            
            print('\nDownloading: ' + file_name)
            print('File size: ' + str(round(f['size']/(1024*1024),2)) + 'MB')       

            download_file(url_file,outfile)

            print('Saved to: ' + outfile + '\n')

def download_asset_data(asset="kelmarsh",outfile_path="data/kelmarsh/"):
    # simplify downloading of know open data assets from zenodo
    
    if asset.lower() == "kelmarsh":
        record_id = 7212475
    elif asset.lower() == "penmanshiel":
        record_id = 5946808
    else:
        raise NameError("Zenodo record id undefined for: " + asset)
        
    download_zenodo_data(record_id,outfile_path)


def extract_all_data(path="data/kelmarsh/"):
    """
    Get all zip files in path and extract them
    """
    print("Extracting compressed data files")
    
    zipFiles = Path(path).rglob('*.zip')
    
    for file in zipFiles:
        with ZipFile(file) as zipfile:
            zipfile.extractall(path)