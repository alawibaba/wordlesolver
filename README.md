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
