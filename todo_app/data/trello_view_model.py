import datetime


class ViewModel:
    def __init__(self, items):
        self._items = items

        open_items = [item for item in items if item.list["name"] != 'Done']
        self.num_open_items = len(open_items)

        self.show_all_done_items = len(self.done_items) < 5

    @property
    def items(self):
        return self._items

    @property
    def todo_items(self):
        todo_items = [item for item in self._items if item.list["name"] == 'To Do']
        return todo_items

    @property
    def doing_items(self):
        doing_items = [item for item in self._items if item.list["name"] == 'Doing']
        return doing_items

    @property
    def done_items(self):
        done_items = [item for item in self._items if item.list["name"] == 'Done']
        return done_items

    @property
    def filtered_done_items(self):
        filtered_done_items = self.recent_done_items
        if self.show_all_done_items:
            filtered_done_items.extend(self.older_done_items)
        return filtered_done_items

    @property
    def recent_done_items(self):
        today_date = datetime.date.today()
        recent_items = []
        for item in self.done_items:
            ticket_date = item.last_updated
            ticket_date = ticket_date.split('T')[0].split('-')
            ticket_date = datetime.date(int(ticket_date[0]), int(ticket_date[1]), int(ticket_date[2]))
            
            if (today_date - ticket_date).days == 0:
                recent_items.append(item)

        return recent_items

    @property
    def older_done_items(self):
        today_date = datetime.date.today()
        older_items = []
        for item in self.done_items:
            ticket_date = item.last_updated
            ticket_date = ticket_date.split('T')[0].split('-')
            ticket_date = datetime.date(int(ticket_date[0]), int(ticket_date[1]), int(ticket_date[2]))
            
            if (today_date - ticket_date).days > 0:
                older_items.append(item)

        return older_items