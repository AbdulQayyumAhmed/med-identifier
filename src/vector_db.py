import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import pickle

def create_vector_db(csv_path, index_path, mappings_path):
    df = pd.read_csv(csv_path)
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    texts = df['combined_text'].tolist()
    embeddings = model.encode(texts)
    
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype('float32'))
    
    faiss.write_index(index, index_path)
    
    with open(mappings_path, 'wb') as f:
        pickle.dump(df, f)
    
    print(f"Vector DB created and saved to {index_path}")
    return index, df

if __name__ == "__main__":
    csv_file = os.path.join('data', 'medicine_cleaned.csv')
    index_file = os.path.join('data', 'medicine_index.faiss')
    mappings_file = os.path.join('data', 'medicine_mappings.pkl')
    
    if os.path.exists(csv_file):
        create_vector_db(csv_file, index_file, mappings_file)
    else:
        print(f"Error: {csv_file} not found. Please run data_prep.py first.")
