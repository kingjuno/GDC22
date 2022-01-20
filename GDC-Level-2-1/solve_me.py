import imp
from unittest import result
from helper import *

class TasksCommand:
    TASKS_FILE = "tasks.txt"
    COMPLETED_TASKS_FILE = "completed.txt"

    current_items = {}
    completed_items = []

    def read_current(self):
        try:
            file = open(self.TASKS_FILE, "r")
            for line in file.readlines():
                item = line[:-1].split(" ")
                self.current_items[int(item[0])] = " ".join(item[1:])
            file.close()
        except Exception:
            pass

    def read_completed(self):
        try:
            file = open(self.COMPLETED_TASKS_FILE, "r")
            self.completed_items = file.readlines()
            file.close()
        except Exception:
            pass

    def write_current(self):
        with open(self.TASKS_FILE, "w+") as f:
            f.truncate(0)
            for key in sorted(self.current_items.keys()):
                f.write(f"{key} {self.current_items[key]}\n")

    def write_completed(self):
        with open(self.COMPLETED_TASKS_FILE, "w+") as f:
            f.truncate(0)
            for item in self.completed_items:
                f.write(f"{item}\n")

    def run(self, command, args):
        self.read_current()
        self.read_completed()
        if command == "add":
            return self.add(args)
        elif command == "done":
            return self.done(args)
        elif command == "delete":
            return self.delete(args)
        elif command == "ls":
            return self.ls()
        elif command == "report":
            return self.report()
        elif command == "help":
            return self.help()

    def help(self):
        return (
            """Usage :-
$ python tasks.py add 2 hello world # Add a new item with priority 2 and text "hello world" to the list
$ python tasks.py ls # Show incomplete priority list items sorted by priority in ascending order
$ python tasks.py del PRIORITY_NUMBER # Delete the incomplete item with the given priority number
$ python tasks.py done PRIORITY_NUMBER # Mark the incomplete item with the given PRIORITY_NUMBER as complete
$ python tasks.py help # Show usage
$ python tasks.py report # Statistics""".replace("$", "\n$")
        )

    def add(self, args):
        if len(args) != 2:
            return "Error: Missing tasks string. Nothing added!"
        data = read_task_as_dict()
        if args[0] in data.keys():
            free_ind = int(args[0])
            while str(free_ind) in data.keys():
                free_ind += 1
            for i in range(free_ind, int(args[0]), -1):
                data[str(i)] = data[str(i-1)]
        data[args[0]] = args[1]
        add_task(data)
        return f"Added task: \"{args[1]}\" with priority {args[0]}"

    def done(self, args):
        if len(args) != 1:
            return "Error: Missing NUMBER for marking tasks as done."
        index = [int(i) for i in args]
        results = []
        for ind in index:
            results.append(mark_task_done(ind))
        results = '\n'.join(results)
        return results

    def delete(self, args):
        if len(args) < 1:
            return "Error: Missing NUMBER for deleting tasks."
        index = [int(i) for i in args]
        results = []
        for ind in index:
            results.append(delete_task(ind))
        results = '\n'.join(results)
        return results

    def ls(self):
        data = read_task_as_dict()
        if len(data) == 0:
            return "There are no pending tasks!"
        return printdata(data)

    def report(self):
        return print_report()
