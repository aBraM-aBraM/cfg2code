from anytree import Node, RenderTree

STRUCT_NAME_PLACEHOLDER = "XX_STRUCT_NAME_PLACEHOLDER_XX"
INSTANCE_NAME_PLACEHOLDER = "XX_INSTANCE_NAME_PLACEHOLDER_XX"

def dict_to_tree(data_dict, parent=None):
    if parent is None:
        root = Node("Root")
        parent = root
    else:
        root = None

    for key, value in data_dict.items():
        if isinstance(value, dict):
            node = Node(key, parent=parent)
            dict_to_tree(value, parent=node)
        else:
            Node(key, parent=parent, data=value)

    return root

def c_declaration(tree: Node):
    python_to_c_type = {int: lambda value: "\tint {name};",
                         str: lambda value: "\tchar {name}" + f"[{len(value)}];",
                           bool: lambda value: "\tbool {name};"}

    content = []

    if tree.parent is None:
        content.append(f"struct {STRUCT_NAME_PLACEHOLDER} {{")

    for child in tree.children:
        if type(child.data) == dict:
            content.append(f"struct {{\n{c_declaration(child)}\n}} {child.name};\n")
        else:
            content.append(python_to_c_type[type(child.data)](child.data).format(name=child.name))
    content = f"\n".join(content)

    if tree.parent is None:
        content += (f"\n}};\ntypedef struct {STRUCT_NAME_PLACEHOLDER} {STRUCT_NAME_PLACEHOLDER};\n")

    return content


def c_definition(tree: Node):
    content = []

    for child in tree.children:
        if type(child.data) == dict:
            content.append(f"{{{c_definition(child.data)}}}")
        else:
            if type(child.data) == str:
                child.data = f"\"{child.data}\""
            content.append(str(child.data))
    
    content = f", ".join(content)
    
    if tree.parent is None:
        content = f"{STRUCT_NAME_PLACEHOLDER} {INSTANCE_NAME_PLACEHOLDER} = {{" + content + f"}};\n"
    
    return content

def to_c(data: dict, typename, instance):
    tree = dict_to_tree(data)
    out = c_declaration(tree) + c_definition(tree)
    return out.replace(STRUCT_NAME_PLACEHOLDER, typename).replace(INSTANCE_NAME_PLACEHOLDER, instance)

file_extension_to_func = {"h": to_c}