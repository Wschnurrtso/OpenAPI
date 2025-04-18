
"""
Example script showing how to represent todo lists and todo entries in Python
data structures and how to implement endpoint for a REST API with Flask.

Requirements:
* flask
"""

import uuid 

from flask import Flask, request, jsonify, abort


# initialize Flask server
app = Flask(__name__)

# create unique id for lists, entries
todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'
todo_1_id = str(uuid.uuid4())
todo_2_id = str(uuid.uuid4())
todo_3_id = str(uuid.uuid4())
todo_4_id = str(uuid.uuid4())

# define internal data structures with example data
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'name': 'Milch', 'description': '', 'list': todo_list_1_id},
    {'id': todo_2_id, 'name': 'Arbeitsblätter ausdrucken', 'description': '', 'list': todo_list_2_id},
    {'id': todo_3_id, 'name': 'Kinokarten kaufen', 'description': '', 'list': todo_list_3_id},
    {'id': todo_3_id, 'name': 'Eier', 'description': '', 'list': todo_list_1_id},
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PUT'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# define endpoint for getting and deleting existing todo lists
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # return ToDo list with given id
        print('Gebe ToDo-Liste zurück...')
        return jsonify(list_item), 200
    elif request.method == 'DELETE':
        # delete list with given id
        print('Lösche ToDo-Liste...')
        todo_lists.remove(list_item)
        return jsonify('Anfrage erfolgreich'), 200

# define endpoint for adding a new list
@app.route('/todo-list', methods=['POST'])
def add_new_list():
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    print('Hinzuzufügende Liste erhalten: {}'.format(new_list))
    # Validate the input data
    if not new_list or 'name' not in new_list or not new_list['name'].strip():
        abort(400, description="Ungültige Eingabe: 'name' ist erforderlich und darf nicht leer sein.")
    # create id for new list, save it and return the list with id
    new_list['id'] = str(uuid.uuid4())
    todo_lists.append(new_list)
    return jsonify(new_list), 200

# define endpoint for adding a new entry to a list
@app.route('/todo-list/<list_id>/entry', methods=['POST'])
def add_new_entry(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    # make JSON from POST data (even if content type is not set correctly)
    new_entry = request.get_json(force=True)
    print('Hinzuzufügenden Eintrag erhalten: {}'.format(new_entry))
    # Validate the input data
    if not new_entry or 'name' not in new_entry or not new_entry['name'].strip():
        abort(400, description="Ungültige Eingabe: 'name' ist erforderlich und darf nicht leer sein.")
    # create id for new entry, set list id, save it and return the entry with the id
    new_entry['id'] = str(uuid.uuid4())
    new_entry['list'] = list_id
    todos.append(new_entry)
    return jsonify(new_entry), 200

# define endpoint for getting all lists
@app.route('/todo-lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists), 200

# define endpoint for getting all entries of a todo list
@app.route('/todo-list/<list_id>/entries', methods=['GET'])
def get_all_entries_of_list(list_id):
    entries_array = []
    for entry in todos:
        if entry['list'] == list_id:
            entries_array.append(entry)
    return jsonify(entries_array)

# define endpoint for deleting an entry of a todo list
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['DELETE'])
def delete_entry(list_id, entry_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    # find todo entry depending on given entry id
    entry_item = None
    for entry in todos:
        if entry['id'] == entry_id and entry['list'] == list_id:
            entry_item = entry
            break
    # if the given entry id is invalid, return status code 404
    if not entry_item:
        abort(404)
    # delete entry with given id
    print('Lösche ToDo-Eintrag...')
    todos.remove(entry_item)
    return jsonify('Anfrage erfolgreich'), 200

# define endpoint for updating an entry of a todo list
@app.route('/todo-list/<list_id>/entry/<entry_id>', methods=['PUT'])
def update_entry(list_id, entry_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    # find todo entry depending on given entry id
    entry_item = None
    for entry in todos:
        if entry['id'] == entry_id and entry['list'] == list_id:
            entry_item = entry
            break
    # if the given entry id is invalid, return status code 404
    if not entry_item:
        abort(404)
    # make JSON from POST data (even if content type is not set correctly)
    new_entry = request.get_json(force=True)
    print('Zu aktualisierenden Eintrag erhalten: {}'.format(new_entry))
    # Validate the input data
    if not new_entry or 'name' not in new_entry or not new_entry['name'].strip():
        abort(400, description="Ungültige Eingabe: 'name' ist erforderlich und darf nicht leer sein.")
    # update the entry with the new data and return it with the id
    entry_item.update(new_entry)
    return jsonify(entry_item), 200

if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
