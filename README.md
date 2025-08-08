"Figma2VectorDB" have all the code and "documentation" have Screenshot of OUTPUT ,WOrkflow and detail about the output generated.

in cmmd write :-
python -m venv venv        <br>
.\venv\Scripts\Activate.ps1       (for windows)   <br>
pip install -r requirements.txt   <br>

   <br>   <br>
python scripts/extract_nodes.py   <br>
python scripts/embed_data.py   <br>
python scripts/build_faiss_index.py   <br>
   <br>   <br>
python scripts/build_faiss_index.py query "Dashboard"   <br>



