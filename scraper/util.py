
class classproperty(object):  # noqa
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)


def traverse_dict(original_dict):
    traversed = {}
    for name, accounts in original_dict.items():
        for account in accounts:
            traversed[account] = name

    return traversed
