import sys

dependencies = ['os','sys', 'math', 'numpy', 'pandas', 'scipy']
missing_dependencies = []

for dependency in dependencies:
    try:
        exec(f"import {dependency}")
        print(f"{dependency} is installed.")
    except ImportError:
        print(f"{dependency} is not installed.")
        missing_dependencies.append(dependency)

if missing_dependencies:
    print("")
    print("The following dependencies are missing:", missing_dependencies)
else:
    print("")
    print("All dependencies are satisfied.")

