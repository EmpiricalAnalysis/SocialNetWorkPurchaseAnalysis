# Analysis of Social Network's Purchases

This project identifies anomalies in a social network's purchasing trend, where a user's purchase amount is considered anomalous if it's more than 3 standard deviations from the mean of the last `T` purchases in the user's `D`-degree social network. Here, `D` stands for the number of degrees that defines a user's social network, and `T` stands for the number of consecutive purchases made by a user's social network (not including the user's own purchases).

The solution is implemented in python. It creates a network of users, each of whom keeps track of his/her first-degree friends and his/her purchases. The list of friends and the list of purchases made by friends are generated as needed. This means that they get updated every time the user's social network gets modified or if one of the friends made a purchase.


## Required Python Packages
The solution requires python packages:
* numpy
* collections
* sys
* json


## Run Instructions
To run the code, enter the following to the command line:
`./run.sh`
