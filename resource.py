
class Resource():

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return '-i {}'.format(self.path)


class Resources(list):

    def add(self, path):
        self.append(Resource(path))

    def append(self, resource):
        resource.number = len(self)
        super().append(resource)

    def __delitem__(self, index):
        for resource in self[index:]:
            resource.number -= 1
        super().__delitem__(index)

    def __str__(self):
        return ' '.join(str(r) for r in self)

