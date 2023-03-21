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
        """
        Este método analiza la frase pasada por parámetro separándola en los diferentes n-gramas y 
        añadiendola al modelo.

        :param 
            sentence: frase a analizar y añadir al modelo
        """
        n = self.info['n']
        for i in range(2, n+1):
            # añadimos antes de la frase un número de dólares según el n-grama a considerar
            # por ejemplo: para los bigramas, añadimos 1 $ y para los trigramas añadimos 2 $, etc.
            sentenceN = '$ '*(i-1) + sentence
            words = sentenceN.split()
            # creamos un bucle que asigne a la variable w los diferentes valores de posiciones del vector words
            for w in range(len(words)):
                # comprobamos que si sumamos i a la posición w, este no es mayor que el tamaño del vector de palabras
                if w+i <= len(words):
                    # creamos una tupla con la palabra en posición w y las i-2 palabras siguientes
                    ngram = tuple(words[w:w+i-1])
                    # añadimos la tupla a info con un diccionario vacio si no existe
                    self.info['lm'][i][ngram] = {
                    } if ngram not in self.info['lm'][i] else self.info['lm'][i][ngram]
                    # se suma uno al contador de veces que aparece la palabra después de la tupla obtenida
                    countWord = 1 if words[w +
                                           i-1] not in self.info['lm'][i][ngram] else self.info['lm'][i][ngram][words[w+i-1]]+1
                    self.info['lm'][i][ngram][words[w+i-1]] = countWord

    def compute_lm(self, filenames: List[str], lm_name: str, n: int):
        """
        Este método separa un archivo por frases y llama al método index_sentence con cada una de
        ellas

        :param 
            filenames: lista de archivos a procesar
            lm_name: nombre del archivo .lm destino
            n: número de n-gramas a considerar
        """
        self.info = {'name': lm_name, 'filenames': filenames, 'n': n, 'lm': {}}
        for i in range(2, n+1):
            self.info['lm'][i] = {}
        for filename in filenames:
            # separamos el archivo en frases, las cuales están separadas por signos de puntuación o doble salto de línea
            sentences = self.r1.split(
                open(filename, encoding='utf-8').read().replace('\n\n', '.'))
            for line in sentences:
                # eliminamos los signos indeseados de la frase y la pasamos a minuscula
                line = self.r2.sub(" ", line).lower()
                # comprobamos que no sea una frase vacía, y si lo es, saltamos a la siguiente iteración
                if not line.strip():
                    continue
                # si no lo es, añadimos el $ final y llamamos al método index_sentence
                line = line+' $'
                self.index_sentence(line)
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
        """
        Este método generea frases aleatorias a partir de un archivo .lm que contiene
        el lenguaje.

        :param 
            n: número que indica qué n-grama utilizar para generar las frases
            nsentences: número de frases que se desea generar
            prefix: prefijo que se desea tener en todas las frases
        """
        if not n:
            n = self.get_n()
        if prefix:
            prefLen = len(prefix.split())
            # si la longitud del prefijo es menor o igual que el tamaño de las tuplas,
            # se añaden n $ hasta que la longitud coincida con la de la tupla
            if prefLen <= n-1:
                prefixAux = "$ "*(n-prefLen-1)+prefix
            # si el prefijo es demasiado largo, se cojerán solo las n-1 últimas palabras para formar la tupla
            else:
                prefixAux = ' '.join(prefix.split()[prefLen-n+1:])
        # si no se ha elegido un prefijo o éste no existe en info, entonces se empezará a formar las frases por la tupla de n-1 $
        if not prefix or tuple(prefixAux.split()) not in self.info['lm'][n]:
            prefixAux = '$ '*(n-1)
        for sentence in range(nsentences):
            thisTuple = tuple(prefixAux.split())
            last = ''
            sentence = prefix if prefix else ''
            word = ''
            # mientras que la última palabra procesada no sea $ y la frase tenga menos de 50 palabras
            # se obtiene un numero aleatorio y se elige la palabra sucesora de la tupla en la que cae dicho número aleatorio
            while '$' not in last and len(sentence.split()) != 50:
                max = self.info['lm'][n][thisTuple][0]
                index = random.randint(1, max)
                sumWeight = 0
                for weight, word in self.info['lm'][n][thisTuple][1]:
                    sumWeight += weight
                    # cuando alcanzamos el número aleatorio generado, comprobamos si la palabra elegida es un $ o no,
                    # si lo es, terminamos esta frase y empezamos otra
                    if sumWeight >= index:
                        if word == '$':
                            break
                        # en caso contrario, añadimos la palabra a la frase y generamos la nueva tupla con esta palabra
                        sentence += " "+word
                        thisTuple = thisTuple[-(n-2):] + \
                            (word, ) if n > 2 else (word, )
                        break
                last = word
            print(sentence)
        pass


if __name__ == "__main__":
    print("Este fichero es una librería, no se puede ejecutar directamente")
