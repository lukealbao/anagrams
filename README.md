###ABOUT

Takes an input string of arbitrary length and word count and returns a list
of the "best" anagrams. "Best" is defined assuming an adversary who has
created the input string; the best would be the one such an adversary meant.


###TO DO

1. Compile bigram probability distribution. Use it to implement a 
   sort_anagram procedure.
2. Tests & error handling.
3. UI code.
4. Clean up Lexicon file:
   a. Remove obscure two-letter and three-letter words
   b. Cut down size to ~100k words.
   c. Add in common proper nouns.
5. Implement relevance graph and procedure for calculating best anagrams
   by relevance.
6. ~~Make generate_anagrams so that it need not take build_candidates as
   a parameter.~~


###USAGE

#### Within Python REPL
```python
cipher_text = 'The Owl of Gold'
anagrams = generate_anagrams(cipher_text, build_candidates(cipher_text))
top_5000 = sorted([next(anagrams) for i in range(5000)],
                  key=score, reverse=True)
```

#### From Command Line
```bash
$ python anagrams.py
>>> Input text: The Owl of Gold
>>> ...
>>> How many anagrams to return: 50
>>> ...
>>> followed goth
>>> ... etc
```