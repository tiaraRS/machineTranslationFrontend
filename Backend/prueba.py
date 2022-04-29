from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['CORS_HEADERS']='Content-Type'
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route("/",methods=['POST'])
@cross_origin()
def helloWorld():
  data = request.get_json(force=True)
  print(data)
  texto = data["translation_text"]
  #texto = "hola"
  return jsonify({"translation":f"Traduccion de {texto}"})

"""
@app.route("/",methods=['GET'])
@cross_origin()
def helloWorld():
  #data = request.get_json(force=True)
  #print(data)
  #texto = data["translation_text"]
  texto = "hola"
  return {"translation":f"Traduccion de {texto}"}"""

if __name__ == '__main__':
   app.run(port=5002)
