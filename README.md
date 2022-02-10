# wordle
A Python script to help beat Wordle.

## Table of Contents:

1. `.gitignore` - a list of patterns for git to ignore.
2. `dictionary.json` - a master database of valid english words.
3. `filter_dictionary.py` - the main script powering this project. See usage below.
4. `five_letter_words.json` - a list of all valid 5 letter words.
5. `histogram.json` - a histogram indicating the frequency of occurrence of each letter in all english words.
6. `LICENSE`
7. `README`
8. `starting_letter_histogram.json` - a histogram indicating the frequency of occurence of each letter as the 1st 
   letter in all 5 letter words. Use this to guide your next guess.

## Usage - pattern matching

The `filter_dictionary.py` script relies on `dictionary.json`, `five_letter_words.json`, and `histogram.json` to 
suggest the next word to guess based guessed words.

1. Create a local virtual env with at least Python 3.8
2. Then inside the project directory:
   1. `python ./filter_dictionary.py --pattern <regex for 1st letter> <regex for 2nd letter> <regex for 3rd letter> 
      <regex for 4th letter> <regex for 5th letter> <known letters in the word>`

For example, if you have guessed the following 2 words:

RAISE

CLOUT

and Wordle tells you the following:

A - green

S - green

E - green

U - yellow

Then we know that the following letters do not exist in the word:

riclot

Therefore, you should pattern match like this:

`python ./filter_dictionary.py --pattern [^riclot] a [^riclot] s e u`

The output will be a list of words that match the pattern given, and contain the letters specified. The list is 
sorted in descending order of a probability heuristic, indicating the likelihood of that word being the correct one.

`[['pause', 34.07643312101911]]`

The number next to each word is a heuristic score indicating the probability of that being the correct word. It is 
currently calculated by summing up the probabilities of each letter in the word. Admittedly this is a simple 
heuristic, and will sometimes mean that rarely occurring words will be ranked higher than more commonly occurring 
words. But for the most part it will give you a pretty good idea about what to guess next.

You should also refer to `starting_letter_histogram.json`, which lists, in descending order, the frequency in 
percentages, of each letter as the starting letter of all 5 letter words.

## Disclaimer

The script suggests words based on the master `dictionary.json`, which is admittedly not complete. Even though it 
contains thousands of words, there could be some missing. Therefore use this at your own risk, or better yet, should 
you find a word is missing, then please add it to `dictionary.json` and regenerate the histograms.

## Usage - histogram generation

If you happen to find a missing word, and want to extend `dictionary.json`, then please do so, and submit a pull 
request. Please also regenerate the other JSON files by executing the following command:

`python ./filter_dictionary.py --histogram`

## Improvements

1. Improve the heuristic.
1. Extend the `dictionary.json`.
