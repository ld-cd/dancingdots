import json, colorsys, random, itertools

import dot, sound

def open_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def ep(prop, config = None):
    if type(prop) == str and len(prop) >=5 and prop[0:5] == "expr:":
        return eval(prop[5:])
    return prop

def generate_dot(dotgroup, window_size, config):
    ek = lambda p: dotgroup[p] if p in dotgroup else (ep(dotgroup['template'][p], config) if p in dotgroup['template'] else None)
    args = {i:ek(i) for i in ['loc', 'radius', 'color', 'period', 'phase', 'duty', 'motile'] if ek(i) != None}
    args['window_size'] = window_size
    args['loc'] = [ep(i, config) for i in args['loc']]
    return dot.Dot(**args)

def generate_dots(config, scene):
    dots = []
    for i in config['scenes'][scene]['dots']:
        dots.extend([generate_dot(i, [config['window']['width'], config['window']['height']], config) for _ in range(i['count'])])
    return dots

def generate_tracks(config, scene):
    return [sound.make_player(config['scenes'][scene]['sounds'])]

def read_config(config):
    if 'seed' in config:
        config['seed'] = ep(config['seed'], config)
        random.seed(config['seed'])
    config['window'] = {i:ep(config['window'][i], config) for i in ep(config['window'], config)}
    for i in config['scenes']:
        config['scenes'][i]['dots'] = [{i:ep(k[i], config) for i in ep(k, config)} for k in ep(config['scenes'][i]['dots'], config)]
        config['scenes'][i]['sounds'] = [{i:ep(k[i], config) for i in ep(k, config)} for k in ep(config['scenes'][i]['sounds'], config)]
    return config