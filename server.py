from flask import Flask, request, render_template
import psycopg2
from db_config import host, user, password, db_name
import json

app = Flask(__name__)

insert_query = """
INSERT INTO request (headers, method, initiator, url, timestamp, type, document, frame, request) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
"""


@app.route("/extinsion_api", methods=["POST"])
def new_record():
    if request.method == "POST":
        data = json.loads(request.data)
        with psycopg2.connect(host=host, user=user, password=password, database=db_name) as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert_query, [json.dumps(data.get(name)) if data.get(name, None) else None for name in
                                                                                      ['headers', 'method', 'initiator', 'url', 'timestamp', 'type', 'document', 'frame', 'request']
                                                                                      ])
        return '', 200


@app.route('/extinsion', methods=["GET", "POST"])
def extinsion():
    if request.method == "GET":
        return render_template('extinsions.html', context={})
    elif request.method == "POST":
        query = request.form['text']
        with psycopg2.connect(host=host, user=user, password=password, database=db_name) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query)
                    data = cursor.fetchall()
                except:
                    data = 'Error'
        return f'{data}'


if __name__ == "__main__":
    app.run(debug=True)
