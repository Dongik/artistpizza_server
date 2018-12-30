import pymongo

db = pymongo.MongoClient()
members_db = db.artistpizza.members
courses_db = db.artistpizza.courses

목 = 4
금 = 5
토 = 6

n2h = {
    4: "목",
    5: "금",
    6: "토"
}

courses = {
    "목1": {
        "name": "목1",
        "weekday": 목,
        "time": "목_1800"
    },
    "목2": {
        "name": "목2",
        "weekday": 목,
        "time": "목_2000"
    },
    "금1": {
        "name": "금1",
        "weekday": 금,
        "time": "금_1800"
    },
    "금2": {
        "name": "금2",
        "weekday": 금,
        "time": "금_2000"
    },
    "토1": {
        "name": "토1",
        "weekday": 토,
        "time": "토_1200"
    },
    "토2": {
        "name": "토2",
        "weekday": 토,
        "time": "토_1400"
    },
}

new_members = [
    {
        "_id": 93733471,
        "name": "일동익",
        "phone": "01093733471",
        "count": 2,
        "credit": 4500,
        "course_name": "목1"
    },
    {
        "_id": 93733472,
        "name": "이동익",
        "count": 4,
        "phone": "01093733472",
        "credit": 4500,
        "course_name": "목2"
    },
    {
        "_id": 93733473,
        "name": "삼동익",
        "phone": "01093733473",
        "count": 5,
        "credit": 4500,
        "course_name": "금1"
    },
    {
        "_id": 93733474,
        "name": "사동익",
        "phone": "01093733474",
        "count": 6,
        "credit": 4500,
        "course_name": "금2"
    },
    {
        "_id": 93733475,
        "name": "오동익",
        "phone": "01093733475",
        "count": 7,
        "credit": 4500,
        "course_name": "토1"
    },
    {
        "_id": 93733476,
        "name": "육동익",
        "phone": "01093733476",
        "count": 7,
        "credit": 4500,
        "course_name": "토2"
    },
]

# members_db.insert_many(new_members)

rollbook_db = db.artistpizza.rollbooks

from datetime import datetime, timedelta

rollbooks = {}

def book2(member, course):
    for i in range(member['count']):
        print("count {}".format(i))
        # calculate book date
        gap = course['weekday'] - datetime.today().weekday() + 7 * (i + 1) - 1
        # if gap < 1:
        #     gap += 7
        date = datetime.today() + timedelta(days=gap)
        bookdate = int(date.strftime('%y%m%d'))
        # bookdate = "{0}_{1}".format(bt, course['time'])
        print("booktime is {}".format(bookdate))

        rollbook = rollbook_db.find_one({"_id": bookdate})
        if rollbook is None:
            rollbook_db.insert_one({"_id": bookdate})
            rollbook = rollbook_db.find_one({"_id": bookdate})

        rollbook[member['name']] = dict(course=member['course_name'], check=False)

        rollbook_db.save(rollbook)

def book(member):
    course = courses[member['course_name']]
    book2(member, course)

def book_all():
    for member in members_db.find():
        print("booking {}".format(member))
        book(member)

book_all()