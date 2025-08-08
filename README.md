"Figma2VectorDB" have all the code and "documentation" have Screenshot  Workflow and detail about the output generated.

in cmmd write :-
python -m venv venv
.\venv\Scripts\Activate.ps1       (for windows)
pip install -r requirements.txt


python scripts/extract_nodes.py
python scripts/embed_data.py
python scripts/build_faiss_index.py

python scripts/build_faiss_index.py query "Dashboard"



