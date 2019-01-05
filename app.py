from flask import Flask, request, jsonify, session, Session, render_template
from flask_cors import CORS, cross_origin
import pymongo
from datetime import datetime
app = Flask(__name__, static_url_path="")
CORS(app)
cors = CORS(app, resources={
  r"/v1/*": {"origin": "*"},
  r"/api/*": {"origin": "*"},
})

# app.config['CORS_HEADERS'] = 'Content-Type'
# app.config['JSON_AS_ASCII'] = False


db = pymongo.MongoClient()
members_db = db.artistpizza.members
attendance_db = db.artistpizza.attendances

def get_today():
    return int(datetime.today().strftime('%y%m%d'))


def get_this_week():
    return int(datetime.today().strftime('%y%W'))

def get_attendance():
    attendance = attendance_db.find_one({"_id": get_today()})
    if attendance is None:
        attendance_db.save({"_id": get_today(), "유화": {}, "수채화": {}})
        attendance = attendance_db.find_one({"_id": get_today()})
    return attendance


@app.route('/members', methods=['GET', 'POST', 'PUT'])
def route_members_view():
    if request.method == 'POST':
        member = request.form
        members_db.incert_one(member)
    elif request.method == 'PUT':
        member = request.form
        members_db.save(member)
    members = members_db.find()
    return render_template("members.html", members=members)

@app.route('/attendance')
def route_attendance_view():
    attendance = attendance_db.find_one({"_id": get_today()})
    del attendance['_id']
    return render_template("attendance.html", title=get_today(),attendance=attendance)


@app.route('/attend', methods=['POST'])
def route_attend_api():
    print(request.json)
    attend_request = request.json
    member_id = attend_request['member_id']
    member = members_db.find_one({"_id": member_id})
    if member is None:
        return jsonify(dict(message="일치하는 회원정보가 없어요"))
    course = member['course']
    attendance = get_attendance()
    if member_id in attendance[course]:
        return jsonify(dict(message="오늘은 이미 출석했습니다."))
    elif member['count'] == 0:
        return jsonify(dict(message="남은 수업횟수가 없습니다."))
    elif member['expire_date'] < get_today():
        member['count'] = 0
        members_db.save(member)
        return jsonify(dict(message="수업기한이 지났습니다."))
    else:
        attendance[course][member_id] = member['name']
        member['count'] -= 1
        attendance_db.save(attendance)
        members_db.save(member)
        return jsonify(dict(message="출석체크 했습니다."))


@app.route('/ask/<pin>', methods=['GET'])
def route_ask_api(pin):
    member = members_db.find_one({"_id": pin})
    if member is None:
        return jsonify(dict(message="없는 번호입니다.", is_attendable=False))
    attendance = get_attendance()
    print(attendance)
    if pin in attendance[member['course']]:
        return jsonify(dict(message="이미 출석하셨습니다.", is_attendable=False))
    if member['expire_date'] < get_today():
        member['count'] = 0
        members_db.save(member)
        return jsonify(dict(message="수업기한이 지났습니다."), is_attendable=False)
    if member['count'] == 0:
        return jsonify(dict(message="수업횟수를 소진하셨습니다.", is_attendable=False))
    else:
        return jsonify(dict(message="{}님 반갑습니다.".format(member['name']), is_attendable=True))


@app.route('/api/members', methods=['POST', 'GET', 'PUT'])
def route_member():
    if request.method == 'POST':
        member = request.json
        return jsonify(members_db.incert_one(member))
    elif request.method == 'GET':
        members = []
        for member in members_db.find():
            members.append(member)
        print(members)
        return str(members)
    elif request.method == 'PUT':
        member = request.json
        return jsonify(members_db.save(member))

app.run(host='0.0.0.0')