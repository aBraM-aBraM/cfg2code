

def to_c(data: dict):
    python_to_c_type = {int: lambda value: "\tint {name};",
                         str: lambda value: "\tchar {name}" + f"[{len(value)}];",
                           bool: lambda value: "\tbool {name};"}

    content = []
    for name, value in data.items():
        if type(value) == dict:
            content.append(f"struct {name} {{\n{to_c(value)}\n}};")
        else:
            content.append(python_to_c_type[type(value)](value).format(name=name))
    content = f"\n".join(content)

    return content

file_extension_to_func = {"h": to_c}