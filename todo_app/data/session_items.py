from flask import session
from operator import itemgetter, attrgetter

_DEFAULT_ITEMS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo items' },
    { 'id': 2, 'status': 'Not Started', 'title': 'Allow new items to be added' }
]


def get_items():
    """
    Fetches all saved items from the session.

    Returns:
        list: The list of saved items.
    """
    return session.get('items', _DEFAULT_ITEMS)


def get_item(id):
    """
    Fetches the saved item with the specified ID.

    Args:
        id: The ID of the item.

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    items = get_items()
    return next((item for item in items if item['id'] == int(id)), None)


def add_item(title):
    """
    Adds a new item with the specified title to the session.

    Args:
        title: The title of the item.

    Returns:
        item: The saved item.
    """
    items = get_items()

    # Determine the ID for the item based on that of the previously added item
    id = items[-1]['id'] + 1 if items else 0

    item = { 'id': id, 'title': title, 'status': 'Not Started' }

    # Add the item to the list
    items.append(item)
    session['items'] = items

    return item


def save_item(item):
    """
    Updates an existing item in the session. If no existing item matches the ID of the specified item, nothing is saved.

    Args:
        item: The item to save.
    """
    existing_items = get_items()
    updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]

    session['items'] = updated_items

    return item


def clear_items():
    """
    Removes all entries from the session cookie
    """

    session['items'] = []

    return


def clear_item(id):
    """
    Removes a single item, specified by its ID in the list of existing items
    """
    
    # Get the item for reference before it is deleted
    cleared_item = get_item(id)

    # Get all items and clear only the specified item
    existing_items = get_items()
    updated_items = [existing_item for existing_item in existing_items if existing_item['id'] != id]

    session['items'] = updated_items

    return cleared_item


def update_item_status(id, new_status):
    """
    Update the status of the specified item in the list with the supplied string.

    Args:
        new_status: A string providing the status to be updated
        id: an integer which identifies the item from the list

    """
    selected_item = get_item(id)

    selected_item['status'] = new_status

    save_item(selected_item)

    return


def sort_items():
    """
    Function to sort items based on their status:
    Not Started > In Progress > Completed
    """

    # Get the current, unsorted list of items
    current_items = get_items()

    # Note that conveniently, we want reverse alphabetical order, but decorators might be more robust here?
    sorted_items = sorted(current_items, key=itemgetter('status'), reverse = 1)

    session['items'] = sorted_items

    return