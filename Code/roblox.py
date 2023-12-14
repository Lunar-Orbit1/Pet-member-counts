import requests
def RecurseGroupMembersByRoleWithCursor(id:int, roleid:int, cursor:str, members:list=[], toreturn:bool=True):
    tr = members
    url =f"https://groups.roblox.com/v1/groups/{str(id)}/roles/{str(roleid)}/users?limit=100&sortOrder=Asc&cursor={cursor}"
    request = requests.get(url)
    if request.status_code == 200:
        requestJson = request.json()
        for x in requestJson['data']:
            tr.append(x)

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
            memberuids.append(x)
        if requestJson['nextPageCursor'] != None:
            #There is another page, recurse
            recursed = RecurseGroupMembersByRoleWithCursor(id, roleid,requestJson['nextPageCursor'])
            for x in recursed:
                memberuids.append(x)
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
        

# print(GetGroupMembersByRole(2593707,17183355))
# print(GetRoleMembercount(2593707, 17183357))