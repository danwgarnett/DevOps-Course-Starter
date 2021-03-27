import pytest
from todo_app.data.trello_items import ViewModel

class TestTrelloItem:
    def __init__(self, card_id, card_name, card_list, description):
        self.id = card_id
        self.title = card_name
        self.list = card_list
        self.description = description


@pytest.fixture
def test_list():
    item_1 = TestTrelloItem(1,'new task', {"name":'To Do',"id":1}, '')
    item_2 = TestTrelloItem(2,'new task', {"name":'Doing',"id":2}, '')
    item_3 = TestTrelloItem(3,'new task', {"name":'Done',"id":3}, '')
    item_4 = TestTrelloItem(4,'new task', {"name":'To Do',"id":1}, '')
    item_5 = TestTrelloItem(5,'new task', {"name":'Doing',"id":2}, '')
    item_6 = TestTrelloItem(6,'new task', {"name":'To Do',"id":1}, '')
    items = [item_1, item_2, item_3, item_4, item_5, item_6]

    return items


def test_num_open_items(test_list):
    model_view = ViewModel(test_list)
    assert model_view.num_open_items == 5


def test_get_todo_items(test_list):
    model_view = ViewModel(test_list)
    assert len(model_view.todo_items) == 3
    for item in model_view.todo_items:
        assert item.list["name"] == "To Do"
        assert item.list["name"] != "Doing"
        assert item.list["name"] != "Done"


def test_get_doing_items(test_list):
    model_view = ViewModel(test_list)
    assert len(model_view.doing_items) == 2
    for item in model_view.doing_items:
        assert item.list["name"] != "To Do"
        assert item.list["name"] == "Doing"
        assert item.list["name"] != "Done"

def test_get_done_items(test_list):
    model_view = ViewModel(test_list)
    assert len(model_view.done_items) == 1
    for item in model_view.done_items:
        assert item.list["name"] != "To Do"
        assert item.list["name"] != "Doing"
        assert item.list["name"] == "Done"