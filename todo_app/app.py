
from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.session_items import sort_items
from todo_app.data.trello_items import get_boards, get_items, get_item, add_item, update_item_status, clear_item
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
@app.route('/<op_message>')
def index(op_message = ""):
    # Get the list of items from the pre-loaded session file and sort by status prior to loading
    board_id = get_boards()
    items = sort_items(get_items(board_id))

    # Get the version out from the file
    with open('TODO_APP/VERSION.txt','rt') as ver_file:
        ver = ver_file.read()

    # Count the items not completed
    open_items = [item for item in items if item['status'] != 'Completed']
    num_open_items = len(open_items)

    # Render the index template, displaying the list items and an update for the last performed action as required
    return render_template("index.html", version = ver, todo_items = items,\
         op_message = op_message,\
         num_open_items = num_open_items)


@app.route('/', methods=['POST'])
@app.route('/<op_message>', methods=['POST'])
def addItem(op_message = ""):
    # Get the item title which has been entered into the form
    item_title = request.form.get('itemTitle')

    # Use the title input to add a new item to the file
    board_id = get_boards()
    added_item = add_item(board_id, item_title)

    # construct operation message to display to user
    op_message = f"Added item: [#{added_item['id']}] \"{added_item['title']}\""

    # Reload the index template to display the list with its new item
    return redirect(url_for('index', op_message = op_message))


@app.route('/clearItem/<id>')
def clearItem(id):
    # Call low-level function to clear the specified item and return it to update the operation message
    cleared_item = clear_item(id)
    op_message = f"Cleared item: [#{cleared_item['id']}] \"{cleared_item['title']}\""

    # Reload the index template to display the list post-clear
    return redirect(url_for('index', op_message = op_message))


@app.route('/clearItems')
def clearItems():
    clear_items()

    # Reload the index template to display the list post-clear
    op_message = "Cleared all items -  hope they weren't important!"
    return redirect(url_for('index', op_message = op_message))


@app.route('/updateStatus/<new_status><id>')
def updateStatus(id, new_status):

    updated_item = get_item(id)
    old_status = updated_item['status']

    update_item_status(id, new_status)

    # construct operation message to display to user
    op_message = f"Updated item [#{updated_item['id']}] \"{updated_item['title']}\":   " \
        + f"  Status changed from \"{old_status}\" to \"{new_status}\"."
    
    return redirect(url_for('index', op_message = op_message))


if __name__ == '__main__':
    app.run()