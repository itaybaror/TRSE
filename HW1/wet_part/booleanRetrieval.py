class BooleanRetriever:
    """
    Performs Boolean retrieval using queries in Reverse Polish Notation (RPN).
    """
    def __init__(self, indexer):
        """Initializes the retriever with a constructed InvertedIndex object."""
        self.index = indexer.index
        self.docid_map = indexer.docid_map

    def _intersect(self, p1, p2):
        """Computes the intersection of two sorted postings lists. O(|p1| + |p2|)."""
        result = []
        i, j = 0, 0
        while i < len(p1) and j < len(p2):
            if p1[i] == p2[j]:
                result.append(p1[i]); i += 1; j += 1
            elif p1[i] < p2[j]:
                i += 1
            else:
                j += 1
        return result

    def _union(self, p1, p2):
        """Computes the union of two sorted postings lists. O(|p1| + |p2|)."""
        result, i, j = [], 0, 0
        while i < len(p1) or j < len(p2):
            if i < len(p1) and (j >= len(p2) or p1[i] < p2[j]):
                result.append(p1[i]); i += 1
            elif j < len(p2) and (i >= len(p1) or p2[j] < p1[i]):
                result.append(p2[j]); j += 1
            else:
                result.append(p1[i]); i += 1; j += 1
        return result

    def _and_not(self, p1, p2):
        """Computes the result of p1 AND NOT p2. O(|p1| + |p2|)."""
        result, i, j = [], 0, 0
        while i < len(p1) and j < len(p2):
            if p1[i] < p2[j]:
                result.append(p1[i]); i += 1
            elif p1[i] > p2[j]:
                j += 1
            else:
                i += 1; j += 1
        while i < len(p1):
            result.append(p1[i]); i += 1
        return result

    def retrieve(self, query):
        """Evaluates an RPN query using a stack."""
        tokens = query.split()
        stack = []
        for token in tokens:
            if token.upper() in ['AND', 'OR', 'NOT']:
                p2 = stack.pop()
                p1 = stack.pop()
                
                if token.upper() == 'AND':
                    # Optimization: intersect smaller list into larger one.
                    result = self._intersect(p1, p2) if len(p1) < len(p2) else self._intersect(p2, p1)
                elif token.upper() == 'OR':
                    result = self._union(p1, p2)
                elif token.upper() == 'NOT': # Treated as AND NOT
                    result = self._and_not(p1, p2)
                stack.append(result)
            else:
                stack.append(self.index.get(token, []))
        
        final_ids = stack.pop() if stack else []
        return [self.docid_map[doc_id] for doc_id in final_ids]