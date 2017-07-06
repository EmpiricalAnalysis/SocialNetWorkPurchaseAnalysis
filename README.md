# Analysis of Social Network's Purchases

This project identifies anomalies in a social network's purchasing trend, where a user's purchase amount is considered anomalous if it's more than 3 standard deviations from the mean of the last `T` purchases in the user's `D`-degree social network. Here, `D` stands for the number of degrees that defines a user's social network, and `T` stands for the number of consecutive purchases made by a user's social network (not including the user's own purchases).

The solution is implemented in python. It creates a network of users, each of whom keeps track of his/her friends and purchases. The network of friends and purchases made by friends are updated every time two users befriend/unfriend each other or if a user makes a purchase.


## Required Python Packages
The solution runs on Python 2.7.11 and requires the following python packages:
* numpy
* collections
* sys
* json


## Run Instructions
To run the code, enter the following to the command line:
`./run.sh`
