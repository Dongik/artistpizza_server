import pymongo
from datetime import datetime, timedelta

db = pymongo.MongoClient()
members_db = db.artistpizza.members
classes_db = db.artistpizza.classes

classes = {}
classes['목요일'] = {}
classes['목요일']['12-2시'] = {'수채화': {}, '유화': {}}
classes['목요일']['2-4시'] = {'수채화': {}, '유화': {}}
classes['목요일']['6-8시'] = {'수채화': {}, '유화': {}}
classes['목요일']['8-10시'] = {'소묘드로잉': {}, '유화': {}}
classes['금요일'] = {}
classes['금요일']['12-2시'] = {'수채화': {}, '유화': {}}
classes['금요일']['2-4시'] = {'수채화': {}, '유화': {}}
classes['금요일']['6-8시'] = {'수채화': {}, '유화': {}}
classes['금요일']['8-10시'] = {'소묘드로잉': {}, '유화': {}}
classes['토요일'] = {}
classes['토요일']['10-2시'] = {'master': {}}
classes['토요일']['12-2시'] = {'수채화': {}, '유화': {}}
classes['토요일']['2-4시'] = {'수채화': {}, '유화': {}}
classes['토요일']['6-8'] = {"oneday": {}}





# class number 22
# member number = 220
def generate_members():
    members = []
    count = 0
    for first_name in ['김', '이', '박' , '서', '최', '인', '리', '나', '강']:
        for middle_name in ['철', '동', '영', '양', '웅']:
            for last_name in ['수', '희', '자', '진']:
                name = first_name + middle_name + last_name
                members.append({
                    "name": name,
                    "id": str(1000-count),
                    "count": 3
                })
    return members


new_members = generate_members()
print("generate members number is {}".format(len(new_members)))

# def insert_members(members):
#     members_db.insert_many(members)
#
# insert_members()

def fill_class_member(members, classes):
    count = 0
    while True:
        for day in classes:
            for time in classes[day]:
                for course in classes[day][time]:
                    # print("count is {}".format(count))
                    member = members[count]
                    # print(member)
                    classes[day][time][course][member['name']] = False
                    count += 1
                    if len(members) == count:
                        return


fill_class_member(new_members, classes)



def insert_week_class(week_class):
    week_class['_id'] = datetime.today().strftime('%y년%W주차')
    classes_db.insert_one(classes)
    print("week class incerted")

insert_week_class(classes)

# members_db.insert_many(new_members)