
from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.session_items import get_item, get_items, add_item, clear_items, clear_item, update_item_status
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
@app.route('/<op_message>')
def index(op_message = ""):
    # Get the list of items from the pre-loaded session file
    todoItems = get_items()

    # Get the version out from the file
    with open('TODO_APP/VERSION.txt','rt') as verFile:
        ver = verFile.read()

    # Render the index template, displaying the list items and an update for the last performed action as required
    return render_template("index.html", version = ver, todoItems = todoItems, op_message = op_message)


@app.route('/', methods=['POST'])
@app.route('/<op_message>', methods=['POST'])
def addItem(op_message = ""):
    # Get the item title which has been entered into the form
    itemTitle = request.form.get('itemTitle')

    # Use the title input to add a new item to the file
    added_item = add_item(itemTitle)

    # Reload the index template to display the list with its new item
    return redirect(url_for('index', op_message = f"Added item: [#{added_item['id']}] {added_item['title']}"))


@app.route('/clearItem/<int:id>')
def clearItem(id):
    # Call low-level function to clear the specified item and return it to update the operation message
    cleared_item = clear_item(id)

    # Reload the index template to display the list post-clear
    return redirect(url_for('index', op_message = f"Cleared item: [#{cleared_item['id']}] {cleared_item['title']}"))


@app.route('/clearItems')
def clearItems():
    clear_items()

    # Reload the index template to display the list post-clear
    return redirect(url_for('index', op_message = "Cleared all items -  hope they weren't important!"))


@app.route('/updateStatus/<new_status><int:id>')
def updateStatus(id, new_status):

    updated_item = get_item(id)
    old_status = updated_item['status']

    update_item_status(id, new_status)
    
    return redirect(url_for('index', \
        op_message = f"Updated item [#{updated_item['id']}] {updated_item['title']} status" \
        + f" from {old_status} to {new_status}."))


if __name__ == '__main__':
    app.run()