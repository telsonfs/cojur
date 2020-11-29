import pandas as pd
import nltk
from nltk import tokenize
import re

nltk.download('punkt')

def tag_entity(named_entity):
    dict_tag = {
        'Lei Complementar': 'LCOMP',
        'Lei Delegada': 'LDEL',
        'Decreto-Lei': 'DLEI',
        'Decreto Legislativo': 'DLEG',
        'Medida Provisória': 'MP',
        'Emenda Constitucional': 'EC',
        'Decreto': 'DEC',
        'Lei': 'LEI'
    }

    for key, value in dict_tag.items():
        if key in str(named_entity): return value

def note_taker(text, named_entity_arr):
    anotated_text = []
    text_tokenize = tokenize.word_tokenize(text, language = 'portuguese')
    i = 0

    while(i < len(text_tokenize)):
        compare = False

        for named_entity in named_entity_arr:
            named_entity_tokenize = tokenize.word_tokenize(named_entity, language = 'portuguese')

            if text_tokenize[i: i + len(named_entity_tokenize)] == named_entity_tokenize:
                anotated_text.append(f'{text_tokenize[i]} B-{tag_entity(named_entity)}')

                for j in range(1, len(named_entity_tokenize)):
                    anotated_text.append(f'{text_tokenize[i+j]} I-{tag_entity(named_entity)}')

                compare = True
                i += len(named_entity_tokenize)

        if compare == False:
            anotated_text.append(f'{text_tokenize[i]} O')
            i += 1
            
    return anotated_text, text_tokenize
