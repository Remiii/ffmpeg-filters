#! /usr/bin/env python3

import json
import os
import sys
import time
from urllib import request
from filter import Filter, FilterChain, Position, TimeRange
from filters import DrawBox, DrawText, Overlay
from resource import Resource, Resources


TMP_DIR = '/tmp'
FILTER_TYPES = {
    'box': DrawBox,
    'text': DrawText,
    'overlay': Overlay
}
resources_dict = {}

timestamp = time.time()
resources = Resources()
filters = FilterChain()

if len(sys.argv) < 4:
    print('Usage: ./titles.py <json> <input.mp4> <output.mp4>')
    exit(1)

with open(sys.argv[1]) as f:
    json = json.load(f)

input_path = sys.argv[2]
resource_path = os.path.join(TMP_DIR, input_path + str(timestamp))
os.mkdir(resource_path)

resources.add(input_path)
for i, (filename, url) in enumerate(json.get('resources', {}).items(), start=1):
    resources_dict[filename] = i
    path = url
    if url.startswith('http'):
        path = os.path.join(resource_path, filename)
        with request.urlopen(url) as req:
            with open(path, 'wb') as f:
                f.write(req.read())
    resources.add(path)


for f in json['filters']:
    filter_type = f['type']
    resource = None
    if filter_type == 'overlay':
        resource = resources[resources_dict[f['resource']]]

    pos = f['position']
    position = None
    if 'x' in pos and 'y' in pos:
        position = Position(pos['x'], pos['y'])
    elif 'place' in pos:
        position = pos['place']

    time_range = None
    if 'timestamp' in f:
        time_range = TimeRange(f['timestamp'].get('start'),
                               f['timestamp'].get('end'))

    options = f.get('options', {})

    filters.append(
        FILTER_TYPES[filter_type](position=position, resource=resource,
                                  time_range=time_range, **options),
        layer=pos.get('z', 0)
    )

print('ffmpeg', '-y', '-r 24', resources, filters,
      '\\\n\t-map', '"[{}]"'.format(filters[-1].sink), sys.argv[3])
print('rm -rf', resource_path)

