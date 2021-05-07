import pymongo


class dbConnector:
    def __init__(self):
        self.__db_name = "imiDB"
        self.__user_name = "doge12"
        self.__user_pwd = "doge12"
        self.__token = f"mongodb+srv://{self.__user_name}:{self.__user_pwd}@cluster0.mk62e.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

        self.__client = pymongo.MongoClient(self.__token)

        self.__collection = "imiRecords"

    def _get_collection(self):
        return self.__collection

    def test(self):
        print(self.__client[self._get_collection()])

    def insert(self, data: dict):
        if self.__client[self._get_collection()]["db1"].find({"rid": data["rid"]}).count() > 0:
            print("record exists")
            return False
        else :
            return self.__client[self._get_collection()]["db1"].insert_one(data)


imi_db_connector = dbConnector()

