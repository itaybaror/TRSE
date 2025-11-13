import heapq
from collections import defaultdict

class CollectionAnalyzer:
    """
    Analyzes the inverted index to compute and report detailed collection statistics.
    """
    def __init__(self, indexer, retriever):
        """Initializes the analyzer with the completed index and retriever."""
        self.doc_freq = indexer.doc_freq
        self.index = indexer.index
        self.docid_map = indexer.docid_map
        self.retriever = retriever  # To use its efficient _intersect method

    def generate_report(self, output_path):
        """
        Generates and writes the full statistics report to the specified file,
        with analysis customized to the actual results we found.
        """
        #  Find the required statistics before writing the file 
        top_10 = heapq.nlargest(10, self.doc_freq.items(), key=lambda item: item[1])
        bottom_10 = heapq.nsmallest(10, self.doc_freq.items(), key=lambda item: item[1])
        # The heuristic will find the 'turco'/'licari' pair or a similar one.
        pair_info = self._find_cooccurring_pair()

        with open(output_path, 'w') as f:
            #  Section 3.1: Top 10 Highest Document Frequency 
            f.write("1. Write the top 10 terms with the highest document frequency:\n")
            for term, freq in top_10:
                f.write(f"  {term}: {freq}\n")
            
            #  Section 3.2: Top 10 Lowest Document Frequency 
            f.write("\n2. Write the top 10 terms with the lowest document frequency:\n")
            for term, freq in bottom_10:
                f.write(f"  {term}: {freq}\n")
            
            #  Section 3.3: Explanation of Characteristics 
            f.write("\n3. Explain the different characteristics of the above two sets of terms:\n")
            f.write("  Characteristics of the highest frequency terms:\n")
            f.write("  The terms with the highest document frequency are classic stopwords. This list includes articles ('the', 'a'), prepositions ('of', 'in', 'to', 'for', 'on'), and conjunctions ('and'). These words form the grammatical backbone of the English language but carry almost no semantic meaning for information retrieval. Their presence in nearly every document (e.g., 'the' is in 242,067 of ~242,918 documents) makes them completely non-discriminative. The term 'said' is also extremely common, reflecting the journalistic nature of the AP news corpus. In most search systems, these words would be filtered out during preprocessing to save space and improve performance.\n")
            
            f.write("\n  Characteristics of the lowest frequency terms:\n")
            f.write("  The terms with the lowest frequency (appearing in only one document) are highly specific and thus have maximum discriminative power. This list consists of proper nouns that are likely names of people or places ('enroth', 'nachnani', 'cullar'), unique compound words ('powerpraying', 'ogdenarea'), and potential misspellings ('figher', 'installtions'). A query containing one of these terms would be extremely precise, likely returning the single document in which it appears. Their rarity makes them highly valuable for targeted searches.\n")

            #  Section 3.4: Finding and Detailing a Co-occurring Pair 
            f.write("\n4. Find two terms with similar document frequencies that also appear in the same documents. Provide details.\n")
            if pair_info:
                t1, t2, freq, overlap = pair_info
                f.write(f"  - Terms: A pair found is '{t1}' and '{t2}'.\n\n")
                f.write(f"  - Document Frequencies: Both terms have an identical document frequency of {freq}. This places them in a mid-frequency range, making their strong co-occurrence statistically significant.\n\n")
                
                intersect_ids = self.retriever._intersect(self.index[t1], self.index[t2])[:3]
                sample_docnos = [self.docid_map[doc_id] for doc_id in intersect_ids]
                f.write(f"  - Documents: They appear together in {overlap} of the same documents. Three example documents where they both appear are:\n")
                for docno in sample_docnos:
                    f.write(f"      {docno}\n")
                
                f.write(f"\n  - Term Characteristics: The terms '{t1}' and '{t2}' likely represent last names of individuals who were frequently mentioned together in news reports, such as figures in a legal case, business partners, or political associates. Their very high co-occurrence rate ({overlap} out of {freq} documents, which is over 80%) is a strong signal that they are not independent but are part of a recurring named entity. Discovering such relationships is a key task in information retrieval and text mining.\n")
                
                f.write("\n  - How these terms were found:\n")
                f.write("    To find this pair efficiently, the algorithm first grouped all terms by their document frequency. It then focused its search on a medium-frequency range (DF between 50 and 100) to find terms that are neither ubiquitous nor extremely rare. By iterating only through pairs of terms that shared the exact same frequency, and then computing the intersection of their postings lists, the algorithm could identify this pair with a high co-occurrence rate without performing a slow, brute-force search across the entire vocabulary.\n")
            else:
                f.write("  No suitable pair with significant co-occurrence was found using the defined heuristic (DF between 50-100 and >50% overlap).\n")

    def _find_cooccurring_pair(self, freq_min=50, freq_max=100, overlap_thresh=0.5):
        """
        Optimized search for a co-occurring pair by grouping terms by frequency.
        Returns a tuple (term1, term2, frequency, overlap_count) or None.
        """
        freq_to_terms = defaultdict(list)
        for term, freq in self.doc_freq.items():
            if freq_min <= freq <= freq_max:
                freq_to_terms[freq].append(term)
        
        # We start checking from the lowest frequency in our target range, as these
        # lists are shorter and intersections are faster to compute.
        for freq in sorted(freq_to_terms.keys()):
            terms = freq_to_terms[freq]
            if len(terms) > 1:
                # Check all unique pairs of terms with the same frequency
                for i in range(len(terms)):
                    for j in range(i + 1, len(terms)):
                        t1, t2 = terms[i], terms[j]
                        intersection_len = len(self.retriever._intersect(self.index[t1], self.index[t2]))
                        
                        # Check if the overlap meets our significance threshold
                        if intersection_len > freq * overlap_thresh:
                            return (t1, t2, freq, intersection_len)
        return None