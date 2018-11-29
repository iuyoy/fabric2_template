# Fabric2 template

This is a template for running commands parallelly in multi-servers with python fabric 2.4, because some functions, such as sudo and put, are not implentmented in ThreadingGroup.

## Requirement

    pip install fabric==2.4

## How to use

Support functions: connection.run, connection.sudo, connection.put

```python
operations = [
    # [files or commands, is_upload or is_sudo, other parameters]
    # Detailed parameters can be found in fabirc.connection.
    ['./test.md', 'upload', {}],
    ['whoami'],
    ['whoami', 'sudo'],
    ['whoami', 'sudo', {'user': 'another_user'}],
    ["""cat ~/test.md
whoami"""],
]
```

```bash
$ python template.py

excute: put ./test.md

excute: run whoami
user
user

excute: sudo whoami
root
root

excute: sudo whoami
another_user
another_user

excute: run cat ~/test.md
hello hello.
hello hello.

excute: run whoami
user
user
```
