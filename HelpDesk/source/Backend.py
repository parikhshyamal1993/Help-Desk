from flask import Flask, redirect, url_for , request ,jsonify
from Application import TopicInference
construct = TopicInference()
app = Flask(__name__) 

@app.route("/Qsection/<query>")
def Comunicator(query):
    print(query)
    Title , FileOutput = construct.run(str(query))
    print(Title,FileOutput)
    return jsonify([Title,FileOutput])

@app.route("/UpdateDB")
def DBUpdate():
    construct.AdminDbUpdate()
    return "1"
if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000, debug=True)