from flask import Flask, request, Response, jsonify
from flask_cors import CORS, cross_origin
from keras.models import load_model
from fit_model import *
import os

app = Flask(__name__)
app.config['CORS_HEADERS']='Content-Type'
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CURR_DIR = os.path.dirname(os.path.realpath(__file__))

best_model_t_es = load_model(f'{CURR_DIR}/Models/best_model-VF-80000.h5')
best_model_t_se = load_model(f'{CURR_DIR}/Models/model_spa_eng_80000.h5')

print('CURRENT DIRECTORYYYYYYYYY:',CURR_DIR)
eng_tokenizer_es, eng_vocab_size_es = load_tokenizer(f'{CURR_DIR}/Tokenizers/eng_tokenizer_80000_eng_spa-2.pickle')
spa_tokenizer_es, spa_vocab_size_es = load_tokenizer(f'{CURR_DIR}/Tokenizers/spa_tokenizer_80000_eng_spa-2.pickle')

eng_tokenizer_se, eng_vocab_size_se = load_tokenizer(f'{CURR_DIR}/Tokenizers/eng_tokenizer_80000_spa_eng.pickle')
spa_tokenizer_se, spa_vocab_size_se = load_tokenizer(f'{CURR_DIR}/Tokenizers/spa_tokenizer_80000_spa_eng.pickle')

@app.route("/eng_spa",methods=['POST'])
@cross_origin()
def translate_eng_spa():
  print("egn spa")
  data = request.get_json(force=True)
  print(data)
  texto = data["translation_text"]
  x_prediction_test=encode_sequences(eng_tokenizer_es, 47, [texto])
  print(x_prediction_test)
  translation = predict_sequence(best_model_t_es,spa_tokenizer_es,x_prediction_test)
  print(translation)
  return jsonify({"translation":translation})

@app.route("/spa_eng",methods=['POST'])
@cross_origin()
def translate_spa_eng():
  print("spa eng")
  data = request.get_json(force=True)
  print(data)
  texto = data["translation_text"]
  
  x_prediction_test=encode_sequences(spa_tokenizer_se, 44, [texto])
  translation = predict_sequence(best_model_t_se,eng_tokenizer_se,x_prediction_test)
  print(translation)
  return jsonify({"translation":translation})

if __name__ == '__main__':
   app.run(port=5002)
