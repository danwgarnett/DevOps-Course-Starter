from todo_app.flask_config import Config
from flask import Flask, render_template, request, redirect, url_for
import pkg_resources
from todo_app.data.trello_class import TrelloBoard

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
@app.route('/<op_message>')
def index(op_message = ""):

    current_board = TrelloBoard()
    items = current_board.board_items

    open_items = [item for item in items if item.list["name"] != 'Done']
    num_open_items = len(open_items)

    # Get the version out from the file - left this syntax in as the pyproject toml version doesn't seem to update.
    # with open('TODO_APP/VERSION.txt','rt') as ver_file:
    #     ver = ver_file.read()
    ver = pkg_resources.get_distribution('todo-app').version

    return render_template("index.html", version = ver, todo_items = items,
         op_message = op_message,
         num_open_items = num_open_items)


@app.route('/', methods=['POST'])
@app.route('/<op_message>', methods=['POST'])
def add_item(op_message = ""):

    item_title = request.form.get('new_item_title')

    current_board = TrelloBoard()
    added_item = current_board.add_item(item_title)

    op_message = f"Added item: \"{added_item.title}\""    
    return redirect(url_for('index', op_message = op_message))


@app.route('/clear_item/<id>')
def clear_item(id):

    current_board = TrelloBoard()
    cleared_item = current_board.get_item(id)
    cleared_item.clear_item()

    op_message = f"Cleared item: \"{cleared_item.title}\""
    return redirect(url_for('index', op_message = op_message))


@app.route('/clear_items')
def clear_items():

    current_board = TrelloBoard()
    current_board.board_id
    items = current_board.board_items

    for item in items:
        item.clear_item()

    op_message = "Cleared all items -  hope they weren't important!"
    return redirect(url_for('index', op_message = op_message))


@app.route('/update_status/<new_status>/<id>')
def update_status(id, new_status):

    current_board = TrelloBoard()
    updated_item = current_board.get_item(id)
    old_status = updated_item.list['name']

    updated_item.update_item_status(new_status)

    op_message = f"Updated item \"{updated_item.title}\":   " \
               + f"    Status changed from \"{old_status}\" to \"{new_status}\"."
    return redirect(url_for('index', op_message = op_message))


if __name__ == '__main__':
    app.run()