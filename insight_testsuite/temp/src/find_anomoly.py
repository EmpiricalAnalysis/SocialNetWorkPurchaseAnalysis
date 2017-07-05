import numpy as np
from collections import deque
from collections import OrderedDict
import sys, json


class user(object):
    """
    Define the user class, where each user has the properties of first-degree
    friends and purchases made by the user (with timestamps).
    """
    def __init__(self, uid, D, T):
        """
        Initialize a user with:
        id: user's id
        friends list: keep track of first-degree friends;
        purchase history of friends: implemented by a queue containing dollar
            amount of purchase.
        """
        self.id = uid
        self.networkDegree = D
        self.maxNumPurchase = T
        self.friendsID={}   # key: friend's id, value: 1
        self.ownPurchaseHistory={} # key: timestamp, value: amount


    def getFriendsList(self):
        # this function returns a list of all friends within user's social network
        listOfFriends = []
        stack = deque()
        iDeg = 1
        # set initial state of stack of friends
        for friend in self.friendsID.keys():
            listOfFriends.append(friend)
            stack.append(friend)
        iDeg += 1
        while iDeg <= self.networkDegree:
            iFriend = 0
            nFriendsAtDeg = len(stack)
            while len(stack) != 0 and iFriend < nFriendsAtDeg:
                aFriendName = stack.popleft()
                iFriend += 1
                for friend in users[aFriendName].friendsID.keys():
                    if friend != self.id and friend not in listOfFriends:
                        listOfFriends.append(friend)
                        stack.append(friend)
            iDeg += 1
        return listOfFriends


    def __str__(self):    
        listOfFriends = self.getFriendsList()
        n_friends = len(listOfFriends)
        lstOfPurchase = ["%.2f" % self.ownPurchaseHistory[v] for v in self.ownPurchaseHistory]

        return "user %s has %d friends \nThey are users %s \nFriends of user %s made purchases %s" % (self.id, n_friends, listOfFriends, self.id, lstOfPurchase)


    def beFriend(self, j):
        """
        Add user j to user's friends list,
        add current user to j's friends list
        """
        self.friendsID[j.id] = 1
        j.friendsID[self.id] = 1


    def unFriend(self, j):
        """
        remove user j from self's friends' list
        remove self from user j's friends' list
        """
        try:
            del self.friendsID[j.id]
        except KeyError:
            pass

        try:
            del j.friendsID[self.id]
        except KeyError:
            pass


    def purchase_batch(self, amount, idx):
        # here we create the initial state of the purchase history, add timestamp and amount to user's ownPurchaseHistory
        self.ownPurchaseHistory[idx] = amount


    def purchase(self, amount, timestamp, idx):
        # here we update the state of user's purchase history, add timestamp and amount to user's ownPurchaseHistory
        self.ownPurchaseHistory[idx] = amount
        
        # in the following, we check if the current purchase amount is anomolous
        # first generate an updated list of friends, then we will create an updated list of friendly purchases, which 
        # will be used to determine the existance of anomoly
        isAnomalous = None
        
        listOfFriends = self.getFriendsList()

        # Is the purchase amount anomoly among the social network? 
        # First, let's gather all purchases by the user's social network
        allFriendsPurchaseHistory = {}
        for friendName in listOfFriends:
            allFriendsPurchaseHistory.update(users[friendName].ownPurchaseHistory)
        if len(allFriendsPurchaseHistory) >= 2: 
            # if there are at least 2 purchases within the social network, select the last T purchases by
            sortedTimestamp = sorted(allFriendsPurchaseHistory.keys(), reverse=True)
            if len(sortedTimestamp) > self.maxNumPurchase:
                relevantTimestamp = sortedTimestamp[0: self.maxNumPurchase]
            else:
                relevantTimestamp = sortedTimestamp
            lastTPurchases = [allFriendsPurchaseHistory[i] for i in relevantTimestamp]
            # calculate mean and standard deviation of network's last T purchases
            meanPurchases = np.mean(lastTPurchases)
            stdPurchases = np.std(lastTPurchases)
            if amount > meanPurchases + 3 * stdPurchases:
                meanPurchasesSTR = str("%0.2f" % meanPurchases)
                stdPurchasesSTR = str("%0.2f" % stdPurchases)
                isAnomalous = OrderedDict([("event_type","purchase"), ("timestamp",timestamp), ("id",self.id), ("amount",str(amount)), ("mean",meanPurchasesSTR), ("sd",stdPurchasesSTR)])
        return isAnomalous



