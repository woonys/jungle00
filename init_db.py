import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbjungle

def insert_db():
<<<<<<< HEAD
    with open('member_list.json') as f:
=======
    with open('member_list.json','rt', encoding='UTF8') as f:
>>>>>>> a31b6feb14488462544e185051575a158193e5b0
        file_data = json.load(f)
        print(file_data)
    db.member_list.insert_many(file_data)


    print('완료!')


### 실행하기
insert_db()