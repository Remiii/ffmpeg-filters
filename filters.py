from filter import Filter, Position


DEFAULT_FONT = '/usr/share/fonts/truetype/ttf-dejavu/DejaVuSans-Bold.ttf'
DEFAULT_FONT_COLOR = 'white'
DEFAULT_FONT_SIZE = '20'


class DrawBox(Filter):

    name = 'drawbox'
    args = ['w', 'h', 'color', 't']

    def __init__(self, position=None, **kwargs):
        kwargs.setdefault('color', 'black@0.5')
        kwargs.setdefault('t', 1000)
        super().__init__(position, **kwargs)


class DrawText(Filter):

    name = 'drawtext'
    args = ['fontfile', 'text', 'fontcolor', 'fontsize']
    centered = Position('(W-tw)/2', '(H-th)/2')

    def __init__(self, text, position=None, time_range=None, **kwargs):
        kwargs.setdefault('fontcolor', DEFAULT_FONT_COLOR)
        kwargs.setdefault('fontfile', DEFAULT_FONT)
        kwargs.setdefault('fontsize', DEFAULT_FONT_SIZE)
        super().__init__(position, time_range, text=text, **kwargs)


class Overlay(Filter):

    name = 'overlay'
    args = []
    centered = Position('(W-w)/2', '(H-h)/2')

    def __init__(self, resource, position=None, time_range=None, **kwargs):
        self.resource = resource
        super().__init__(position, time_range, **kwargs)

