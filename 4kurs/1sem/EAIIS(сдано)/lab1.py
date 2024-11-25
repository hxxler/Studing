import os
import tkinter as tk
from tkinter import filedialog, messagebox
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import re

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ' '.join(tokens)

def extract_context(text, query, window=10):
    words = text.split()
    query_words = query.split()
    context_fragments = []
    
    for i in range(len(words)):
        if words[i:i + len(query_words)] == query_words:
            start = max(0, i - window)
            end = min(len(words), i + len(query_words) + window)
            context = ' '.join(words[start:end])
            context_fragments.append(context)
    
    return context_fragments


def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_var.set(folder_selected)

def search_documents():
    folder_path = folder_var.get()
    if not folder_path:
        messagebox.showwarning("Warning", "Please select a folder first!")
        return

    query = query_entry.get().strip()
    if not query:
        messagebox.showwarning("Warning", "Please enter a search query!")
        return

    documents = []
    filenames = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"): 
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                documents.append(file.read())
                filenames.append(filename)

    if not documents:
        messagebox.showinfo("Info", "No documents found in the selected folder.")
        return

    preprocessed_docs = [preprocess_text(doc) for doc in documents]
    
    vectorizer = TfidfVectorizer()
    doc_vectors = vectorizer.fit_transform(preprocessed_docs)


    preprocessed_query = preprocess_text(query)
    query_vector = vectorizer.transform([preprocessed_query])


    similarities = cosine_similarity(query_vector, doc_vectors).flatten()
    results = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)

 
    results_text.delete(1.0, tk.END)  
    results_text.insert(tk.END, f"Results for query: '{query}'\n\n")
    for idx, score in results:
        if score > 0:  
            original_text = documents[idx]
            context_fragments = extract_context(preprocess_text(original_text), preprocessed_query)

            results_text.insert(tk.END, f"Document: {filenames[idx]} (Similarity: {score:.2f})\n")
            if context_fragments:
                results_text.insert(tk.END, f"Context around '{query}':\n")
                for fragment in context_fragments:
                    results_text.insert(tk.END, f"... {fragment} ...\n")
            results_text.insert(tk.END, "\n")


root = tk.Tk()
root.title("Document Search")


folder_var = tk.StringVar()

folder_label = tk.Label(root, text="Select Folder with Documents:")
folder_label.pack(padx=10, pady=5)

folder_entry = tk.Entry(root, textvariable=folder_var, width=50)
folder_entry.pack(padx=10, pady=5)

folder_button = tk.Button(root, text="Browse", command=select_folder)
folder_button.pack(padx=10, pady=5)

query_label = tk.Label(root, text="Enter Search Query:")
query_label.pack(padx=10, pady=5)

query_entry = tk.Entry(root, width=50)
query_entry.pack(padx=10, pady=5)

search_button = tk.Button(root, text="Search", command=search_documents)
search_button.pack(padx=10, pady=10)

results_text = tk.Text(root, height=20, width=70)
results_text.pack(padx=10, pady=10)

root.mainloop()
