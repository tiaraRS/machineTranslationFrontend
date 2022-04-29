from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin
from keras.models import load_model
from fit_model import *

app = Flask(__name__)
app.config['CORS_HEADERS']='Content-Type'
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
import os
CURR_DIR = os.path.dirname(os.path.realpath(__file__))
print(CURR_DIR)
best_model_t = load_model('C:/TIARA/UNIVERSIDAD/SEMESTRE 7/SISTEMAS INTELIGENTES/PROYECTO MACHINE TRANSLATION FINAL/MachineTranslation/PROYECTO MACHINE TRANSLATION/Models/tr_model_1_2.h5')
print('CURRENT DIRECTORYYYYYYYYY:',CURR_DIR)
eng_tokenizer, eng_vocab_size = load_tokenizer(f'{CURR_DIR}/Tokenizers/eng_tokenizer_10000.pickle')
spa_tokenizer, spa_vocab_size = load_tokenizer(f'{CURR_DIR}/Tokenizers/spa_tokenizer_10000.pickle')

print(spa_tokenizer.texts_to_sequences(['hola mundo es', 'chau chau', 'como estas', 'estas bien']))
print(eng_tokenizer.texts_to_sequences(['hello world', 'bye bye', 'how are you', 'fine']))
@app.route("/",methods=['POST'])
@cross_origin()
def helloWorld():
  data = request.get_json(force=True)
  print(data)
  texto = data["translation_text"]
  

  x_prediction_test=encode_sequences(eng_tokenizer, 8, [texto])
  print(x_prediction_test)
  #source = x_prediction_test.reshape((1, x_prediction_test.shape[0]))
  translation = predict_sequence(best_model_t,spa_tokenizer,x_prediction_test)
  print(translation)
  #texto = "hola"
  return jsonify({"translation":translation})

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
