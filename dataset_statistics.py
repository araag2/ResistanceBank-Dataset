import json
import os
from nltk.stem import PorterStemmer


def dataset_statistics():
    txt_destiny = "./txt/"
    reference_destiny = "./references/"

    stemmed_dic = {}
    stemmer = PorterStemmer()

    word_count = 0
    kp_count = 0
    absent_kp = 0
    n_docs = 0

    new_kp_dic = {}

    with open(f'{reference_destiny}test.json', 'rb') as ref_file:
        with open(f'{reference_destiny}test-stem.json', 'w', encoding='utf-8') as ref_file_stem:
            ref_dic = json.load(ref_file)
            
            for file in ref_dic:
                if os.path.exists(f'{txt_destiny}{file}.txt'):
                    new_kp_dic[file] = ref_dic[file]
                    with open(f'{txt_destiny}{file}.txt', 'r', encoding='utf-8') as txt_file:
                        raw_txt = txt_file.read()
                        word_count += len(raw_txt.split())

                        stemmed_dic[file] = []
                        kp_count += len(ref_dic[file])
                        for kp in ref_dic[file]:
                            if kp[0] not in raw_txt:
                                absent_kp += 1
                            stemmed_dic[file].append([stemmer.stem(kp[0])])
                    
            n_docs = len(stemmed_dic)
            json.dump(stemmed_dic, ref_file_stem, indent=4, separators=(',', ': '))

    with open(f'{reference_destiny}test.json', 'w', encoding='utf-8') as ref_file:
        json.dump(new_kp_dic, ref_file, indent=4, separators=(',', ': '))

    print(f'Dataset Statistics:\n  N_docs = {n_docs}\n  Avg word count = {word_count/n_docs:.3f}\n  Avg kp = {kp_count/n_docs:.1f}\n  Absent key-phrases = {(absent_kp/kp_count)*100:.2f}%')

dataset_statistics()