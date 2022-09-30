class Task:

    def __init__(self, id, description, done, date):
        self.id = id
        self.description = description
        self.done = done
        self.date = date

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def get_done(self):
        return self.done

    def get_date(self):
        return self.date


class Topic:

    def __init__(self, id, description, tasks, date):
        self.id = id
        self.description = description
        self.tasks = tasks
        self.date = date

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def get_tasks(self):
        return self.tasks

    def get_date(self):
        return self.date
