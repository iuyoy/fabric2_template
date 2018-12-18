# Fabric2 template

This is a template for running commands parallelly in multi-servers with python fabric 2.4, because some functions, such as sudo and put, are not implentmented in ThreadingGroup.

## Requirement

    pip install fabric==2.4

## How to use

- test_connection(hosts)
  
    run `hostname` for each host, print exception for failed connection.

    ```python
    hosts = ['user@host1:port', 'user@host2:port']
    ```

- parallelly_run(hosts, operations)

    run commands parallelly

    **supported functions**: connection.run, connection.sudo, connection.put
    ```python
    hosts = ['user@host1:port', 'user@host2:port']

    operations = [
        # [files or commands, function: put, run (default) or sudo, other parameters]
        # or  
        # [ file list or command list, function: put, run (default) or sudo, other parameters (can be dict, if same for all hosts) or other parameter list]
        # Detailed parameters can be found in fabirc.connection.
        ['./test.md', 'put', {}],
        ['whoami'],
        ['whoami', 'sudo'],
        ['whoami', 'sudo', {'user': 'another_user'}],
        ["""cat ~/test.md
    whoami"""],
        [['./test.md', './test.md'], 'put',
            [{'remote': '1.txt'}, {'remote': '2.txt'}]],

        [['cat 1.txt', 'cat 2.txt']],
        ]
    ```

    ```bash
    $ python template.py

    excute: put ./test1.md

    excute: run whoami
    user
    user

    excute: sudo whoami
    root
    root

    excute: sudo whoami
    another_user
    another_user

    excute: run cat ~/test1.md
    hello test 1.
    hello test 1.

    excute: run whoami
    user
    user

    excute diff commands, example: put ./test1.md

    excute diff commands, example: run cat 1.txt
    hello test 2.
    hello test 1.
    ```
