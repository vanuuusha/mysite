from flask import Flask, request, render_template
import psycopg2
from db_config import host, user, password, db_name

app = Flask(__name__)


@app.route("/extinsion_api", methods=["POST"])
def new_record():
    if request.method == "POST":
        with psycopg2.connect(host=host, user=user, password=password, database=db_name) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM table")

        print(request.data.decode())
        return '', 200


@app.route('/extinsion', methods=["GET", "POST"])
def extinsion():
    if request.method == "GET":
        return render_template('extinsions.html', context={})
    elif request.method == "POST":
        return render_template()


if __name__ == "__main__":
    app.run(debug=True)
