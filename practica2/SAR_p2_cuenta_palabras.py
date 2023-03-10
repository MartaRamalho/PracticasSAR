#! -*- encoding: utf8 -*-

# Nombres: Marta Filipa Ramalho

import argparse
import os
import re
from typing import Optional


def sort_dic_by_values(d: dict) -> list:
    return sorted(d.items(), key=lambda a: (-a[1], a[0]))


class WordCounter:

    def __init__(self):
        """
           Constructor de la clase WordCounter
        """
        self.clean_re = re.compile('\W+')

    def write_stats(self, filename: str, stats: dict, use_stopwords: bool, full: bool):
        """
        Este método escribe en fichero las estadísticas de un texto

        :param 
            filename: el nombre del fichero destino.
            stats: las estadísticas del texto.
            use_stopwords: booleano, si se han utilizado stopwords
            full: boolean, si se deben mostrar las stats completas
        """

        with open(filename, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('Lines: %s\n' % (stats.get('nlines')))
            fh.write('Number words (including stopwords): %s\n'
                     % (stats.get('nwords')))
            # calcular suma de frecuencias de las palabras sin contar stopwords
            if use_stopwords:
                num = 0
                for key, value in sorted(stats.get('word').items()):
                    num += value
                fh.write('Number words (without stopwords): %s\n' % (num))

            fh.write('Vocabulary size: %s\n' %
                     (len(stats.get('word'))))

            symbols = 0
            # calcular numero total de simbolos
            for key, value in sorted(stats.get('symbol').items()):
                symbols += value
            fh.write('Number of symbols: %s\n' % (symbols))
            fh.write('Number of different symbols: %s\n' %
                     (len(stats.get('symbol'))))

            orderedWords = self.order_dict(
                sorted(stats.get('word').items()), full)
            fh.write('Words (alphabetical order):\n%s' % (orderedWords))

            sortedWordsByValue = self.order_dict(
                sort_dic_by_values(stats['word']), full)
            fh.write('\nWords (by frequency):\n%s' % (sortedWordsByValue))

            sortedSymbols = self.order_dict(
                sorted(stats.get('symbol').items()), full)
            fh.write('\nSymbols (alphabetical order):\n%s' % (sortedSymbols))

            sortedSymbolsByValue = self.order_dict(
                sort_dic_by_values(stats['symbol']), full)
            fh.write('\nSymbols (by frequency):\n%s' % (sortedSymbolsByValue))

            if 'biword' and 'bisymbol' in stats:
                sortedBiwords = self.order_dict(
                    sorted(stats.get('biword').items()), full)
                fh.write('\nWord pairs (alphabetical order):\n%s' %
                         (sortedBiwords))

                sortedBiwordsByValue = self.order_dict(
                    sort_dic_by_values(stats['biword']), full)
                fh.write('\nWord pairs (by frequency):\n%s' %
                         (sortedBiwordsByValue))

                sortedBisymbols = self.order_dict(
                    sorted(stats.get('bisymbol').items()), full)
                fh.write('\nSymbol pairs (alphabetical order):\n%s' %
                         (sortedBisymbols))

                sortedBisymbolsByValue = self.order_dict(
                    sort_dic_by_values(stats['bisymbol']), full)
                fh.write('\nSymbol pairs (by frequency):\n%s' %
                         (sortedBisymbolsByValue))

            sortedPrefixes = self.order_dict(
                sort_dic_by_values(stats['prefix']), full)
            fh.write('\nPrefixes (by frequency):\n%s' % (sortedPrefixes))

            sortedSuffixes = self.order_dict(
                sort_dic_by_values(stats['suffix']), full)
            fh.write('\nSuffixes (by frequency):\n%s' % (sortedSuffixes))

            pass

    def order_dict(self, ordered: list, full: bool):
        """
        Este método formata y guarda en un string los diferentes
        elementos de una lista ordenada

        :param 
            ordered: el nombre de la lista ordenada
            full: boolean, si se deben mostrar las stats completas

        :return: string
        """
        firstSorted = ordered.pop(0)
        sortedWordsByValue = '\t%s: %s' % (
            firstSorted[0], firstSorted[1])
        limit = 1
        for key, value in ordered:
            if key != firstSorted:
                # comprobando que no estamos en la primera palabra para añadir \n
                sortedWordsByValue += '\n\t%s: %s' % (key, value)
            limit += 1
            if not full and limit == 20:
                break
        return sortedWordsByValue

    def file_stats(self, fullfilename: str, lower: bool, stopwordsfile: Optional[str], bigrams: bool, full: bool):
        """
        Este método calcula las estadísticas de un fichero de texto

        :param 
            fullfilename: el nombre del fichero, puede incluir ruta.
            lower: booleano, se debe pasar todo a minúsculas?
            stopwordsfile: nombre del fichero con las stopwords o None si no se aplican
            bigram: booleano, se deben calcular bigramas?
            full: booleano, se deben montrar la estadísticas completas?
        """

        stopwords = [] if stopwordsfile is None else open(
            stopwordsfile, encoding='utf-8').read().split()

        # variables for results

        sts = {
            'nwords': 0,
            'nlines': 0,
            'word': {},
            'symbol': {},
            'prefix': {},
            'suffix': {}
        }

        if bigrams:
            sts['biword'] = {}
            sts['bisymbol'] = {}

        fullfile = open(fullfilename, encoding='utf-8')
        for line in fullfile.readlines():
            line = self.clean_re.sub(" ", line)
            if lower:
                line = line.lower()
            if bigrams:
                self.compute_bigrams(line, sts, stopwords)
            sts['nlines'] = sts['nlines']+1
            for word in line.split():
                sts['nwords'] = sts['nwords']+1
                if word not in stopwords:
                    count = 1 if word not in sts['word'] else sts['word'][word]+1
                    sts['word'][word] = count
                    for i in range(len(word)):
                        # Guarda en prefix y suffix los prefijos y sufijos de entre 2 y 4 caracteres
                        if i >= 2 and i <= 4 and i < len(word):
                            pref = word[0:i]+'-'
                            suf = '-'+word[-i:]
                            countPref = 1 if pref not in sts['prefix'] else sts['prefix'][pref]+1
                            countSuf = 1 if suf not in sts['suffix'] else sts['suffix'][suf]+1
                            sts['prefix'][pref] = countPref
                            sts['suffix'][suf] = countSuf
                        char = word[i]
                        countS = 1 if char not in sts['symbol'] else sts['symbol'][char]+1
                        sts['symbol'][char] = countS
        filename, ext0 = os.path.splitext(fullfilename)
        add = ""
        # obtenemos las siglas que se deben añadir al nombre del nuevo archivo
        if lower or bigrams or full or stopwordsfile is not None:
            add = add+"_"
            if lower:
                add = add+'l'
            if stopwordsfile is not None:
                add = add+'s'
            if bigrams:
                add = add+'b'
            if full:
                add = add+'f'
        add = add+"_stats"
        new_filename = filename+add+ext0
        self.write_stats(new_filename, sts, stopwordsfile is not None, full)

    def compute_bigrams(self, line: str, stats: dict, stopwords: list):
        """
        Este método procesa una linea del texto y guarda en stats los parámetros 
        relacionados con los bigramas, en este caso biwords and bisymbols

        :param 
            line: linea a procesar
            stats: las estadísticas del texto.
            stopwords: lista de stopwords
        """
        # añadimos '$' al principio y al final de la frase si no es una linea en blanco
        bigramLine = '$ '+line+' $' if line.strip() else line
        words = bigramLine.split()
        for i in range(len(words)-1):
            word = words[i]
            if word not in stopwords:
                if word != '$':
                    j = 0
                    # obtenemos y guardamos todos los pares de simbolos de cada palabra
                    while j < len(word)-1:
                        pairLetter = word[j]+word[j+1]
                        count = 1 if pairLetter not in stats['bisymbol'] else stats['bisymbol'][pairLetter]+1
                        stats['bisymbol'][pairLetter] = count
                        j += 1
                # si la siguiente palabra tampoco es una stopword se añade el bigrama
                if words[i+1] not in stopwords:
                    biW = word+" "+words[i+1]
                    count = 1 if biW not in stats['biword'] else stats['biword'][biW]+1
                    stats['biword'][biW] = count

    def compute_files(self, filenames: str, **args):
        """
        Este método calcula las estadísticas de una lista de ficheros de texto

        :param 
            filenames: lista con los nombre de los ficheros.
            args: argumentos que se pasan a "file_stats".

        :return: None
        """

        for filename in filenames:
            self.file_stats(filename, **args)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Compute some statistics from text files.')
    parser.add_argument('file', metavar='file', type=str, nargs='+',
                        help='text file.')

    parser.add_argument('-l', '--lower', dest='lower',
                        action='store_true', default=False,
                        help='lowercase all words before computing stats.')

    parser.add_argument('-s', '--stop', dest='stopwords', action='store',
                        help='filename with the stopwords.')

    parser.add_argument('-b', '--bigram', dest='bigram',
                        action='store_true', default=False,
                        help='compute bigram stats.')

    parser.add_argument('-f', '--full', dest='full',
                        action='store_true', default=False,
                        help='show full stats.')

    args = parser.parse_args()
    wc = WordCounter()
    wc.compute_files(args.file,
                     lower=args.lower,
                     stopwordsfile=args.stopwords,
                     bigrams=args.bigram,
                     full=args.full)
