from flask import Flask, render_template, request, redirect, url_for

from todo_app.data.session_items import get_items, add_item, clear_items, clear_item
from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index(statusUpdate = ""):
    # Get the list of items from the pre-loaded session file
    todoItems = get_items()

    # Get the version out from the file
    with open('TODO_APP/VERSION.txt','rt') as verFile:
        ver = verFile.read()

    # Render the index template, displaying the list items
    return render_template("index.html", version = ver, todoItems = todoItems, statusUpdate = statusUpdate)


@app.route('/', methods=['POST'])
def addItem():
    # Get the item title which has been entered into the form
    itemTitle = request.form.get('itemTitle')

    # Use the title input to add a new item to the file
    add_item(itemTitle)

    # Reload the index template to display the list with its new item
    return redirect(url_for('index'))


@app.route('/clearItem/<item>')
def clearItem(item):
    clear_item(item)

    # Reload the index template to display the list post-clear
    return redirect(url_for('index'))


@app.route('/clearItems')
def clearItems():
    clear_items()

    # Reload the index template to display the list post-clear
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
