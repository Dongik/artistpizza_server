import pymongo
from datetime import datetime, timedelta

db = pymongo.MongoClient()
members_db = db.artistpizza.members
courses = ['수채화', '유화']

def generate_members():
    members = []
    count = 0
    for first_name in ['김', '이', '박', '서', '최', '인', '리', '나', '강']:
        for middle_name in ['철', '동', '영', '양', '웅']:
            for last_name in ['수', '희', '자', '진']:
                name = first_name + middle_name + last_name
                members.append({
                    "_id": str(9999 - count),
                    "name": name,
                    "phone": "010-0000-{}".format(9999-count),
                    "count": 3,
                    "expire_date": 191230,
                    "credit": 0,
                    "course": courses[count%2]
                })
                count += 1
    return members


new_members = generate_members()
print("generate members number is {}".format(len(new_members)))


def insert_members(members):
    members_db.insert_many(members)


insert_members(new_members)