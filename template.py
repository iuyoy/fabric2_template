# coding: utf-8
import os
import threading

from fabric import Connection
from fabric import ThreadingGroup as Group

ALLOW_FUNCTIONS = ['sudo', 'run', 'put']


def connect(hosts):
    group = Group(*hosts)
    return group


def thread_run(group, function, cmd, kwargs):
    if function in ALLOW_FUNCTIONS:
        try:
            threads = list()
            # different hosts run different command.
            if type(cmd) is list:
                assert len(group) == len(cmd) and len(group) == len(kwargs),\
                    "Host number, command number and kwargs number are not same."
                for connection, cmd, kwargs in zip(group, cmd, kwargs):
                    thread = threading.Thread(
                        target=getattr(connection, function),
                        args=(cmd,),
                        kwargs=kwargs
                    )
                    threads.append(thread)
            # different hosts run same command
            else:
                for connection in group:
                    thread = threading.Thread(
                        target=getattr(connection, function),
                        args=(cmd, ),
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
        cmds = operation[0]
        function = operation[1] if len(operation) > 1 else 'run'
        kwargs = operation[2] if len(operation) > 2 else {}
        # files are uploaded to ~/ by default
        if type(cmds) is str:
            for cmd in cmds.splitlines():
                print("\nexcute: {} {}".format(function, cmd))
                thread_run(group, function=function, cmd=cmd, kwargs=kwargs)
        elif type(cmds) is list:
            if type(kwargs) is not list:
                kwargs = [kwargs]*len(cmds)
            print("\nexcute diff commands, example: {} {}".format(
                function, cmds[0]))
            thread_run(group, function=function, cmd=cmds, kwargs=kwargs)


def test_connection(hosts):
    for host in hosts:
        print(host)
        with Connection(host) as c:
            try:
                c.run('hostname')
            except Exception as e:
                print("Error:", e)


if __name__ == '__main__':
    hosts = ['user@host1:port', 'user@host2:port']

    test_connection(hosts)

    operations = [
        ['./test1.md', 'put', {}],
        ['whoami'],
        ['whoami', 'sudo'],
        ['whoami', 'sudo', {'user': 'another_user'}],
        ["""cat ~/test1.md
whoami"""],
        [['./test1.md', './test2.md'], 'put',
            [{'remote': '1.txt'}, {'remote': '2.txt'}]],

        [['cat 1.txt', 'cat 2.txt']],
    ]

    parallelly_run(hosts, operations)
