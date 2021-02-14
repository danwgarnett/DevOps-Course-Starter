import requests
import os

def main():

    my_board = TrelloBoard()
    print(my_board.user_auth)
    print(my_board.board_items)

    return


class TrelloBoard:

    def __init__(self):

        def get_user_auth(self):

            TRELLO_KEY = os.environ.get('TRELLO_KEY')
            TRELLO_TOKEN = os.environ.get('TRELLO_TOKEN')

            if not(TRELLO_KEY and TRELLO_TOKEN):
                raise ValueError("No authentication data found for Trello API - please add to .env file")

            self.user_auth = {"key":TRELLO_KEY, "token":TRELLO_TOKEN}

            return

        def get_board_id(self):

            response = requests.request(
                "GET",
                "https://api.trello.com/1/members/me/boards?fields=name,url",
                params = self.user_auth)

            user_boards = response.json()
            self.board_id = user_boards[0]["id"]   

            return

        def get_available_lists(self):

            response = requests.request(
                "GET",
                f"https://api.trello.com/1/boards/{self.board_id}/lists?fields=name",
                params = self.user_auth)
            
            board_lists_raw = response.json()
        
            self.board_lists = {}
            [self.board_lists.update({list["name"] : list["id"]}) for list in board_lists_raw]

            return 

        def get_items(self):

            response = requests.request(
                "GET",
                f"https://api.trello.com/1/boards/{self.board_id}/cards",
                params = self.user_auth)
            
            board_cards = response.json()
            self.board_items = [parse_item(self, card) for card in board_cards]

            return

        get_user_auth(self)
        get_board_id(self)
        get_available_lists(self)
        get_items(self)


    def add_item(self, new_card_name, new_card_list = "To Do"):

        board_lists = self.board_lists
        todo_list_id = board_lists[new_card_list]

        params = self.user_auth
        params.update({"name" : new_card_name})
        params.update({"idList" : todo_list_id})

        response = requests.request(
            "POST",
            f"https://api.trello.com/1/cards/",
            params = params)

        new_card = response.json()
        item = parse_item(self, new_card)

        return item

    def get_item(self, card_id):

        response = requests.request(
            "GET",
            f"https://api.trello.com/1/cards/{card_id}",
            params = self.user_auth)
        
        card = response.json()
        item = parse_item(self, card)

        return item


def parse_item(board, card):

    def get_list_name(board, list_id):

        response = requests.request(
            "GET",
            f"https://api.trello.com/1/lists/{list_id}",
            params = board.user_auth)

        list_data = response.json()
        list_name = list_data["name"]

        return list_name

    card_id = card["id"]
    card_name = card["name"]

    list_id = card["idList"]
    card_list = {"name" : get_list_name(board, list_id) , "id" : list_id}

    item = TrelloItem(board, card_id, card_name, card_list)

    return item


class TrelloItem:

    def __init__(self, board, card_id, card_name, card_list):

        self.user_auth = board.user_auth
        self.board_id = board.board_id
        self.available_lists = board.board_lists
        self.id = card_id
        self.title = card_name
        self.list = card_list
        # self.description = ""
        # self.due_date = ""


    def update_item_status(self, new_status):

        board_lists = self.available_lists
        new_list_id = board_lists[new_status]
        list_update = {"idList" : new_list_id}

        params = self.user_auth
        params.update(list_update)

        response = requests.request(
            "PUT",
            f"https://api.trello.com/1/cards/{self.id}",
            params = params)

        return response


    def clear_item(self):
    
        response = requests.request(
            "DELETE",
            f"https://api.trello.com/1/cards/{self.id}",
            params = self.user_auth)

        return


if __name__ == '__main__':
    main()