'''
# TEST case 1
users = {}
users["1"] = user("1", 2, 5)
users["2"] = user("2", 2, 5)
users["3"] = user("3", 2, 5)
#print(users["2"])    # expect user 2 to have no friends at this moment
#print("-----------------------")
users["1"].beFriend(users["2"])
users["1"].beFriend(users["3"])

#print(users["1"])    # expect user 1 to have 2 friends, user 2 (degree 1) and user 3 (degree 1)
#print("-----------------------")
#print(users["2"])    # expect user 2 to have 2 friends, user 1 (degree 1) and user 3 (degree 2)
#print("-----------------------")
#print(users["3"])    # expect user 3 to have 2 friends, user 1 (degree 2) and user 2 (degree 1)
#print("#########################################")


# TEST case 2
users["4"] = user("4", 2, 5)
users["5"] = user("5", 2, 5)
users["6"] = user("6", 2, 5)
users["4"].beFriend(users["2"])
users["4"].beFriend(users["5"])
users["5"].beFriend(users["2"])
users["3"].beFriend(users["5"])
users["6"].beFriend(users["5"])

#print(users["1"])    # expect user 1 to have 4 friends, users 2, 3, 4, 5
#print("-----------------------")
#print(users["2"])    # expect user 2 to have 5 friends, users 1, 4, 5, 3, 6
#print("-----------------------")
#print(users["3"])    # expect user 3 to have 5 friends, users 1, 5, 2, 4, 6
#print("-----------------------")
#print(users["4"])    # expect user 1 to have 5 friends, users 2, 5, 1, 3, 6
#print("-----------------------")
#print(users["5"])    # expect user 2 to have 5 friends, users 2, 3, 4, 6, 1
#print("-----------------------")
#print(users["6"])    # expect user 3 to have 4 friends, users 5, 3, 2, 4
#print("#########################################")

# TEST case 3
users["5"] .unFriend(users["2"])

print(users["1"])    # expect user 1 to have 4 friends, users 2, 3, 5, 4
print("-----------------------")
print(users["2"])    # expect user 2 to have 4 friends, users 1, 4, 3, 5
print("-----------------------")
print(users["3"])    # expect user 3 to have 5 friends, users 1, 5, 2, 4, 6
print("-----------------------")
print(users["4"])    # expect user 1 to have 5 friends, users 2, 5, 1, 3, 6
print("-----------------------")
print(users["5"])    # expect user 2 to have 5 friends, users 3, 4, 6, 1, 2
print("-----------------------")
print(users["6"])    # expect user 3 to have 3 friends, users 5, 3, 4
'''


'''
# TEST case 4
users = {}
users["1"] = user("1", 3, 5)
users["2"] = user("2", 3, 5)
users["3"] = user("3", 3, 5)
users["1"].beFriend(users["2"])
users["1"].beFriend(users["3"])
users["4"] = user("4", 3, 5)
users["5"] = user("5", 3, 5)
users["6"] = user("6", 3, 5)
users["4"].beFriend(users["2"])
users["4"].beFriend(users["5"])
users["5"].beFriend(users["2"])
users["3"].beFriend(users["5"])
users["6"].beFriend(users["5"])
users["5"].unFriend(users["2"])

print(users["1"])    # expect user 1 to have 5 friends, users 2, 3, 5, 4, 6
print("-----------------------")
print(users["2"])    # expect user 2 to have 5 friends, users 1, 4, 3, 5, 6
print("-----------------------")
print(users["3"])    # expect user 3 to have 5 friends, users 1, 5, 2, 4, 6
print("-----------------------")
print(users["4"])    # expect user 1 to have 5 friends, users 2, 5, 1, 3, 6
print("-----------------------")
print(users["5"])    # expect user 2 to have 5 friends, users 3, 4, 6, 1, 2
print("-----------------------")
print(users["6"])    # expect user 3 to have 5 friends, users 5, 3, 4, 1, 2
'''

