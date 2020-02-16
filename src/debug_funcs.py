EXTRA_DEBUG = True


def print_if_cond(condition, *arg):
    if condition:
        print(*arg)


def pause_if_cond(condition, *arg):
    if condition:
        print(*arg)
        input()

