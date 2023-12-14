import requests, roblox, database
groupid = 2593707

rolesets = {
    "TR": {
        "name": "Trained Respondent",
        "id": 17183355,
        "count": 0,
    },
    "DR":{
        "name": "Dedicated Respondent",
        "id": 17183357,
        "count":0,
    },
    "ER":{
        "name": "Elite Respondent",
        "id":17183356,
        "count": 0,
    },
    "MR":{
        "name": "Marshall",
        "id":68940287,
        "count": 0,
    },
    "SP":{
        "name": "Specialist",
        "id":38168385,
        "count":0,
    },
    "CHEIF":{
        "name": "Cheif",
        "id":17179389,
        "count":0
    },
}




def checkForDifferences():
    data = database.readDB("PET")
    if data is None:
        data = rolesets
    for i,x in enumerate(rolesets):
        # Get the lists for the roles, check how many people are in it and compare to the db
        # if it's the same, delete the data and move on
        # else handle the promotion and save the data
        print(rolesets[x])
        memberList = roblox.GetGroupMembersByRole(groupid, rolesets[x]['id'])
        oldData = data[x]
        if oldData['count'] != len(memberList):
            # Discrepancy detected, loop through both lists and see what's changed
            print("Yay")
        else:
            print("Nyooo")


checkForDifferences()