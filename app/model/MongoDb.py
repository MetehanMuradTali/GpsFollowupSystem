import pymongo

client = pymongo.MongoClient()
mydb=client["mydb"]
mycol=mydb["Cars"]


def SearchCoordinates(id,firstdate,seconddate):
    myquery = {"Id": id,"$and":[
        {"Date":{"$gte":seconddate}},
        {"Date": {"$lte": firstdate}},
    ]}
    mydoc = list(mycol.find(myquery))
    for x in mydoc:
         x.pop('_id')
    return mydoc

def theLastCoordinate(id):
    myquery= {"Id":str(id)}
    mydoc = list(mycol.find(myquery).sort('_id',-1).limit(1));
    for x in mydoc:
         x.pop('_id')
    return mydoc