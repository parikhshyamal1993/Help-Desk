# Help-Desk

This is a simple implementation of a text search algorithm based on context objectness score .
We are generating vector embedding of titles which are considered as a summary of documents.
We can add new  documents to DocumentLibrary and w.r.t documents a title csv containing document 
name and document title.

We are using Word2Vector model for generating embeddings :
Link : https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit?resourcekey=0-wjGZdNAUop6WykTtMip30g

Place this weights in ../Assets/Model/ 


To start the backend server run :
python3 Beckend.py

For Frontend Run :

streamlit run RestAPI.py


TODO:

1) Threshold: currently we are showing the best matched result . We can add a threshold of confidence 
2) cognitive : we can add a document summarizer which will generate titles for csv
3) Q&A : From the classified text document we can get particular answer to query 

