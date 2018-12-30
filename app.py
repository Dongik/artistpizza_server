from flask import Flask, request, jsonify, session, Session
import pymongo

app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False
db = pymongo.MongoClient()
rollbook_db = db.artistpizza.rollbooks
members_db = db.artistpizza.members

@app.route('/')
def index():
    return "hello"

@app.route('/attend', methods=['POST'])
def route_attend():
    print(request.json)
    attend_request = request.json
    date = attend_request['date']
    member_id = int(attend_request['member_id'])
    rollbook = rollbook_db.find_one({"_id": date})
    member = members_db.find_one({"_id": member_id})
    if member is None:
        return jsonify(dict(message="wrong member id"))
    member_name = member['name']
    if member_name in rollbook:
        print("check {}".format(rollbook[member_name]))
        if rollbook[member_name]['check'] == False:
            member['count'] -= 1
            members_db.save(member)
            rollbook[member_name]['check'] = True
            rollbook_db.save(rollbook)
            return jsonify(dict(message="success"))
        else:
            return jsonify(dict(message="already checked"))
    else:
        return jsonify(dict(message="not booked"))


@app.route('/rollbook/<date>', methods=['POST', 'GET', 'PUT'])
def route_rollbook(date):
    if request.method == 'POST':
        rollbook = request.json
        return jsonify(rollbook_db.incert_one(rollbook))
    elif request.method == 'GET':
        return jsonify(rollbook_db.find_one({"date": date}))
    elif request.method == 'PUT':
        rollbook = request.json
        return jsonify(rollbook_db.save(rollbook))


@app.route('/members', methods=['POST', 'GET', 'PUT'])
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