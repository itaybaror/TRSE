import os
from invertedIndex import InvertedIndex
from booleanRetrieval import BooleanRetriever
from collectionAnalyzer import CollectionAnalyzer

def main():
    """
    Main function to execute the full assignment pipeline from within the 'wet_part' directory.
    """
    # Define paths relative to the current directory (wet_part)
    data_path = 'data'
    queries_path = 'BooleanQueries.txt'
    output_path_2 = 'Part_2.txt'
    output_path_3 = 'Part_3.txt'

    #  Part 1: Build the Inverted Index 
    indexer = InvertedIndex()
    indexer.create_index(data_path)

    #  Part 2: Boolean Retrieval 
    print("\nStarting Boolean retrieval...")
    retriever = BooleanRetriever(indexer)
    try:
        with open(queries_path, 'r') as f:
            queries = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: '{queries_path}' not found. Please ensure it is in the 'wet_part' directory.")
        return

    with open(output_path_2, 'w') as f_out:
        for i, query in enumerate(queries):
            print(f"  Executing query {i+1}/{len(queries)}: {query}")
            results = retriever.retrieve(query)
            f_out.write(' '.join(results) + '\n')
    print(f"Boolean retrieval complete. Results saved to '{output_path_2}'")

    #  Part 3: Collection Statistics 
    print("\nStarting collection statistics analysis...")
    analyzer = CollectionAnalyzer(indexer, retriever)
    analyzer.generate_report(output_path_3)
    print(f"Collection statistics report saved to '{output_path_3}'")
    print("\nAssignment complete.")

if __name__ == '__main__':
    main()