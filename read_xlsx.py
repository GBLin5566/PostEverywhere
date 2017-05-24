
from openpyxl import load_workbook
import os

def get_file_names(data_dir_address, ends_with = ".xlsx"):
    files = []
    for f in os.listdir(data_dir_address):
        if f.endswith(ends_with):
            files.append(f)
    return files
def get_url_from_files(data_dir_address, finish_file = []):
    files = get_file_names(data_dir_address)
    urls = []
    all_files = []
    # Open xlsxs
    for f in files:
        if f in finish_file:
            continue
        print ("[*] Reading file ", f)
        try:
            wb = load_workbook(filename= data_dir_address + "/" + f, read_only=True)
            ws = wb['Timeline']
            f_urls = []
            for row in ws.rows:
                url = str(row[2].value)
                if url.startswith('http'):
                    f_urls.append(url)
            urls.append((f, f_urls))
            all_files.append(f)
        except BadZipfile:
            print (f , " failed")
            pass

    return all_files ,urls
