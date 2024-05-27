import asyncpg
from flask import Flask, jsonify
import asyncio
from flask import request

user = "bohdandemyanchuk"
password = "AeT8hs9lOLSq"
database = "diary"
host = "ep-weathered-resonance-391969.eu-central-1.aws.neon.tech"

app = Flask(__name__)

@app.route('/get_lessons')
async def get_lessons():
    classroom_name = '10 Б'
    con = await asyncpg.connect(user=user, password=password, database=database, host=host)
    lessons = []
    try:
        classroom_id = await con.fetchval("SELECT id FROM classroom WHERE name = $1", classroom_name)
        data = await con.fetch("SELECT * FROM classroom_subject WHERE classroom_id = $1", classroom_id)
        for i in data:
            tmp = {}
            print(i['classroom_id'], i['subject_id'])
            subject_name = await con.fetchval("SELECT name FROM subject WHERE id = $1", i['subject_id'])
            teacher_id = await con.fetchval("SELECT user_id FROM user_subject WHERE subject_id = $1", i['subject_id'])
            teacher_name = await con.fetchrow("SELECT name, surname FROM users WHERE id = $1", teacher_id)
            tmp['name'] = subject_name
            tmp['teacher'] = f"{teacher_name['name']} {teacher_name['surname']}"
            print(tmp)
            lessons.append(tmp)
    finally:
        await con.close()
    # lessons = [
    #     {"name": "Українська мова", "teacher": "Ім'я"},
    #     {"name": "Російська мова", "teacher": "Ім'я"}
    # ]
    return jsonify(lessons), 200

@app.route('/keep_alive')
async def keep_alive():
	return "200"


@app.route('/login')
async def login():
    classroom_name = '10 Б'
    con = await asyncpg.connect(user=user, password=password, database=database, host=host)
    lessons = []
    try:
        amount = await con.fetchval("SELECT count(id) FROM users WHERE email = $1", str(request.args.get('email')))
        return jsonify({"exists": bool(amount)})
    finally:
        await con.close()
    # lessons = [
    #     {"name": "Українська мова", "teacher": "Ім'я"},
    #     {"name": "Російська мова", "teacher": "Ім'я"}
    # ]

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
