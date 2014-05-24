#! /usr/bin/ python

import math, itertools, re
from operator import mul
from collections import defaultdict

def encode(text, decode=False):
    "Credit for this strategy goes to http://stackoverflow.com/a/16872684"  
    table = {'a':2, 'b':3, 'c':5, 'd':7, 'e':11, 'f':13, 'g':17, 'h':19, 
    'i':23, 'j':29, 'k':31, 'l':37, 'm':41, 'n':43,'o':47, 'p':53, 'q':59, 
    'r':61, 's':67, 't':71, 'u':73, 'v':79, 'w':83, 'x':89, 'y':97, 'z':101}  
    if not decode: 
        return reduce(mul,[table[char] for char in text]) if text else ''

class Prdist(dict):
    """Return a probability distribution of a lexicon. A word's raw 
    probability score can be called from Prdist(word). Format is:
    {<word>: [raw_probability, prime_encoding]}"""

    def __init__(self, text):
        for word, score in text:
            self[word] = [int(score), encode(word)] 
        self.N = float(sum([self[word][0] for word in self.iterkeys()]))
    def encoded(self, word):
        return self[word][1]

def datafile(filename, sep='\t'):
    """Generate a tuple of word, count from each line in a textfile.
       For use when building a Prdist."""
    for line in open(filename):
        yield line.split(sep)

NWORDS = Prdist(datafile('newwords.txt'))

def n_choose_k(n, k):
    return math.factorial(n) \
           / float(math.factorial(n - k) * math.factorial(k))

def weighted_Pr(word, n, NWORDS=NWORDS):
    "Calculate prior probability and give greater weight to longer words"
    k = len(word)
    prior_probability = NWORDS[word][0] / NWORDS.N
    return prior_probability / (n_choose_k(n, k) * 26**(n-k))
    
             
def get_candidates(code, lexicon=NWORDS):
    """Return a list of all words found in input string."""
    if type(code) == str: 
         code = encode(code)
    return [word for word in lexicon if code % NWORDS.encoded(word) == 0]

def generate_anagrams(code, candidates, sort_test=weighted_Pr):
    "Return a generator which spits anagram lists."
    stack = []
    candidates = sorted(candidates, key = lambda x: sort_test(x, len(code)))
    if type(code) == str: code = encode(''.join(re.findall('[a-z]+', code)))
    while candidates:
        branch = candidates.pop()
        stack.append((branch, code/NWORDS.encoded(branch), 
                     get_candidates(code/NWORDS.encoded(branch), candidates)))
        while stack:
            leaf, leaf_code, leaf_candidates = stack[-1]
            # Success - a full anagram!
            if leaf_code == 1: 
                stack.pop() 
                yield [word[0] for word in stack] + [leaf] 
            # Failures: drop leaf from branch. Continue one level back.
            elif not leaf_candidates: stack.pop() #old: continue
            # Partial Success: Continue branch. 
            else:
                next = leaf_candidates.pop()
                stack.append((next, leaf_code/NWORDS.encoded(next), 
                             get_candidates(leaf_code/NWORDS.encoded(next), 
                             leaf_candidates)))
                continue    

def build_candidates(input_string, lexicon=NWORDS):
    code = encode(''.join(re.findall('[a-z]+', input_string.lower())))
    d = {}
    for word in lexicon:
        _code = lexicon.encoded(word)
        if code % _code == 0: 
            d[word] = lexicon[word]
    return d

def score_anagram(words, length=50):
    m = map(lambda x: weighted_Pr(x, length), words)
    return reduce(lambda x, y: x+y, m)

def score(words):
    "Don't count small, common words."
    m = map(lambda x: NWORDS[x][0] / NWORDS.N if len(x) > 3 else 0, words)
    return reduce(lambda x, y: x+y, m)

"""
TODO

def score(words, lexicon=NWORDS):
    return sum([lexicon[word][0] for word in words])

P2 = defaultdict(lambda: 0)
for key, val in datafile('count_2w.txt'):
    P2[key] = int(val)

P2_N = float(sum(P2.values()))

def sort_anagram(words, func=None, lookup=P2):
    start = '<S> '
    scores = {start+word: lookup[start+word]/P2_N for word in words}
    for bigram in itertools.permutations(words, 2):
        score = lookup[' '.join(bigram)] / P2_N
        scores[' '.join(bigram)] = score 
    return scores

"""
    
"""
A running sum based on permutations as whole strings: lookup(' '.join(i, i+1))"""
    
  




"""
Possible states after receiving a particular input:

1. Total Success: Add anagram to sucesses; back up one level on stack and continue (L*, A2)
2. Partial Success: add self less next to stack; continue with next (L2, A1)
3. Failure for not matching: remove self from stack; back up one level and continue (L1, A1)
4. Failure for end-of-line with remainder: back up one level and continue (L1, A1)

Possible states for an input list (L):
1. empty
2. contains elements

Possible states for an anagram code (A):
1. > 1
2. == 1

"""
