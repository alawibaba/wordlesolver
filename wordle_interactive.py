#!/usr/bin/env python3

from math import log
from collections import defaultdict
from tqdm import tqdm
from joblib import Parallel, delayed
import json

LENGTH = 5
PROCESSES = 36
lowercase = 'abcdefghijklmnopqrstuvwxyz'
CACHE_FILE = "wordle.cache"

def goodWords(raw_words):
    """
    Returns a list of words that are of the correct length and only contain
    lowercase letters. The current word lists already have this property,
    but this enables you to replace it with your own word list.
    """
    words = []
    for raw_word in raw_words:
        word = raw_word.strip()
        if len(word) != LENGTH:
            continue
        bad_word = False
        for c in word:
            if c not in lowercase:
                bad_word = True
                break
        if bad_word:
            continue
        words.append(word)
    return words

guess_words = goodWords(open("wordList"))
answer_words = goodWords(open("answerList"))

def postState(truth, guess, old_state, old_constraints):
    new_state = [set(old_state_spot) for old_state_spot in old_state]
    remainingLettersTruth = {c: 0 for c in lowercase}
    remainingLettersGuess = {c: 0 for c in lowercase}
    matchCounts = {c: 0 for c in lowercase}
    unmatched = LENGTH
    for i in range(LENGTH):
        if truth[i] == guess[i]:
            new_state[i] = set([guess[i]])
            matchCounts[guess[i]] += 1
            unmatched -= 1
        else:
            remainingLettersTruth[truth[i]] += 1
            remainingLettersGuess[guess[i]] += 1
            try:
                new_state[i].remove(guess[i])
            except KeyError:
                pass

    new_constraints = {}
    for c in lowercase:
        old_min, old_max = old_constraints[c]
        if remainingLettersTruth[c] >= remainingLettersGuess[c]:
            new_constraints[c] = (max(remainingLettersGuess[c] + matchCounts[c], old_min),
                    min(LENGTH + matchCounts[c], old_max))
        else:
            old_min, old_max = old_constraints[c]
            new_constraints[c] = (matchCounts[c] + remainingLettersTruth[c], matchCounts[c] + remainingLettersTruth[c])

    return new_state, new_constraints

def match(truth, state, constraints):
    counts = {c: 0 for c in lowercase}
    for i in range(LENGTH):
        if truth[i] not in state[i]:
            return False
        counts[truth[i]] += 1
    for c in lowercase:
        cmin, cmax = constraints[c]
        if counts[c] < cmin or counts[c] > cmax:
            return False
    return True

def serialize(state, constraints):
    return ",".join(["".join(sorted(list(state_spot))) for state_spot in state]) + ":" + ",".join(["(%d, %d)" % constraints[c] for c in lowercase])

def entropy(guess, candidates, old_state, old_constraints):
    total = 0
    count = defaultdict(lambda: 0)
    for candidate in candidates:
        count[serialize(*postState(candidate, guess, old_state, old_constraints))] += 1
        total += 1
    score = 0
    for pnum in count.values():
        p = pnum / total
        score -= p * log(p)
    return score, guess

if __name__ == '__main__':
    old_state = [set(lowercase) for _ in range(LENGTH)]
    old_constraints = {c: (0, LENGTH) for c in lowercase}

    try:
        cache = json.load(open(CACHE_FILE, 'r'))
        hardMode = True
        stateKey = ''
        while True:
            if stateKey in cache:
                bestword = cache[stateKey]
            else:
                candidates = set([])
                for word in answer_words:
                    if not match(word, old_state, old_constraints):
                        continue
                    candidates.add(word)
                    print(word)

                if len(candidates) == 0:
                    print("No candidates left! ABORT!")
                    break

                if hardMode:
                    new_guess_words = set()
                    for word in guess_words:
                        if not match(word, old_state, old_constraints):
                            continue
                        new_guess_words.add(word)
                    guess_words = new_guess_words

                # find the word that gives the best entropy --- parallelized with joblib!
                bestscore, bestword = max(Parallel(n_jobs=PROCESSES)(delayed(entropy)(word, candidates, old_state, old_constraints) for word in tqdm(guess_words)))

                if len(candidates) == 1:
                    print("The answer is ", candidates.pop())
                    break

                cache[stateKey] = bestword

            response = input("Please guess '%s' and enter the response: " % bestword).strip()

            if len(response.split()) == 2:
                guess, response = response.split()
            else:
                guess = bestword

            stateKey = stateKey + guess.lower() + response

            wrongSpotCounts = {c: 0 for c in lowercase}
            wrongLetterCounts = {c: 0 for c in lowercase}
            matchCounts = {c: 0 for c in lowercase}
            unmatched = LENGTH
            for i in range(LENGTH):
                if response[i] == '0':
                    try:
                        old_state[i].remove(guess[i])
                    except KeyError:
                        pass
                    wrongLetterCounts[guess[i]] += 1
                elif response[i] == '1':
                    try:
                        old_state[i].remove(guess[i])
                    except KeyError:
                        pass
                    wrongSpotCounts[guess[i]] += 1
                else:
                    old_state[i] = set([guess[i]])
                    matchCounts[guess[i]] += 1
                    unmatched -= 1
            for c in lowercase:
                old_min, old_max = old_constraints[c]
                if wrongLetterCounts[c] > 0:
                    old_constraints[c] = (matchCounts[c] + wrongSpotCounts[c], matchCounts[c] + wrongSpotCounts[c])
                else:
                    old_constraints[c] = (max(old_min, matchCounts[c] + wrongSpotCounts[c]), min(old_max, matchCounts[c] + wrongSpotCounts[c] + unmatched))
        print()
    finally:
        # update the cache
        json.dump(cache, open(CACHE_FILE, 'w'))
