import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os
import difflib

class MedicineRAG:
    def __init__(self, index_path, mappings_path, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        
        self.index = faiss.read_index(index_path)
        
        with open(mappings_path, 'rb') as f:
            self.df = pickle.load(f)
            self.df = self.df.fillna('Information not available')
            
        self.all_brands = self.df['brand_name'].unique().tolist()
        self.all_generics = self.df['generic_name'].unique().tolist()
        
        symptoms = set()
        for ind in self.df['indications'].unique():
            parts = [p.strip() for p in ind.replace(' and ', ',').replace(';', ',').split(',')]
            symptoms.update(parts)
            
        self.search_pool = self.all_brands + self.all_generics + list(symptoms)
            
    def get_suggestions(self, query, n=3, cutoff=0.5):
        """
        Provides fuzzy suggestions for brands, generics, or symptoms.
        """
        query = query.lower()
        matches = difflib.get_close_matches(query, [s.lower() for s in self.search_pool], n=n, cutoff=cutoff)
        return [m.title() for m in matches]

    def query(self, user_query, k=3, threshold=1.2):
        """
        Retrieves medicines with a focus on relevance and accuracy.
        - Handles fuzzy brand/generic matching for typos.
        - Filters out irrelevant queries using distance thresholding.
        """
        query_words = user_query.lower().split()
        confident_match = False
        
        for word in query_words:
            matches = difflib.get_close_matches(word, [s.lower() for s in self.search_pool], n=1, cutoff=0.7)
            if matches:
                confident_match = True
                break
                
        query_embedding = self.model.encode([user_query])
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), k * 3)
        
        results = []
        seen_brands = set()

        for i, idx in enumerate(indices[0]):
            if idx != -1:
                dist = float(distances[0][i])
               
                if confident_match or dist < threshold:
                    medicine = self.df.iloc[idx].to_dict()
                    brand_key = f"{medicine['brand_name']}_{medicine['dosage']}".lower()

                    if brand_key not in seen_brands:
                        medicine['confidence_score'] = 1 - (dist / 2) # Normalized mock score
                        results.append(medicine)
                        seen_brands.add(brand_key)
                
                if len(results) >= k:
                    break
        
        
        if not results:
            return []
            
        return results

if __name__ == "__main__":
    index_file = os.path.join('data', 'medicine_index.faiss')
    mappings_file = os.path.join('data', 'medicine_mappings.pkl')
    
    if os.path.exists(index_file) and os.path.exists(mappings_file):
        rag = MedicineRAG(index_file, mappings_file)
        test_query = "headache and fever"
        results = rag.query(test_query)
        
        print(f"Results for query: {test_query}")
        for r in results:
            print(f"- Brand: {r['brand_name']}, Generic: {r['generic_name']}, Dosage: {r['dosage']}")
    else:
        print("Error: Vector DB files not found. Please run vector_db.py first.")
