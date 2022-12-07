import json
import psycopg2
from flask import Flask, request, render_template, g
from flask_cors import CORS
from flask_restful import Resource, Api
from data_preprocessing import preprocess_data
from db_config import host, user, password, db_name
from queries.ext_query import insert_query, check_in_user_agent, create_new_note, create_new_ext_user, user_have_dataset

app = Flask(__name__)
CORS(app)
api = Api()

COUNT_NOTE = 15000
COUNT_CHECKS = 5


@app.before_request
def connect_to_db():
    g.conn_db = psycopg2.connect(host=host, user=user, password=password, database=db_name)


@app.teardown_request
def teardown_request(errors):
    db = getattr(g, 'conn_db', None)
    if db is not None:
        db.commit()
        db.close()


class ExtBlock(Resource):
    def post(self): # блокировочка
        data = json.loads(request.data)
        user_agent = data.pop('userAgent')
        with g.conn_db.cursor() as cursor:
            cursor.execute(check_in_user_agent, (user_agent,))  # если ли уже такой пользователь
            user_id = cursor.fetchone()
            cursor.execute(user_have_dataset, (user_id,))
            res = cursor.fetchone()
            res = res[0] // (COUNT_NOTE / COUNT_CHECKS)
        ret = {'block': False, 'count_checks': res}
        return ret, 200


class Extension(Resource):
    def post(self):  # запросы для слежки за пользователем
        data = json.loads(request.data)
        with g.conn_db.cursor() as cursor:
            cursor.execute(insert_query, [json.dumps(data.get(name)) if data.get(name, None) else None for name in
                                          ['headers', 'method', 'initiator', 'url', 'timestamp', 'type', 'document',
                                           'frame', 'request']
                                          ])
        return {}, 200

    def put(self):  # запросы для сборке сведений о идетификации
        try:
            data = json.loads(request.data)
        except Exception:
            return {}, 200
        user_agent = data.pop('userAgent')
        max_x = data.pop('x')
        max_y = data.pop('y')
        if not data:
            return {}, 200
        with g.conn_db.cursor() as cursor:
            cursor.execute(check_in_user_agent, (user_agent,))  # если ли уже такой пользователь
            user_id = cursor.fetchone()
            if not user_id:
                cursor.execute(create_new_ext_user, [user_agent, max_x, max_y])
                cursor.execute(check_in_user_agent, [user_agent])
                user_id = cursor.fetchone()
            user_id = user_id[0]
            data = [(i['X'], i['Y'], i['timestamp'], user_id, i['url']) for i in data.values()]
            cursor.executemany(create_new_note, data)
        return {}, 200

    def delete(self): # нужно ли пользователю повторно проходить процедуру
        data = json.loads(request.data)
        user_agent = data.pop('userAgent')
        ret = {'checked': False}
        with g.conn_db.cursor() as cursor:
            cursor.execute(check_in_user_agent, (user_agent,))  # если ли уже такой пользователь
            user_id = cursor.fetchone()
            if user_id:
                cursor.execute(user_have_dataset, (user_id,))
                res = cursor.fetchone()
                if res[0] > COUNT_NOTE:
                    ret['checked'] = True # пока просто на сбор датасета
                    # сюда вставить запуск юпитер ноутбука по подготовке данных
                    # TODO встроить проверку есть ли уже таблица на этого польщователя
                    preprocess_data(user_id)
        return ret, 200


@app.route('/extinsion_ui', methods=["GET", "POST"])
def extinsion():
    if request.method == "GET":
        return render_template('extinsions.html', context={})
    elif request.method == "POST":
        query = request.form['text']
        with g.conn_db.cursor() as cursor:
            try:
                cursor.execute(query)
                data = cursor.fetchall()
            except:
                data = 'Error'
        return render_template('extinsions.html', context={data: data})


api.add_resource(Extension, '/extinsion/api')
api.add_resource(ExtBlock, '/extinsion/block')
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
