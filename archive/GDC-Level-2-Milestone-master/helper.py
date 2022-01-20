def add_task(data):
    with open('tasks.txt', 'w') as f:
        for key in sorted(data.keys()):
            f.write(f"{key} {data[key]}\n")
        f.close()

def read_task_as_dict():
    try:
        with open('tasks.txt', 'r') as f:
            lines = f.readlines()
        return {line.split()[0]: ' '.join(line.split()[1:]) for line in lines}
    except FileNotFoundError:
        return {}

def read_completed_as_dict():
    try:
        with open('completed.txt', 'r') as f:
            lines = f.readlines()
        return {l: line for l,  line in enumerate(lines)}
    except FileNotFoundError:
        return {}

def delete_task(index):
    data = read_task_as_dict()
    if str(index) not in data.keys():
        print(f"Error: item with priority {index} does not exist. Nothing deleted.")
        return
    else:
        del data[str(index)]
        add_task(data)
        print(f"Deleted item with priority {index}")

def mark_task_done(index):
    data = read_task_as_dict()
    if str(index) not in data:
        print(f"Error: no incomplete item with priority {index} exists.")
        return
    with open('completed.txt', 'a') as f:
        f.write(f"{data[str(index)]}\n")
    del data[str(index)]
    print(f"Marked item as done.")
    add_task(data)

def printdata(data, report = False, comp = False):
    line = 1
    listdata = ""
    for key in sorted(data.keys()):
        if not comp:
            listdata += f"{line}. {data[key]} [{key}]\n"
        else:
            listdata += f"{line}. {data[key]}\n"
        line += 1
    if not report:
        print(listdata)
    else :
        return listdata

def print_report():
    task = read_task_as_dict()
    completed = read_completed_as_dict()
    line = 0
    report = f"Pending : {len(task)}\n"
    report += printdata(task, True)
    report += f"\nCompleted : {len(completed)}\n"
    report += printdata(completed, True, True)
    print(report)