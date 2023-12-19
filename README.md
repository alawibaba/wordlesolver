# wordlesolver
My Greedy Wordle Solver

This is a really simple [wordle](https://www.powerlanguage.co.uk/wordle/) solver. It picks the guess that has the greatest impact on information contact assuming that a word was chosen at random from the wordList database (which was copied from wordle's source).

To enter the response from the game, enter as a five digit number, where 0 indicates a black square (no match), 1 indicates a yellow square (matching letter but not place), and 2 indicates a green square (matching letter and place).

Example session:

```
Please guess 'tares' and enter the response: 00100
Please guess 'bound' and enter the response: 00000
Please guess 'pilch' and enter the response: 21020
Please guess 'aback' and enter the response: 00022
The answer is  prick
```

This code is not fast.

The wordlist (list of permitted guesses) came from [here](https://gist.githubusercontent.com/cfreshman/d97dbe7004522f7bc52ed2a6e22e2c04/raw/633058e11743065ad2822e1d2e6505682a01a9e6/wordle-nyt-words-14855.txt).

The list of possible answers came from [here](https://gist.githubusercontent.com/cfreshman/a7b776506c73284511034e63af1017ee/raw/60531ab531c4db602dacaa4f6c0ebf2590b123da/wordle-nyt-answers-alphabetical.txt).
