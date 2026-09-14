import pymupdf

pdf_path = "data/Grievance_Redressal_Guidelines.pdf"
output_path = "data/Grievance_Redressal_Guidelines.txt"

document=pymupdf.open(pdf_path)
print("Number of pages:", len(document))


with open(output_path,'w',encoding="utf-8") as file:
    for page in document:
        text=page.get_text()
        file.write(text)
        file.write("\n\n")
        print(page)

document.close()
print("Pdf text extracted successfully!!")