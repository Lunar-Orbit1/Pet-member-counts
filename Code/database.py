from sqlitedict import SqliteDict

def readDB(key:str):
    try:
        with SqliteDict("DATABASEMAIN.sqlite3") as mydict:
            value = mydict[key]
        return value
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def writeDB(key:str, data:any):
    try:
        with SqliteDict("DATABASEMAIN.sqlite3") as mydict:
            mydict[key] = data
            mydict.commit() 
            return
    except Exception as e:
        print(f"ERROR: {e}")
        return