import pytest
import datetime
from todo_app.data.trello_view_model import ViewModel

class TrelloItem:
    def __init__(self, card_id, card_name, card_list, description, last_updated):
        self.id = card_id
        self.title = card_name
        self.list = card_list
        self.description = description
        self.last_updated = last_updated

def make_date_string(updated_today = False):
    if updated_today:
        date_string = datetime.date.today().strftime("%Y-%m-%d") 
    else:
        date_string = "2021-03-21"

    time_string = "T19:00:47.551Z"
    datetime_string = date_string + time_string

    return datetime_string

def create_test_list(num_items, status, updated_today):
    datetime_string = make_date_string(updated_today = updated_today)

    items = []
    for i in range(1,num_items + 1):
        item = TrelloItem(i,'new task', {"name":status,"id":1}, '', datetime_string)
        items.append(item)

    return items

@pytest.fixture
def short_test_list():
    items = []
    items.extend(create_test_list(3, 'To Do', False))
    items.extend(create_test_list(2, 'Doing', False))
    items.extend(create_test_list(1, 'Done', False))
    return items


def test_num_open_items(short_test_list):
    model_view = ViewModel(short_test_list)
    assert model_view.num_open_items == 5


def test_get_todo_items(short_test_list):
    model_view = ViewModel(short_test_list)
    assert len(model_view.todo_items) == 3
    for item in model_view.todo_items:
        assert item.list["name"] == "To Do"
        assert item.list["name"] != "Doing"
        assert item.list["name"] != "Done"

def test_get_doing_items(short_test_list):
    model_view = ViewModel(short_test_list)
    assert len(model_view.doing_items) == 2
    for item in model_view.doing_items:
        assert item.list["name"] != "To Do"
        assert item.list["name"] == "Doing"
        assert item.list["name"] != "Done"

def test_get_done_items(short_test_list):
    model_view = ViewModel(short_test_list)
    assert len(model_view.done_items) == 1
    for item in model_view.done_items:
        assert item.list["name"] != "To Do"
        assert item.list["name"] != "Doing"
        assert item.list["name"] == "Done"


def test_show_all_done_items(short_test_list):
    model_view = ViewModel(short_test_list)
    assert model_view.show_all_done_items == True

    model_view.show_all_done_items = False
    assert model_view.show_all_done_items == False

    model_view.show_all_done_items = True
    assert model_view.show_all_done_items == True

def test_show_all_done_items_GT5():
    # req: fewer than 5 completed, show all, otherwise show only those completed today
    test_list = []
    test_list.extend(create_test_list(3,'Done',False))
    test_list.extend(create_test_list(6,'Done',True))
    model_view = ViewModel(test_list)

    assert model_view.show_all_done_items == False

def test_show_all_done_items_LT5():
    # req: fewer than 5 completed, show all, otherwise show all completed today
    test_list = []
    test_list.extend(create_test_list(3,'Done',False))
    test_list.extend(create_test_list(1,'Done',True))
    model_view = ViewModel(test_list)

    assert model_view.show_all_done_items == True

def test_get_recent_done_items():
    test_list = []
    test_list.extend(create_test_list(3,'Done',False))
    test_list.extend(create_test_list(6,'Done',True))
    model_view = ViewModel(test_list)

    recent_items = model_view.recent_done_items
    assert len(recent_items) == 6

def test_get_older_done_items():
    test_list = []
    test_list.extend(create_test_list(3,'Done',False))
    test_list.extend(create_test_list(6,'Done',True))
    model_view = ViewModel(test_list)
    older_items = model_view.older_done_items
    assert len(older_items) == 3