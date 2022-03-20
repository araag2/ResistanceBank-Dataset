import json
import os
from nltk.stem import PorterStemmer

txt_destiny = "./txt/"
reference_destiny = "./references/"

def trim_bad_docs(number):
    new_kp_dic = {}
    absent_dic = {}
    with open(f'{reference_destiny}test.json', 'rb') as ref_file:
        ref_dic = json.load(ref_file)

        for file in ref_dic:
            with open(f'{txt_destiny}{file}.txt', 'r', encoding='utf-8') as txt_file:
                raw_txt = txt_file.read()
                absent_kp = 0.0
                for kp in ref_dic[file]:
                    if kp[0] not in raw_txt:
                        absent_kp += 1.0
                    absent_dic[file] = round(absent_kp/len(ref_dic[file]), 4)

        absent_dic = {k: v for k, v in sorted(absent_dic.items(), key=lambda item: item[1])[:-number]}
        print(sorted(absent_dic.items(), key=lambda item: item[1]))

        for file in absent_dic:
            new_kp_dic[file] = ref_dic[file]

    with open(f'{reference_destiny}test.json', 'w', encoding='utf-8') as ref_file:
        json.dump(new_kp_dic, ref_file, indent=4, separators=(',', ': '))

    delete_missing_docs()

def delete_missing_docs():
    with open(f'{reference_destiny}test.json', 'rb') as ref_file:
        ref_dic = json.load(ref_file)

        for file in os.listdir(txt_destiny):
            if file[:-4] not in ref_dic:
                os.remove(f'{txt_destiny}{file}')

def dataset_build():
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

#trim_bad_docs(30)
dataset_build()