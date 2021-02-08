import requests
from pprint import pprint 

def main():

    board_id = get_boards()
    items = get_items(board_id)

    pprint(items)

    get_available_lists(board_id)

    get_card_board(items[1]["id"])
    print(complete_item(items[1]["id"]))

    return


def get_user_auth():

    # This is a draft workaround until the information is saved in the environment files.
    with open('todo_app/USER_INFO','rt') as cfg_file:
        cfg_lines = cfg_file.read().split('\n')
    
    key = cfg_lines[0].split(':')
    token = cfg_lines[1].split(':')

    user_auth = {"key":key[1], "token":token[1]}

    return user_auth


def get_boards():

    user_auth = get_user_auth()

    response = requests.request(
        "GET",
        "https://api.trello.com/1/members/me/boards?fields=name,url",
        params = user_auth)

    user_boards = response.json()
    board_id = user_boards[0]["id"]   

    return board_id


def parse_item(card):

    card_id = card["id"]
    card_name = card["name"]

    list_id = card["idList"]
    card_list = get_list_name(list_id)

    item = {"id" : card_id,
            "status" : card_list,
            "title" : card_name}

    return item


def get_items(board_id):

    user_auth = get_user_auth()

    response = requests.request(
        "GET",
        f"https://api.trello.com/1/boards/{board_id}/cards",
        params = user_auth)
    
    board_cards = response.json()
    items = [parse_item(card) for card in board_cards]

    # for card in board_cards: 
    #     item = parse_item(card)
    #     items.append(item)

    return items


def get_item(card_id):

    user_auth = get_user_auth()

    response = requests.request(
        "GET",
        f"https://api.trello.com/1/cards/{card_id}",
        params = user_auth)
    
    card = response.json()
    item = parse_item(card)

    return item


def get_list_name(list_id):

    user_auth = get_user_auth()

    response = requests.request(
        "GET",
        f"https://api.trello.com/1/lists/{list_id}",
        params = user_auth)

    list_data = response.json()
    list_name = list_data["name"]

    return list_name


def get_available_lists(board_id):

    user_auth = get_user_auth()

    response = requests.request(
        "GET",
        f"https://api.trello.com/1/boards/{board_id}/lists?fields=name",
        params = user_auth)
    
    board_lists_raw = response.json()
 
    board_lists = {}
    [board_lists.update({list["name"] : list["id"]}) for list in board_lists_raw]

    return board_lists


def get_card_board(card_id):

    user_auth = get_user_auth()

    response = requests.request(
        "GET",
        f"https://api.trello.com/1/cards/{card_id}/board?fields=name",
        params = user_auth)
    
    card_board = response.json()

    return card_board


def add_item(board_id, card_name):

    user_auth = get_user_auth()

    board_lists = get_available_lists(board_id)
    todo_list_id = board_lists["Not Started"]

    params = user_auth
    params.update({"name" : card_name})
    params.update({"idList" : todo_list_id})

    response = requests.request(
        "POST",
        f"https://api.trello.com/1/cards/",
        params = params)

    new_card = response.json()
    new_item = parse_item(new_card)

    return new_item


def complete_item(card_id):

    user_auth = get_user_auth()

    card_board = get_card_board(card_id)
    board_id = card_board["id"]

    board_lists = get_available_lists(board_id)
    done_list_id = board_lists["Done"]
    list_update = {"idList" : done_list_id}

    params = user_auth
    params.update(list_update)

    response = requests.request(
        "PUT",
        f"https://api.trello.com/1/cards/{card_id}",
        params = params)

    return response


def update_item_status(card_id, new_status):

    user_auth = get_user_auth()

    card_board = get_card_board(card_id)
    board_id = card_board["id"]

    board_lists = get_available_lists(board_id)
    new_list_id = board_lists[new_status]
    list_update = {"idList" : new_list_id}

    params = user_auth
    params.update(list_update)

    response = requests.request(
        "PUT",
        f"https://api.trello.com/1/cards/{card_id}",
        params = params)

    return response


def clear_item(card_id):

    cleared_item = get_item(card_id)

    user_auth = get_user_auth()

    response = requests.request(
        "DELETE",
        f"https://api.trello.com/1/cards/{card_id}",
        params = user_auth)

    return cleared_item


if __name__ == '__main__':
    main()