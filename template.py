# coding: utf-8
import os
import threading

from fabric import ThreadingGroup as Group

ALLOW_FUNCTIONS = ['sudo', 'run', 'put']


def connect(hosts):
    group = Group(*hosts)
    return group


def thread_run(group, function, args, kwargs):
    if function in ALLOW_FUNCTIONS:
        try:
            threads = list()
            for connection in group:
                thread = threading.Thread(
                    target=getattr(connection, function),
                    args=args,
                    kwargs=kwargs
                )
                threads.append(thread)
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        except Exception as e:
            print(e)
    else:
        print('Function {} is now allowed.'.format(function))


def parallelly_run(hosts, operations):
    group = connect(hosts)
    for operation in operations:
        function = command[1] if len(command) > 1 else 'run'
        kwargs = command[2] if len(command) > 2 else {}
        # files are uploaded to ~/ by default
        for cmd in command[0].splitlines():
            print("\nexcute: {} {}".format(action, cmd))
            thread_run(group, function=function, args=(file_path,), kwargs={})


if __name__ == '__main__':
    hosts = ['user@host1:port', 'user@host2:port']
    operations = [
        ['./test.md', 'put', {}],
        ['whoami'],
        ['whoami', 'sudo'],
        ['whoami', 'sudo', {'user': 'another_user'}],
        ["""cat ~/test.md
whoami"""],
    ]

    parallelly_run(hosts, operations)
