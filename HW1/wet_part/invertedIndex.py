import os
import re
import time
from collections import defaultdict

class InvertedIndex:
    """
    Constructs an inverted index from the AP collection.
    """
    def __init__(self):
        """Initializes the data structures required for the index."""
        self.index = defaultdict(list)
        self.docid_map = {}
        self.doc_freq = defaultdict(int)
        self.doc_count = 0

    def create_index(self, data_directory):
        """
        Builds the inverted index by parsing all document files.
        """
        print("Starting index construction from unzipped directories...")
        start_time = time.time()

        for root, dirs, files in os.walk(data_directory):
            for name in sorted(files):
                file_path = os.path.join(root, name)

                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Split the file's content by the <DOC> tag to get individual documents.
                # The first item in the split will be empty, so we slice it off with [1:].
                doc_contents = content.split('<DOC>')[1:]
                
                for doc_text in doc_contents:
                    if not doc_text.strip():
                        continue

                    docno_match = re.search(r'<DOCNO>(.*?)</DOCNO>', doc_text, re.DOTALL)
                    if not docno_match:
                        continue
                    
                    internal_id = self.doc_count
                    self.docid_map[internal_id] = docno_match.group(1).strip()
                    
                    text_matches = re.findall(r'<TEXT>(.*?)</TEXT>', doc_text, re.DOTALL)
                    tokens = ' '.join(text_matches).split()
                    
                    for term in set(tokens):
                        self.index[term].append(internal_id)
                        self.doc_freq[term] += 1
                    
                    self.doc_count += 1
        
        # We added time to see whos computer is faster, might be fun for you!
        duration = time.time() - start_time
        print(f"Index construction complete.")
        print(f"  - Processed {self.doc_count} documents in {duration:.2f} seconds.") 
        print(f"  - Vocabulary size: {len(self.index)} terms.")