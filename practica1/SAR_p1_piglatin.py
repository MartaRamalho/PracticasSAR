#!/usr/bin/env python
#! -*- encoding: utf8 -*-
# Autora: Marta Filipa Ramalho
# 1.- Pig Latin

import re
import sys
from typing import Optional, Text
from os.path import isfile


class Translator():

    def __init__(self, punt: Optional[Text] = None):
        """
        Constructor de la clase Translator

        :param punt(opcional): una cadena con los signos de puntuación
                                que se deben respetar
        :return: el objeto de tipo Translator
        """
        if punt is None:
            punt = ".,;?!"
        self.re = re.compile(r"(\w+)([" + punt + r"]*)")

    def translate_word(self, word: Text) -> Text:
        """
        Recibe una palabra en inglés y la traduce a Pig Latin

        :param word: la palabra que se debe pasar a Pig Latin
        :return: la palabra traducida
        """
        # creamos un string con las diferentes vocales
        vocals = 'aeiouy'
        new_word = ''
        final = ''
        """comprobamos si la primera letra no es un caracter del alfabeto y 
        en caso de que no lo sea la devolvemos sin ningun cambio"""
        if not word[0].isalpha():
            return word
        # si es una letra comprobamos si es vocal o consonante
        else:
            """"comprobamos que la primera letra esté entre las vocales 
            en minuscula o en mayuscula"""
            if word[0] in vocals or word[0] in vocals.upper():
                new_word = word+'yay'
            # si empieza por consonante:
            else:
                letter = ''
                i = 0
                # separamos en un string el prefijo formado únicamente por consonantes
                for letter in word:
                    if letter not in vocals and letter not in vocals.upper():
                        final = final+letter
                    else:
                        break
                    i = i+1
                # movemos al final de la palabra el prefijo de consonantes
                final[0].lower()
                new_word = word[i:]+final+'ay'
        """comprobamos si la palabra original estaba en mayúsculas, si solo
        tenía la primera letra en mayúscula o si estaba en minúscula y devolvemos
        la nueva palabra de la misma forma"""
        if word.isupper():
            new_word = new_word.upper()
        elif word[0].isupper():
            new_word = new_word.capitalize()
        elif word.islower():
            new_word = new_word.lower()
        return new_word

    def translate_sentence(self, sentence: Text) -> Text:
        """
        Recibe una frase en inglés y la traduce a Pig Latin

        :param sentence: la frase que se debe pasar a Pig Latin
        :return: la frase traducida
        """
        new_sentence = ""
        """"bucle para separar las palabras de sus signos de puntuación y 
        añadirlos al final de la nueva palabra para crear la nueva frase"""
        for w, p in self.re.findall(sentence):
            newWord = self.translate_word(w)+p
            # si es la primera palabra no añadimos espacio antes
            if new_sentence == "":
                new_sentence = new_sentence + newWord
            else:
                new_sentence = new_sentence+" "+newWord
        return new_sentence

    def translate_file(self, filename: Text):
        """
        Recibe un fichero y crea otro con su tradución a Pig Latin

        :param filename: el nombre del fichero que se debe traducir
        :return: None
        """
        if not isfile(filename):
            print(f'{filename} no existe o no es un nombre de fichero',
                  file=sys.stderr)
        # abrimos el archivo y creamos el nuevo añadiendo el sufijo '_piglatin'
        file = open(filename)
        nameSplit = filename.split('.')
        newFile = nameSplit[0]+'_piglatin.'+nameSplit[1]
        newFile = open(newFile, "w")
        lines = file.readlines()
        # separamos por lineas y las traducimos con la función translate_sentence
        for line in lines:
            newSentence = t.translate_sentence(line)
            newFile.write(newSentence+'\n')


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(f'Syntax: python {sys.argv[0]} [filename]')
        exit()
    t = Translator()
    if len(sys.argv) == 2:
        t.translate_file(sys.argv[1])
    else:
        sentence = input("ENGLISH: ")
        while len(sentence) > 1:
            print("PIG LATIN:", t.translate_sentence(sentence))
            sentence = input("ENGLISH: ")
