from flask import Flask, render_template
from todo_app.data.session_items import get_items

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    
    # Get the list of items from the pre-loaded session file
    todoItems = get_items()
    
    # Use a list comprehension to get the titles of all the items
    todoTitles = [item['title'] for item in todoItems]
    #todoTitles = ["first item", "second item", "third item"]

    # render the index template, displaying the list items
    return render_template("index.html", todoItems = todoTitles)


if __name__ == '__main__':
    app.run()
