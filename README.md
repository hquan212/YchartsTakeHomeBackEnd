# Ychart take home challenge 3

## Back-End challenge

In this challenge, I wrote the Reconciliation class which takes in the recon.in file, parses the instructions, performs
the transaction steps and then compares the output from the transactions vs the second days positions input.

This will perform the unit reconciliation that will display the differences between the two positions and whether or not
we need to go back and find out if we are missing input data.

to run type:

> make run

to run via python command line:
type:

> python3 src/main.py input/recon.in

## Assumptions

This project assumes that you can sell a stock that you do now own. _short shell_ the stock.
It also assumes that the data input will always have the same format.

To calculated reconciliation will be a file called recon.out under the output directory.
