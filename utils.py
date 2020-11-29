import pandas as pd
import nltk
from nltk import tokenize
import re

nltk.download('punkt')

def make_tag_entity(named_entity):
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

def make_note(text, named_entity_arr):
    anotated_text = []
    text_tokenize = tokenize.word_tokenize(text, language = 'portuguese')
    i = 0

    while(i < len(text_tokenize)):
        compare = False

        for named_entity in named_entity_arr:
            named_entity_tokenize = tokenize.word_tokenize(named_entity, language = 'portuguese')

            if text_tokenize[i: i + len(named_entity_tokenize)] == named_entity_tokenize:
                anotated_text.append(f'{text_tokenize[i]} B-{make_tag_entity(named_entity)}')

                for j in range(1, len(named_entity_tokenize)):
                    anotated_text.append(f'{text_tokenize[i+j]} I-{make_tag_entity(named_entity)}')

                compare = True
                i += len(named_entity_tokenize)

        if compare == False:
            anotated_text.append(f'{text_tokenize[i]} O')
            i += 1
            
    return anotated_text, text_tokenize

def create_corpus(description_arr):
    train_docs = []
    test_docs = []

    amount_text = 0

    lines = []
    words = []
    chars = []
    df_note = pd.DataFrame({'named_entities': []})
    for description in description_arr:
        named_entities_arr = []

        if type(description) is not float:
            text = description.split("'")[1] if len(description.split("'")) > 1 else description
            
                
            named_entities_arr.extend(re.findall(r'Lei\sComplementar\sno\s\d+.\d+|Lei\sComplementar\sno\s\d+', text))
            named_entities_arr.extend(re.findall(r'Lei\sDelegada\sno\s\d+.\d+|Lei\sDelegada\sno\s\d+', text))
            named_entities_arr.extend(re.findall(r'\sLei\sno\s\d+.\d+|Lei\sno\s\d+ ', text))
            named_entities_arr.extend(re.findall(r'Decreto-Lei\sno\s\d+.\d+|Decreto-Lei\sno\s\d+', text))
            named_entities_arr.extend(re.findall(r'Decreto\sLegislativo\sno\s\d+.\d+|Decreto\sLegislativo\sno\s\d+', text))
            named_entities_arr.extend(re.findall(r'\sDecreto\sno\s\d+.\d+|Decreto\sno\s\d+', text))
            named_entities_arr.extend(re.findall(r'Medida\sProvisória\sno\s\d+.\d+|Medida\sProvisória\sno\s\d+', text))
            named_entities_arr.extend(re.findall(r'Emenda\sConstitucional\sno\s\d+.\d+|Emenda\sConstitucional\sno\s\d+', text))

            if named_entities_arr:
                amount_text += 1
                corpus, text_tokens = make_note(text, named_entities_arr)

                if amount_text < 9: 
                    train_docs.extend(corpus)
                    train_docs.append(' ')

                elif amount_text < 11: 
                    test_docs.extend(corpus)
                    test_docs.append(' ')

                else: amount_text = 0

                words.extend(text_tokens)
                df_note = df_note.append(named_entities_arr, ignore_index=True)

    with open('dataset/train.txt', 'w') as arquivo:
        for train in train_docs: arquivo.write(f'{train}\n')
                
    with open('dataset/test.txt', 'w') as arquivo:
        for test in test_docs: arquivo.write(f'{test}\n')

    with open('dataset/words.txt', 'w') as words_arq:
        for word in set(words): 
            words_arq.write(f'{word}\n')
            chars.extend(list(word))

    with open('dataset/chars.txt', 'w') as chars_arq:
        for char in set(chars): chars_arq.write(f'{char}\n')

    df_note.to_csv('dataset/note_taker_automatic_info.csv', sep = '\t')
