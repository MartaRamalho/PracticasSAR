#!/usr/bin/env python
#! -*- encoding: utf8 -*-
# 3.- Mono Library

import pickle
import random
import re
import sys
from typing import List, Optional, TextIO

# Nombres: Marta Filipa Ramalho

########################################################################
########################################################################
###                                                                  ###
###  Todos los métodos y funciones que se añadan deben documentarse  ###
###                                                                  ###
########################################################################
########################################################################


def convert_to_lm_dict(d: dict):
    for k in d:
        l = sorted(((y, x) for x, y in d[k].items()), reverse=True)
        d[k] = (sum(x for x, _ in l), l)


class Monkey():

    def __init__(self):
        self.r1 = re.compile('[.;?!]')
        self.r2 = re.compile('\W+')
        self.info = {}

    def get_n(self):
        return self.info.get('n', 0)

    def index_sentence(self, sentence: str):
        n = self.info['n']
        for i in range(2, n+1):
            sentenceN = '$ '*(i-1) + sentence
            words = sentenceN.split()
            for w in range(len(words)):
                if w+i <= len(words):
                    ngram = tuple(words[w:w+i-1])
                    self.info['lm'][i][ngram] = {
                    } if ngram not in self.info['lm'][i] else self.info['lm'][i][ngram]
                    countWord = 1 if words[w +
                                           i-1] not in self.info['lm'][i][ngram] else self.info['lm'][i][ngram][words[w+i-1]]+1
                    self.info['lm'][i][ngram][words[w+i-1]] = countWord
        print(self.info)

    def compute_lm(self, filenames: List[str], lm_name: str, n: int):
        self.info = {'name': lm_name, 'filenames': filenames, 'n': n, 'lm': {}}
        for i in range(2, n+1):
            self.info['lm'][i] = {}

        for filename in filenames:
            sentences = self.r1.split(open(filename, encoding='utf-8').read())
            for line in sentences:
                s = line.split('\n\n')
                for l in s:
                    if l != '':
                        l = self.r2.sub(" ", l).lower()+' $'
                        self.index_sentence(l)
        for i in range(2, n+1):
            convert_to_lm_dict(self.info['lm'][i])

    def load_lm(self, filename: str):
        with open(filename, "rb") as fh:
            self.info = pickle.load(fh)

    def save_lm(self, filename: str):
        with open(filename, "wb") as fh:
            pickle.dump(self.info, fh)

    def save_info(self, filename: str):
        with open(filename, "w", encoding='utf-8', newline='\n') as fh:
            self.print_info(fh=fh)

    def show_info(self):
        self.print_info(fh=sys.stdout)

    def print_info(self, fh: TextIO):
        print("#" * 20, file=fh)
        print("#" + "INFO".center(18) + "#", file=fh)
        print("#" * 20, file=fh)
        print(f"language model name: {self.info['name']}", file=fh)
        print(
            f'filenames used to learn the language model: {self.info["filenames"]}', file=fh)
        print("#" * 20, file=fh)
        print(file=fh)
        for i in range(2, self.info['n']+1):
            print("#" * 20, file=fh)
            print("#" + f'{i}-GRAMS'.center(18) + "#", file=fh)
            print("#" * 20, file=fh)
            for prev in sorted(self.info['lm'][i].keys()):
                wl = self.info['lm'][i][prev]
                print(
                    f"'{' '.join(prev)}'\t=>\t{wl[0]}\t=>\t{', '.join(['%s:%s' % (x[1], x[0]) for x in wl[1]])}", file=fh)

    def generate_sentences(self, n: Optional[int], nsentences: int = 10, prefix: Optional[str] = None):
        if not n:
            n = self.get_n()
        if prefix:
            prefLen = len(prefix.split())
            if prefLen <= n-1:
                prefixAux = "$ "*(n-prefLen-1)+prefix
            else:
                prefixAux = ' '.join(prefix.split()[prefLen-n+1:])
        if not prefix or tuple(prefixAux.split()) not in self.info['lm'][n]:
            prefixAux = '$ '*(n-1)
        for sentence in range(nsentences):
            thisTuple = tuple(prefixAux.split())
            last = ''
            sentence = prefix
            word = ''
            while '$' not in last and len(sentence.split()) != 50:
                max = self.info['lm'][n][thisTuple][0]
                index = random.randint(1, max)
                sumWeight = 0
                for weight, word in self.info['lm'][n][thisTuple][1]:
                    sumWeight += weight
                    if sumWeight >= index:
                        if word == '$':
                            break
                        sentence += " "+word
                        thisTuple = thisTuple[-(n-2):] + \
                            (word, ) if n > 2 else (word, )
                        break
                last = word
            print(sentence)
        pass


if __name__ == "__main__":
    print("Este fichero es una librería, no se puede ejecutar directamente")
