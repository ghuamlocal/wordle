from argparse import ArgumentParser
from copy import deepcopy
from json import load, dump
import os.path
import pprint
import re
from typing import List, Dict, Tuple


def create_histogram(histogram: Dict[str, int], total: int) -> List[Tuple[str, float]]:
    return sorted(list(map(lambda item: (item[0], (float(item[1]) / float(total)) * 100),
                           histogram.items())),
                  key=lambda item: item[1], reverse=True)


def export_5_letter_words_histogram(words: List[str]):
    starting_letter_histogram: Dict[str, int] = {letter: 0 for letter in 'abcdefghijklmnopqrstuvwxyz'}
    histogram: Dict[str, int] = deepcopy(starting_letter_histogram)
    for word in words:
        try:
            starting_letter_histogram[word[0]] += 1
            for letter in word:
                histogram[letter] += 1
        except KeyError:
            continue
    starting_letter_histogram: List[Tuple[str, float]] = create_histogram(starting_letter_histogram, len(words))
    histogram: List[Tuple[str, float]] = create_histogram(histogram, sum(histogram.values()))
    with open('starting_letter_histogram.json', 'a+t') as f3:
        dump(starting_letter_histogram, f3)
    with open('histogram.json', 'a+t') as f4:
        dump(histogram, f4)


def pattern_match(words, args):
    pattern = ''.join(args.pattern[:5])
    pattern = re.compile(pattern)
    matched_words = [[word] for word in words if (re.match(pattern, word) and
                                                  (len(args.pattern) != 6 or
                                                   all([letter in word for letter in args.pattern[5]])))]
    if os.path.exists('histogram.json'):
        with open('histogram.json') as f6:
            histogram = dict(load(f6))
        for item in matched_words:
            item.append(sum([histogram[letter] for letter in item[0]]))
    matched_words = sorted(matched_words, key=lambda item: item[1], reverse=True)
    pprint.pprint(matched_words, compact=False)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--histogram')
    parser.add_argument('--pattern', nargs='+', action='extend', type=str)
    if not os.path.exists('five_letter_words.json'):
        with open('dictionary.json') as f1:
            words_def_map: Dict[str, str] = load(f1)
        words: List[str] = sorted([word for word in words_def_map.keys() if len(word) == 5 and '-' not in word
                                   and ' ' not in word])
        with open('five_letter_words.json', 'a+t') as f2:
            dump(words, f2)
    else:
        with open('five_letter_words.json') as f5:
            words: List[str] = load(f5)
    args = parser.parse_args()
    if args.histogram:
        export_5_letter_words_histogram(words)
    elif args.pattern:
        pattern_match(words, args)
