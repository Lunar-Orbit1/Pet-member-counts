import requests
def RecurseGroupMembersByRoleWithCursor(id:int, roleid:int, cursor:str, members:list=[], toreturn:bool=True):
    tr = members
    url =f"https://groups.roblox.com/v1/groups/{str(id)}/roles/{str(roleid)}/users?limit=100&sortOrder=Asc&cursor={cursor}"
    request = requests.get(url)
    if request.status_code == 200:
        requestJson = request.json()
        for x in requestJson['data']:
            tr.append(x['userId'])

        # problem child


        if requestJson['nextPageCursor'] != None:
            return RecurseGroupMembersByRoleWithCursor(id, roleid, requestJson['nextPageCursor'], tr)
        
        else:
            return tr
            

    else:
        print(request.status_code)
        print(request.json())
        return []

def GetGroupMembersByRole(id:int, roleid:int):
    memberuids = []
    url = f"https://groups.roblox.com/v1/groups/{str(id)}/roles/{str(roleid)}/users?limit=100&sortOrder=Asc"
    request = requests.get(url)
    if request.status_code == 200:
        requestJson = request.json()
        for x in requestJson['data']:
            memberuids.append(x['userId'])
        if requestJson['nextPageCursor'] != None:
            #There is another page, recurse
            recursed = RecurseGroupMembersByRoleWithCursor(id, roleid,requestJson['nextPageCursor'])
            for v in recursed:
                memberuids.append(v)
    else:
        print(request.status_code)
        print(request.json())
        return []
    return memberuids

def GetGroupMembercount(id:int):
    url = f"https://groups.roblox.com/v1/groups/{str(id)}"
    request = requests.get(url)
    if request.status_code == 200:
        return request.json()['memberCount']
    
def GetRoleMembercount(id:int,roleid:int, memberlist:list=[]):
    if len(memberlist) <= 0:
        return len(GetGroupMembersByRole(id, roleid))
    else:
        return len(memberlist)

def getUserRoleInGroup(groupId: int, userId: int):
    url = f"https://groups.roblox.com/v2/users/{str(userId)}/groups/roles?includeLocked=false"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()['data']
        for i, group in enumerate(data):
            if group['group']['id']==groupId:
                return group['role']['name']
    else:
        print(res.json())
    return False

def getThumbnailUrl(uid:int):
    url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={str(uid)}&size=150x150&format=Png&isCircular=false"
    request = requests.get(url)
    if request.status_code == 200:
        return request.json()['data'][0]['imageUrl']            
        
def getNameFromUid(uid:int):
    request = requests.get(f"https://users.roblox.com/v1/users/{str(uid)}")
    if request.status_code == 200:
        return request.json()['name']


#print(len(GetGroupMembersByRole(2593707,17183357)))
# print(GetRoleMembercount(2593707, 17183357))