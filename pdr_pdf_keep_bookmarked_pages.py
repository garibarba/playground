"""
This file takes bookmarked pages from a folder with several PDFs from Kindle and outputs a single PDF file with all the bookmarked pages.
The Kindle bookmarks are expected in .pdr format with the same file name as the corresponding .pdf files.
"""
# %%
import io
from pathlib import Path
from struct import unpack
input_path_name = '/some/path/to/pdf_and_pdr/folder/'
output_file_name = "Your.Favourites.pdf"
root_path = Path(input_path)

bookmarks = {}
for file_path in root_path.glob("*.pdr"):
    data = Path(file_path).read_bytes()  # Python 3.5+
    i = 0
    i += 20
    bookmark_list = []
    while i < len(data):
        length = data[i:].find(0x00)
        if length > 0:
            bookmark_list.append(int(data[i:i+length].decode()))
        i += length + 7
    bookmarks[file_path.stem] = bookmark_list
# bookmarks
for k in sorted(bookmarks.keys()):
    print(f"{k}: {len(bookmarks[k])}")

# %%
from pikepdf import Pdf
    
output_pdf = Pdf.new()
for file_path_stem in sorted(bookmarks.keys()):
    file_path = root_path / (file_path_stem + ".pdf")
    with Pdf.open(file_path) as input_pdf:
        for i in bookmarks[file_path.stem]:
            output_pdf.pages.append(input_pdf.pages[i-1])
output_pdf.save(root_path / output_filename)
