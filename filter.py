from collections import namedtuple


class Position(namedtuple('Position', ['x', 'y'])):

    def __str__(self):
        return "x='{}':y='{}'".format(*self)


class TimeRange(namedtuple('TimeRange', ['start', 'end'])):

    def __new__(cls, start=None, end=None):
        if start is None:
            start = 0
        if end is None:
            end = 100000
        return cls.__bases__[0].__new__(cls, start, end)

    def __str__(self):
        return 'if(between(t\, {t.start}\, {t.end})\, {{expr}}, NAN)'.format(t=self)


ALIASES = {
    'scroll': Position('mod(-t*50\,W)', 'mod(-t*50\,H)'),
    'ticker': Position('mod(-t*50\,W)', 'H-60'),
    'score_box': Position('iw-130', '20'),
    'score_home': Position('w-50', '30'),
    'score_away': Position('w-50', '60'),
    'team_home': Position('w-120', '30'),
    'team_away': Position('w-120', '60')
}


class Filter(dict):

    resource = None
    centered = Position('W/2', 'H/2')

    def __init__(self, position='', time_range=None, **kwargs):
        super().__init__()
        if isinstance(position, str):
            if position == 'center':
                self.position = self.centered
            elif position in ALIASES:
                self.position = ALIASES[position]
            else:
                raise ValueError('Position "{}" is not supported'.format(position))
        elif isinstance(position, tuple):
            x, y = position
            if x == 'center':
                x, __ = self.centered
            if y == 'center':
                __, y = self.centered
            if x == 'scroll':
                x, __ = ALIASES['scroll']
            if y == 'scroll':
                __, y = ALIASES['scroll']
            self.position = Position(x, y)
        self.time_range = time_range
        self.update({k: v for k, v in kwargs.items() if k in self.args})

    @property
    def position(self):
        if self.time_range:
            x, y = self._position
            return Position(str(self.time_range).format(expr=x), y)
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    def __str__(self):
        params_list = ["{}='{}'".format(k, self[k]) for k in self.args]
        params_list.append(str(self.position))
        params = ':'.join(params_list)
        resource = '[{}]'.format(self.resource.number) if self.resource else ''
        return '{} {}={}'.format(resource, self.name, params)


class FilterChain(list):

    def update_links(self):
        for i, f in enumerate(self):
            f.source = self[i-1].sink if i else '0'
            f.sink = chr(ord(self[i-1].sink) + 1) if i else 'a'

    def insert(self, i, f):
        super().insert(i, f)
        self.update_links()

    def append(self, f, layer=0):
        f.layer = layer
        for i, x in enumerate(self):
            if f.layer > x.layer:
                return self.insert(i, f)
        return self.insert(len(self), f)

    def __delitem__(self, index):
        try:
            self[index + 1].source = self[index].source
        except IndexError:
            pass
        super().__delitem__(index)

    def __str__(self):
        if not self:
            return ''
        filters = (';\n\t'.join('[{f.source}]{f} [{f.sink}]'.
                   format(f=f) for f in self))
        return '-filter_complex \\\n\t"{}"'.format(filters)