'''
# TEST case 5
users = {}
users["1"] = user("1", 2, 5)
users["2"] = user("2", 2, 5)
users["3"] = user("3", 2, 5)
users["1"].beFriend(users["2"])
users["1"].beFriend(users["3"])
users["4"] = user("4", 2, 5)
users["5"] = user("5", 2, 5)
users["6"] = user("6", 2, 5)
users["4"].beFriend(users["2"])
users["4"].beFriend(users["5"])
users["5"].beFriend(users["2"])
users["3"].beFriend(users["5"])
users["6"].beFriend(users["5"])
users["5"].unFriend(users["2"])

users["1"].purchase_batch(5, "time")
users["2"].purchase_batch(1, "time")
users["3"].purchase(2, "time", 1)
users["4"].purchase(3, "time", 1)
users["5"].purchase(15, "time", 1)

print(users["1"])    # expect user 1 to have 4 friends, users 2, 3, 5, 4
print("-----------------------")
print(users["2"])    # expect user 2 to have 4 friends, users 1, 4, 3, 5
print("-----------------------")
print(users["3"])    # expect user 3 to have 5 friends, users 1, 5, 2, 4, 6
print("-----------------------")
print(users["4"])    # expect user 1 to have 5 friends, users 2, 5, 1, 3, 6
print("-----------------------")
print(users["5"])    # expect user 2 to have 5 friends, users 3, 4, 6, 1, 2
print("-----------------------")
print(users["6"])    # expect user 3 to have 3 friends, users 5, 3, 4
'''


batch_log_path = sys.argv[1]    
stream_log_path = sys.argv[2]   
flagged_purchases_path = sys.argv[3]   


# process batch log

with open(batch_log_path) as batch:
    flag = 0
    for line in batch:
        if line != "\n":
            j_content = json.loads(line)
            if flag == 0:
                degNetwork = int(j_content['D'])
                TPurchases = int(j_content['T'])
                users = {}
                flag = 1
                purchaseIdx = 0
            else:
                if j_content['event_type'] == "purchase":
                    # check if user record exists, if not create record
                    if str(j_content['id']) not in users:
                        users[str(j_content['id'])] = user(str(j_content['id']), degNetwork, TPurchases)
                    users[str(j_content['id'])].purchase_batch(float(j_content['amount']), purchaseIdx)
                    purchaseIdx += 1
                if j_content['event_type'] == "befriend":
                    # if if both users' records exist, if not create records
                    if str(j_content['id1']) not in users:
                        users[str(j_content['id1'])] = user(str(j_content['id1']), degNetwork, TPurchases)
                    if j_content['id2'] not in users:
                        users[str(j_content['id2'])] = user(str(j_content['id2']), degNetwork, TPurchases)
                    users[str(j_content['id1'])].beFriend(users[str(j_content['id2'])])
                if j_content['event_type'] == "unfriend":
                    # if if both users' records exist, if not create records
                    if str(j_content['id1']) not in users:
                        users[str(j_content['id1'])] = user(str(j_content['id1']), degNetwork, TPurchases)
                    if j_content['id2'] not in users:
                        users[str(j_content['id2'])] = user(str(j_content['id2']), degNetwork, TPurchases)
                    users[str(j_content['id1'])].unFriend(users[str(j_content['id2'])])
batch.close()


# process stream log
with open(flagged_purchases_path, 'w') as outFile:
    with open(stream_log_path) as stream:
        for line in stream:
            if line != "\n":
                j_content = json.loads(line)
                if j_content['event_type'] == "purchase":
                    # check if user record exists, if not create record
                    if str(j_content['id']) not in users:
                        users[str(j_content['id'])] = user(str(j_content['id']), degNetwork, TPurchases)
                    # record purchase
                    isAnomalous = users[str(j_content['id'])].purchase(float(j_content['amount']), str(j_content['timestamp']), purchaseIdx)
                    purchaseIdx += 1
                    if isAnomalous != None:
                        outFile.write(json.dumps(isAnomalous))
                        outFile.write('\n')
                if j_content['event_type'] == "befriend":
                    # if if both users' records exist, if not create records
                    if str(j_content['id1']) not in users:
                        users[str(j_content['id1'])] = user(str(j_content['id1']), degNetwork, TPurchases)
                    if j_content['id2'] not in users:
                        users[str(j_content['id2'])] = user(str(j_content['id2']), degNetwork, TPurchases)
                    users[str(j_content['id1'])].beFriend(users[str(j_content['id2'])])
                if j_content['event_type'] == "unfriend":
                    # if if both users' records exist, if not create records
                    if str(j_content['id1']) not in users:
                        users[str(j_content['id1'])] = user(str(j_content['id1']), degNetwork, TPurchases)
                    if j_content['id2'] not in users:
                        users[str(j_content['id2'])] = user(str(j_content['id2']), degNetwork, TPurchases)
                    users[str(j_content['id1'])].unFriend(users[str(j_content['id2'])])
    stream.close()
outFile.close()

    
