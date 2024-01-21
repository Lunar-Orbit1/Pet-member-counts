import requests, roblox, database,os,datetime, time
from dotenv import load_dotenv

load_dotenv()
groupid = 2593707

rolesets = {
    "ER":{
        "name": "Elite Respondent",
        "id":17183356,
        "rank": 0, #Arbitrary number
    },
    "MR":{
        "name": "Marshall",
        "id":68940287,
        "rank": 1, #Arbitrary number
    },
    "SP":{
        "name": "Specialist",
        "id":38168385,
        "rank": 2, #Arbitrary number
    },
    "CHIEF":{
        "name": "Chief",
        "id":17179389,
        "rank": 69, #Arbitrary number
    },
}
def checkKey(dic, key):
    if key in dic.keys():
        return True
    else:
        return False
    
def startGossip(uid: int, message:str):
    # Sends notifications/messages via https about someone's rank
    print("Starting gossip.. ooh!!!")
    webhookurl = os.getenv("WEBHOOK_URL")
    name = roblox.getNameFromUid(uid)
    thumbnailurl = roblox.getThumbnailUrl(uid)
    data = {
        "content": None,
        "embeds": [
            {
                "title": name,
                "description": f"""
{message}
""",
                "color": 16745298,
                "timestamp": str(datetime.datetime.fromtimestamp(time.time())),
                "image": {
                    "url": thumbnailurl
                }, 
                "footer": {
                "text": "Programmed by claym1x"
            }
            }
        ],
    }
    requests.post(webhookurl, json=data) #Discord webhook

def checkForDifferences():
    data = database.readDB("PET")
    if data is None:
        data = {}
    currentMembers = {}
    rankCounts = {
        'ER' : roblox.GetGroupMembersByRole(groupid, rolesets['ER']['id']),
        'MR' : roblox.GetGroupMembersByRole(groupid, rolesets['MR']['id']),
        'SP' : roblox.GetGroupMembersByRole(groupid, rolesets['SP']['id']),
        'CHIEF' :roblox.GetGroupMembersByRole(groupid, rolesets['CHIEF']['id']),
    }
    for role in rankCounts:
        for i,member in enumerate(rankCounts[role]):
            currentMembers[member] = role

    if len(currentMembers) != len(data):
        print(f"A difference of {str(len(currentMembers)-len(data))} detected")
        actions = {} #Members who changed, with human readable descriptions
        for uid in currentMembers:
            if not checkKey(data, uid):
                # The user was promoted from a LR rank
                actions[uid] = f"Promoted to {rolesets[currentMembers[uid]]['name']}"
            elif data[uid] != currentMembers[uid] and rolesets[currentMembers[uid]]['rank'] > rolesets[data[uid]]['rank']:
                #The user was promoted from an existing mr rank
                actions[uid] = f"Promoted to {rolesets[currentMembers[uid]]['name']} from {rolesets[data[uid]]['name']}"

        for uid in data:
            if not checkKey(currentMembers, uid):
                # User is no longer in an mr rank. Check if they left or were demoted.
                role = roblox.getUserRoleInGroup(groupid, uid)
                print(role)
                if role == False:
                    actions[uid] = f"Left the group from {rolesets[data[uid]]['name']}"
                else:
                    actions[uid] = f"Demoted to {role} from {rolesets[data[uid]]['name']}"
            elif data[uid] != currentMembers[uid] and checkKey(actions, uid) == False:
                # User got demoted to another mr rank
                actions[uid] = f"Demoted to {rolesets[currentMembers[uid]]['name']} from {rolesets[data[uid]]['name']}"

        database.writeDB("PET", currentMembers)
        print("Wrote difference to db")

    else:
        print("No difference detected")

    

startGossip(767877034, "**Claym1x** made a cool thing or smth idk")

#checkForDifferences()