from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.text_splitter import CharacterTextSplitter
import pandas as pd


# https://drive.google.com/file/d/18_eYfx3cFSnQ7W21n_3A0lEClnzhHmK0/view?usp=sharing? dataset_name=(Consultancy agreement)
#id=18_eYfx3cFSnQ7W21n_3A0lEClnzhHmK0
file_id = "18_eYfx3cFSnQ7W21n_3A0lEClnzhHmK0"  #enter your own API
file_name = "legaldoc.txt"
!gdown --id $file_id --output $file_name
# Check if the file is struc. tured or unstructured
with open(file_name, 'r') as file:
    sample = file.read(500)  # Read the first 500 characters as a sample
print("Sample of the file content:")
print(sample)


loader = TextLoader("legaldoc.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
print("Number of chunks:",len(texts))

embeddings = HuggingFaceEmbeddings()
docsearch = Chroma.from_documents(texts, embeddings)
print('Successfully!! document ingested')

#Importing LLM Gemini
import google.generativeai as genai
# Configure and initialize GenAI
api_key = "AIzaSyBQiT1bfsMLONlsyYygJYq7-gBA6HMkPQA" #enter your own gemini api_key (which is free)
genai.configure(api_key=api_key)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

def query_legal_doc(user_query):
    chat_session = model.start_chat()
    full_text = "\n".join([doc.page_content for doc in texts])
    response = chat_session.send_message("Based on the legal document"+full_text+ "answer the following question:"+user_query)
    print("Response:")
    print(response.text)

def summarize_legal_doc():
    full_text = "\n".join([doc.page_content for doc in texts])
    response = model.start_chat().send_message(f"Summarize the following legal document:\n{full_text}")
    print("Summary:")
    print(response.text)

if __name__ == "__main__":
    summarize_legal_doc()
    user_query = input("Ask a question about the legal document: ")
    query_legal_doc(user_query)

#Load and Preprocessing
import os
import re
import json
from transformers import pipeline
def load_and_preprocess(file_path):
  if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")
  with open(file_path, 'r', encoding='utf-8') as file:
      document = file.read()
  chunks = [document[i:i+1000] for i in range(0, len(document), 1000)]
  return chunks

#Risk Detection
def risk_detection(chunks):
    model_name = "google/flan-t5-base"
    nlp = pipeline("text2text-generation", model=model_name)
    results=[]
    for chunk in chunks:
        prompt = ("Analyze the following text for potential risks, hidden obligations,"
               "or dependencies, and provide recommendations:\n\n"+ chunk
               )
        result= nlp(prompt, max_length=200, do_sample=False)
        prompt = ("Analyze the following text for potential risks, hidden obligations,"
               "or dependencies, and provide risk detection :\n\n"+ chunk
               )
        result1= nlp(prompt, max_length=200, do_sample=False)
        results.append({"context": chunk, "recommendations": result[0]['generated_text'],"risk detection": result1[0]['generated_text']})
    return results

#Function Execution
def main(file_path):
    print("Loading and preprocessing document...")
    chunks = load_and_preprocess(file_path)
    print("Detecting risks and generating recommendations...")
    analysis = risk_detection(chunks)
    # Save results to a JSON file
    output_path = "risk_analysis.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=4)
    print(f"Analysis complete. Results saved to {output_path}")
# Execute the pipeline
if __name__ == "__main__":
    file_path = "legaldoc.txt"
    main(file_path)

import json
import openpyxl
import pandas as pd # import pandas library and alias it as 'pd'

output_file = "output.xlsx"
with open("risk_analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data) # Use pd to access the pandas library
df.to_excel(output_file, index=False, engine='openpyxl')
print(f"Excel file created successfully at {output_file}")
for entry in data:
    print("Context:\n", entry["context"])
    print("Recommendation:\n", entry["recommendations"])
    print("Risk Detection:\n", entry["risk detection"])
    print("-" * 80)