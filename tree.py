import os

def print_tree(path, indent=""):
    items = sorted(os.listdir(path))

    for index, item in enumerate(items):
        if item.startswith("."):
            continue

        full_path = os.path.join(path, item)
        is_last = index == len(items) - 1

        print(indent + ("└── " if is_last else "├── ") + item)

        if os.path.isdir(full_path):
            print_tree(full_path, indent + ("    " if is_last else "│   "))

print(os.path.basename(os.getcwd()))
print_tree(".")