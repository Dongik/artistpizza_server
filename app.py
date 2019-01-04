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
rollbook_db = db.artistpizza.rollbooks
members_db = db.artistpizza.members
classes_db = db.artistpizza.classes

def get_today_code():
    date = datetime.today()
    return int(date.strftime('%y%m%d'))


@app.route('/api/weekdata', methods=['GET', 'PUT'])
# @cross_origin(supports_credentials=True)
# @cross_origin(origins=['http://0.0.0.0:5000/'])
def route_week_data():
    if request.method == 'GET':
        week_id = datetime.today().strftime('%y년%W주차')
        week_class = classes_db.find_one({"_id":week_id})
        return jsonify(week_class)
    elif request.method == 'PUT':
        # print(request.json)
        week_data = request.json
        # print(week_data)
        classes_db.save(week_data)
        # return "good"
        return jsonify(dict(message="good"))


@app.route('/class')
def route_class_view():
    query = request.json
    week_id = query['week_id']
    week_class = classes_db.find_one({"_id":week_id})
    rollbook = week_class[query['day']][query['time']][query['course']]
    rollbook['title'] = "{0} {1} {2} {3}".format(week_id, query['day'], query['time'], query['course'])
    return render_template("rollbook.html", rollbook=rollbook)

@app.route('/rollbook')
def route_rollbook_view():
    day = request.args.get('day')
    time = request.args.get('time')
    course = request.args.get('course')
    name = request.args.get('name')
    today = get_today_code()
    # today = 190103
    rollbook = rollbook_db.find_one({"day": day, "time": time, "course": course, "name": name})
    del rollbook['_id']
    title = "{} 출석부".format(name)
    return render_template("rollbook.html", title=title, rollbook=rollbook)

@app.route('/attend', methods=['POST'])
def route_attend_api():
    print(request.json)
    attend_request = request.json
    current_week = ""
    member_id = int(attend_request['member_id'])
    rollbook = rollbook_db.find_one({"_id": date})
    class_board = classes_db.find_one({"_id": current_week})
    member = members_db.find_one({"_id": member_id})
    course = member['course']
    if member is None:
        return jsonify(dict(message="wrong member id"))
    member_name = member['name']
    rollbook = class_board[course['day']][course['time']][course['course']]
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

# api
@app.route('/rollbook', methods=['POST', 'GET', 'PUT'])
def route_rollbook_api(date):
    if request.method == 'POST':
        rollbook = request.json
        return jsonify(rollbook_db.incert_one(rollbook))
    elif request.method == 'GET':
        return jsonify(rollbook_db.find_one({"_id": int(date)}))
    elif request.method == 'PUT':
        rollbook = request.json
        return jsonify(rollbook_db.save(rollbook))

# @app.route('/weekclass', methods=['GET'])
# def route_weekclass():
#     return jsonify(rollbook_db.find({""}))


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