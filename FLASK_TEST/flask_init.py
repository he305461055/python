from flask import Flask, jsonify,abort,make_response,request, url_for
import pymysql
#import pandans
import json
'''
config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'db': 'spiders',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor,
    }

app = Flask(__name__)
def get_data(tablename,parameter):
    datalist=[]
    connection=pymysql.connect(**config)
    with  connection.cursor() as cursor:
        sql='SELECT %s FROM %s limit 10 ' %(parameter,tablename)
        cursor.execute(sql)
        for row in cursor.fetchall():
            sss=str(row)
            print(sss)
            #aa=json.loads(sss)
            #print(aa)
            #print(aa['url'])
            #value='\"value\":' +str(row)
            #print(value)
            datalist.append(row)
    return datalist

@app.route('/v1.0/<string:str>', methods=['GET'])
def get_task(str):
    #if request.method=='POST':
    #    print(request.form)
    #    print(request.get_data())
    #    print(request.data)
    #    return jsonify({tablename: get_data(tablename,parameter)})
    #else:
    url = request.url
    tablename = url.split('/')[-1].split('?')[0]
    parameter = url.split('?')[-1]
    return jsonify({'data':get_data(tablename,parameter)})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
'''
'''
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    #return jsonify({'tasks': tasks})
    return jsonify({'tasks': list(map(make_public_task, tasks))})

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    print(new_task)
    return new_task

'''
'''
if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0')#让外网能访问
'''

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')


def index():
    return render_template('index.html')


@app.route('/user/<name>')


def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    app.run()