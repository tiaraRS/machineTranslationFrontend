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
#print(CURR_DIR)
best_model_t_es = load_model(f'{CURR_DIR}/Models/tr_model_1_2_eng_spa_10000.h5')
best_model_t_se = load_model(f'{CURR_DIR}/Models/model_spa_eng_80000.h5')
#best_model_t.compile()
#best_model_t.summary()
print('CURRENT DIRECTORYYYYYYYYY:',CURR_DIR)
eng_tokenizer_es, eng_vocab_size_es = load_tokenizer(f'{CURR_DIR}/Tokenizers/eng_tokenizer_10000_eng_spa.pickle')
spa_tokenizer_es, spa_vocab_size_es = load_tokenizer(f'{CURR_DIR}/Tokenizers/spa_tokenizer_10000_eng_spa.pickle')

eng_tokenizer_se, eng_vocab_size_se = load_tokenizer(f'{CURR_DIR}/Tokenizers/eng_tokenizer_80000_spa_eng.pickle')
spa_tokenizer_se, spa_vocab_size_se = load_tokenizer(f'{CURR_DIR}/Tokenizers/spa_tokenizer_80000_spa_eng.pickle')
#print('eng_tokenizer',len(eng_tokenizer.word_index) + 1)
#print('spa_tokenizer',len(spa_tokenizer.word_index) + 1)
#print(spa_tokenizer.texts_to_sequences(['hola mundo es', 'chau chau', 'como estas', 'estas bien']))
#print(eng_tokenizer.texts_to_sequences(['hello world', 'bye bye', 'how are you', 'fine']))
@app.route("/eng_spa",methods=['POST'])
@cross_origin()
def translate_eng_spa():
  data = request.get_json(force=True)
  print(data)
  texto = data["translation_text"]
  

  x_prediction_test=encode_sequences(eng_tokenizer_es, 5, [texto])
  print(x_prediction_test)
  #source = x_prediction_test.reshape((1, x_prediction_test.shape[0]))
  translation = predict_sequence(best_model_t_es,spa_tokenizer_es,x_prediction_test)
  print(translation)
  #texto = "hola"
  return jsonify({"translation":translation})

@app.route("/spa_eng",methods=['POST'])
@cross_origin()
def translate_spa_eng():
  data = request.get_json(force=True)
  print(data)
  texto = data["translation_text"]
  
  x_prediction_test=encode_sequences(spa_tokenizer_se, 44, [texto])
  print(x_prediction_test)
  #source = x_prediction_test.reshape((1, x_prediction_test.shape[0]))
  translation = predict_sequence(best_model_t_se,eng_tokenizer_se,x_prediction_test)
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
