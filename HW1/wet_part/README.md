***Collaborators***
 - Itay Bar Or `808711`
 - Hershel Thomas `808894`

**Setup:**
   - Make sure the `data` directory with all 9 `AP_Coll_Parsed_*` subfolders is placed inside the `wet_part` directory.
   - the subfolders are all expected to be unzipped
   - Ensure the `BooleanQueries.txt` file is present and contains the queries to be executed. Can be Changed to whatever you want as long as it follows RPN.

**Execution:**
   - Open your terminal or command prompt.
   - Navigate into the `wet_part` directory:
     ```bash
     cd path/to/your/project/wet_part
     ```
   - Run the main script:
     ```
     python main.py
     ```

**Additional Files:**
  - We created `collectionAnalyzer.py` in order to display results for part 3. 
  - We created `main.py` as the injection point to run all of our code using 
    ```
    python main.py
    ```