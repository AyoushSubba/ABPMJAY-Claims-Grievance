import pymupdf # cat /etc/os-release
import json


PDF_FILE = "data/Grievance_Redressal_Guidelines.pdf"

SOURCE = "National Health Authority"
DOCUMENT = "AB-PMJAY Grievance Redressal Guidelines"
VERSION = "December 2021"

MAX_CHUNK=700
def clean_text(text):
    lines=text.splitlines()
    cleaned_lines=[]##list of cleaned lines...

    for line in lines:
        line=line.strip()
        if not line:
            continue
        if line.isdigit():
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

def create_chunks(text,page_number):
    if not text.strip():
        return []
    lines = text.splitlines()

    chunks=[]
    current_chunk=""
    for line in lines:
        line=line.strip()
        if not line:
            continue
        if len(line)+len(current_chunk)<=MAX_CHUNK:
            if current_chunk:
                current_chunk+=line + "\n"
            else:
                current_chunk=line
        else:
            if current_chunk:
                chunks.append({
                    "text":current_chunk.strip(),
                    "metadata":{
                        "source":SOURCE,
                        "document":DOCUMENT,
                        "version":VERSION,
                        "page":page_number
                    }
                })
            current_chunk=line
    
    if current_chunk:#if there is the string in the current_chunk then it is treated as true!!
        chunks.append({
            "text":current_chunk.strip(),
            "metadata":{
                "source":SOURCE,
                "document":DOCUMENT,
                "version":VERSION,
                "page":page_number
            }
        })
    
    return chunks

document=pymupdf.open(PDF_FILE)

all_chunks=[]
for page_number, page in enumerate(document,start=1):
    page_text=page.get_text()
    cleaned_text=clean_text(page_text)
    page_chunks=create_chunks(cleaned_text,page_number)
    all_chunks.extend(page_chunks)

print("Total Chunks: ",len(all_chunks))

with open("data/chunks.json","w",encoding="utf-8")as file:
    json.dump(all_chunks,file,ensure_ascii=False,indent=2)
output_path = "data/Grievance_Redressal_Guidelines.txt"
all_text="\n\n".join(chunk["text"] for chunk in all_chunks)

with open(output_path,"w",encoding="utf-8")as file:
    file.write(all_text)
    print("All chunks is written in the txt also:\n")


print("\nChunks saved to data/chunks.json")

for i, chunk in enumerate(all_chunks[:5], start=1):
    print("\n--- CHUNK", i, "---")
    print("Page:", chunk["metadata"]["page"])
    print("Source:", chunk["metadata"]["source"])
    print("Document:", chunk["metadata"]["document"])
    print("Version:", chunk["metadata"]["version"])
    print("Text:")
    print(chunk["text"][:500])

