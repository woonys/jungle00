import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbjungle

def insert_db():

    with open('member_list.json') as f:
        file_data = json.load(f)
        print(file_data)
    db.member_list.insert_many(file_data)


    print('완료!')


### 실행하기
insert_db()