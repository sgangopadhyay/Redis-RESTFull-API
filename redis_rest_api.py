# PROGRAM : RESTfull API using Python and Redis NoSQL Database Server
# Name of Programmer : Suman Gangopadhyay
# Email ID : linuxgurusuman@gmail.com
# Website : https://www.sumangangopadhyay.tech
# Python Version : 3.7
# Redis : 5.0.4

from flask import Flask
from flask import request
from flask import redirect
from flask import jsonify
import redis
import uuid
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'i_love_pizza'

cur = redis.Redis(host='127.0.0.1', port=6379, db=0, password='priya@123')

# Display all the data from a Redis Server
@app.route('/', methods=['GET'])
def display_all():
    my_list = cur.zrange("data", 0, -1, withscores=True)
    return jsonify(my_list)

#Write to a Redis Server
@app.route('/write', methods=['POST'])
def write():
    name = request.get_json()["name"]
    email = request.get_json()["email"]
    score = cur.zcount("data", '-inf', '+inf') + 1
    data = str({'id': score, 'uid':str(uuid.uuid1()),'name': name, 'email': email, 'created_updated':str(datetime.datetime.now())})
    cur.zadd("data", {data:score})
    return jsonify(data)

# Delete a data using score
@app.route('/delete/<int:score>', methods=['DELETE'])
def delete(score):
    if cur.zremrangebyscore("data", score,score) == 0:
        return jsonify({"error": "the element does not exists"})
    else:
        cur.zremrangebyscore("data", score, score)
        return display_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
