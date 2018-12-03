# Decision Tree

This decision tree program uses a data set of 1000 different credit histories and a decision
if this particular person defaulted on their loan.

The program performs slightly better than guessing with a correct prediction rate of 63%. In this implementation
continuous data was handled by calculating midpoints of the data as well as quarterpoints which allowed continuous values
to be categorized. As the program worked through the tree creation it would set the decision of that branch to be unknown if
a possible answer was not found in the subtree. This unfortunately causes a loss of data that would have likely improved the
correct prediction rate.

To see an output of the tree, pull the repository down and run the program.