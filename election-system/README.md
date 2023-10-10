# Election System

This is a tool built to help in the processing of secret ballots.

## Preferential Voting

The program given by `prefvoting.py` implements preferential, or instant-runoff voting. The program will need the ballots to be presented in csv format, of the form:
```
Candidate A, Candidate B, Candidate C, ...
1, 2, 3, ...
3, 1, 2, ...
...
```
The first row contains the list of candidates separated by commas. Every subsequent row is one ballot, with each value being the preference given to the respective candidate (for example, if a value of 1 is found in the third position in a row, it corresponds to first preference being given to the third candidate).

To run the program, the call will be:
`py prefvoting.py ballots.csv`
`py` is the python program call, may take on a different form depending on install. `ballots.csv` is the ballots to process.

The provided `sample-ballot.csv` corresponds to the following table:
| Ballot | Candidate A | Candidate B | Candidate C |
| 0 | 1 | 2 | 3 |
| 1 | 2 | 3 | 1 |
| 2 | 1 | 3 | 2 |
| 3 | 2 | 1 | 3 |
| 4 | 1 | 3 | 2 |
| 5 | 3 | 1 | 2 |

