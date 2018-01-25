import pickle
import numpy as np
import spacy
nlp = spacy.load('en_core_web_lg')

def load_pickle(filepath):
    documents_f = open(filepath, 'rb')
    file = pickle.load(documents_f)
    documents_f.close()
    
    return file

def save_pickle(data, filepath):
    save_documents = open(filepath, 'wb')
    pickle.dump(data, save_documents)
    save_documents.close()

def divide_into_sentences(document):
    return [sent for sent in document.sents]

def number_of_fine_grained_pos_tags(sent):
    """
    Find all the tags related to words in a given sentence. Slightly more
    informative then part of speech tags, but overall similar data.
    Only one might be necessary. 
    For complete explanation of each tag, visit: https://spacy.io/api/annotation
    """
    tag_dict = {
    '-LRB-': 0, '-RRB-': 0, ',': 0, ':': 0, '.': 0, "''": 0, '""': 0, '#': 0, 
    '``': 0, '$': 0, 'ADD': 0, 'AFX': 0, 'BES': 0, 'CC': 0, 'CD': 0, 'DT': 0,
    'EX': 0, 'FW': 0, 'GW': 0, 'HVS': 0, 'HYPH': 0, 'IN': 0, 'JJ': 0, 'JJR': 0, 
    'JJS': 0, 'LS': 0, 'MD': 0, 'NFP': 0, 'NIL': 0, 'NN': 0, 'NNP': 0, 'NNPS': 0, 
    'NNS': 0, 'PDT': 0, 'POS': 0, 'PRP': 0, 'PRP$': 0, 'RB': 0, 'RBR': 0, 'RBS': 0, 
    'RP': 0, '_SP': 0, 'SYM': 0, 'TO': 0, 'UH': 0, 'VB': 0, 'VBD': 0, 'VBG': 0, 
    'VBN': 0, 'VBP': 0, 'VBZ': 0, 'WDT': 0, 'WP': 0, 'WP$': 0, 'WRB': 0, 'XX': 0,
    'OOV': 0, 'TRAILING_SPACE': 0}
    
    for token in sent:
        if token.is_oov:
            tag_dict['OOV'] += 1
        elif token.tag_ == '':
            tag_dict['TRAILING_SPACE'] += 1
        else:
            tag_dict[token.tag_] += 1
            
    return tag_dict

def number_of_specific_entities(sent):
    """
    Finds all the entities in the sentence and returns the amont of 
    how many times each specific entity appear in the sentence.
    """
    entity_dict = {
    'PERSON': 0, 'NORP': 0, 'FAC': 0, 'ORG': 0, 'GPE': 0, 'LOC': 0,
    'PRODUCT': 0, 'EVENT': 0, 'WORK_OF_ART': 0, 'LAW': 0, 'LANGUAGE': 0,
    'DATE': 0, 'TIME': 0, 'PERCENT': 0, 'MONEY': 0, 'QUANTITY': 0,
    'ORDINAL': 0, 'CARDINAL': 0 }
    
    entities = [ent.label_ for ent in sent.as_doc().ents]
    for entity in entities:
        entity_dict[entity] += 1
        
    return entity_dict

def sample(test_sent, classifier):
    # Preprocess using spacy
    parsed_test = divide_into_sentences(nlp(test_sent))
    
    # Get features
    sentence_with_features = {}
    entities_dict = number_of_specific_entities(parsed_test[0])
    sentence_with_features.update(entities_dict)
    pos_dict = number_of_fine_grained_pos_tags(parsed_test[0])
    sentence_with_features.update(pos_dict)
    
    # Transform features into array
    vals = np.fromiter(iter(sentence_with_features.values()), dtype=float)
    
    # Run a prediction
    prediction = classifier.predict(vals.reshape(1, -1))
    if prediction == 0:
        print('Your sentence: "' + test_sent + '" is a FACT!')
    else:
        print('Your sentence: "' + test_sent + '" is an OPINION!')

#==============================================================================
# Load models and test on random sentences
#==============================================================================
rf_classifier = load_pickle('models/rf_classifier.pickle')
svm_classifier = load_pickle('models/svm_classifier.pickle')
lr_classifier = load_pickle('models/lr_classifier.pickle')
nn_classifier = load_pickle('models/nn_classifier.pickle')

# Bunch of tests with different classifiers and sentences
test_sent = 'As far as I am concerned, donuts are amazing.'
sample(test_sent, rf_classifier)

test_sent = 'Donuts are a kind of ring-shaped, deep fried dessert.'
sample(test_sent, svm_classifier)

test_sent = 'Doughnut can also be spelled as "Donut", which is an American variant of the word.'
sample(test_sent, lr_classifier)

test_sent = 'This new graphics card I bought recently is pretty amazing, it has no trouble rendering my 3D donuts art in high quality.'
sample(test_sent, nn_classifier)

test_sent = 'I think this new graphics card is amazing, it has no trouble rendering my 3D donuts art in high quality.'
sample(test_sent, nn_classifier)