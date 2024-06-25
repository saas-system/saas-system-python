class Hongwei(object):
    name = 'hongwei'
    age = 41

    def __init__(self):
        self.gender = 'male'

    def keys(self):
        return ['name']

    def __getitem__(self, item):
        return getattr(self, item)


o = Hongwei()
print(dict(o))
