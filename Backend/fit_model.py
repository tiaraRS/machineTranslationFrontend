from pickle import load
from numpy import array
import tensorflow
import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
#from keras.utils import to_categorical
from keras.utils.vis_utils import plot_model
from keras.models import *
from keras.layers import *
from keras.callbacks import ModelCheckpoint
from tensorflow.keras.optimizers import Adam
import numpy as np
import matplotlib.pyplot as plt
def load_clean_sentences(filename):
	return load(open(filename, 'rb'))

def create_tokenizer(lines): #assigns id to words in lines vocab
	tokenizer = Tokenizer() #default filters punctuation
	tokenizer.fit_on_texts(lines)
	return tokenizer

def max_length(lines): #max words in a sentence
	return max(len(line.split()) for line in lines)

def encode_sequences(tokenizer, length, lines): #returns dim (#lines,length)
	# integer encode sequences
	X = tokenizer.texts_to_sequences(lines)
	#creates id array from tokenizer ids for each sentence
	# pad sequences with 0 values
	X = pad_sequences(X, maxlen=length, padding='post') # adds 0s to the end(post) of sequence
	return X

def encode_output(sequences, vocab_size): #returns 3d
	ylist = np.array([])
	for sequence in sequences:
		encoded = to_categorical(sequence, num_classes=vocab_size,dtype=int)
		ylist=np.append(ylist,encoded)
	y = array(ylist)
	y = y.reshape(sequences.shape[0], sequences.shape[1], vocab_size)
	return y

def load_data(ds_filename, train_ds_fn, test_ds_fn):    
    dataset = load_clean_sentences(ds_filename)
    train = load_clean_sentences(train_ds_fn)
    test = load_clean_sentences(test_ds_fn)
    return dataset,train,test

def prepare_tokenizer(dataset, index):
    tokenizer = create_tokenizer(dataset[:, index])
    vocab_size = len(tokenizer.word_index) + 1
    max_sentence_length = max_length(dataset[:, index])
    return tokenizer,vocab_size,max_sentence_length

def preprocess_input(origin_tok, origin_max_sent_length, target_tok, target_max_sent_length,target_vocab_size, data, one_hot=False):
    dataX = encode_sequences(origin_tok, origin_max_sent_length, data[:, 0])
    dataY = encode_sequences(target_tok, target_max_sent_length, data[:, 1])
    if one_hot:
        dataY = encode_output(dataY, target_vocab_size)
    return dataX,dataY

def graph_loss_vs_epochs(history, save_image_filename, title):
    training_loss = history.history['loss']
    test_loss = history.history['val_loss'] #[10 9 8 5 6 7] 3

    # Create count of the number of epochs
    epoch_count = range(1, len(training_loss) + 1) #[1 2 3 4 5 6]

    # Visualize loss history
    plt.title(title)
    plt.plot(epoch_count, training_loss, 'r--')
    plt.plot(epoch_count, test_loss, 'b-')
    plt.legend(['Training Loss', 'Test Loss'])
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.axvline(x = epoch_count[test_loss.index(min(test_loss))], color = 'c', linestyle="dotted")
    plt.savefig(save_image_filename) 
    plt.show()

def train_evaluate_model(trainX, trainY, testX,testY, epochs, batch_size, model, model_save_file_name, history_save_file_name):
    checkpoint = ModelCheckpoint(model_save_file_name, monitor='val_loss', verbose=1,save_best_only=True, mode='min')
    model.fit(trainX, trainY, epochs=epochs, batch_size=batch_size,  validation_data=(testX, testY),callbacks=[checkpoint], verbose=2)
    save_history(history_save_file_name, model)

def create_model(model,loss_func='categorical_crossentropy',learning_rate=0.001):
    optimizer = Adam(learning_rate)
    model.compile(optimizer=optimizer, loss=loss_func,metrics=['acc'])
    #categorical cross entropy -> one hot encoding output
    #sparse categorical cross entropy -> output as integers
    # summarize defined model
    print(model.summary())
   
def save_history(filename, model):
    # ejemplo de filename:'history1.npy'
    np.save(filename,model.history.history)
    
def load_history(filename):
    history=np.load(filename,allow_pickle='TRUE').item()
    return history


"""
def define_model(src_vocab, tar_vocab, src_timesteps, tar_timesteps, n_units):
	model = Sequential()
	model.add(Embedding(src_vocab, n_units, input_length=src_timesteps, mask_zero=True)) 
	model.add(LSTM(n_units))
	model.add(RepeatVector(tar_timesteps))
	model.add(LSTM(n_units, return_sequences=True))
	model.add(TimeDistributed(Dense(tar_vocab, activation='softmax')))
	return model

def define_model_2(src_vocab, tar_vocab, src_timesteps, tar_timesteps, n_units):
	model = Sequential()
	model.add(Embedding(src_vocab, n_units, input_length=src_timesteps, mask_zero=True)) 
	model.add(GRU(64, return_sequences=True))
	#model.add(RepeatVector(tar_timesteps))
	#model.add(LSTM(n_units, return_sequences=True))
	model.add(TimeDistributed(Dense(tar_vocab, activation='softmax')))
	return model
"""

from numpy import argmax
# asignar un número entero a una palabra
def word_for_id(integer, tokenizer):
    print('integer: ', integer)
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None
 
# generar la secuencia de origen del objetivo
def predict_sequence(model, tokenizer, source):
    #print(f"S {source}")
    prediction = model.predict(source, verbose=0)[0]
    print(f"PREDICTION {prediction.shape}")
    integers = [argmax(vector) for vector in prediction]
    print(f"integers {integers}")
    target = list()
    for i in integers:
        word = word_for_id(i, tokenizer)
        print(f"WORD: {word}")
        if word is None:
            break
        target.append(word)
    return' '.join(target)

import pickle

def save_tokenizer(file_name, tokenizer):
    with open(file_name, 'wb') as handle:
        pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

# loading
def load_tokenizer(file_name):
    with open(file_name, 'rb') as handle:
        tokenizer = pickle.load(handle)
        vocab_size = len(tokenizer.word_index) + 1
        print(vocab_size)
    return tokenizer, vocab_size