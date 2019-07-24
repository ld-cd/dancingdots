# dancingdots

###### A psychophysics experiment by [Aleksandra Sherman](mailto:asherman@oxy.edu), [Carmel Levitan](mailto:levitan@oxy.edu), and [Aled Cuda](mailto:aled@berkeley.edu)

This is the main repository for the dancing dots experiment. This code allows the user to create arbitrary dancing dots displayes based on a robust configuration syntax.

## Installation

Dancing dots has only two dependencies, [python](https://www.python.org/downloads/), and [pyglet](https://pyglet.readthedocs.io/en/pyglet-1.3-maintenance/programming_guide/installation.html), which it uses to draw a graphics accelerated display. In order to play most types of audio pyglet also requires [avbin](https://avbin.github.io/AVbin/Home/Home.html).

Once all of those are installed, simply clone this repository and run `python3 main.py sample_config.json`

## Configuration

In order to tease out the details of this illusion the program was built to be highly configureable. The configuration file has four crucial sections, dotgroups, sounds, and window.

The configuration file is a normal json file with one exception, any field can be replaced with a python expresion by writing the string `"expr:"` followed by some code (ie `"expr:random.choice([0, 1, 2])"`). This allows any of the various parameters to be randomized or minipulated in a multitude of ways. In this environment the python packages `json`, `colorsys`, and `random` are available. In addition the configfile is bound to the variable `config` which allows the configfile to be self modifiying and makes the configuration syntax turing complete. Additionally the random number generator in the environment can be seeded by the `"seed"` parameter at the top of the config to enable consistent trials. It is recommended you look at the `sample_config.json` file to see how this all fits together.

Each of the Three top level groups are evaluated once, and the results of any expressions replace the expressions themselves for all future accesses. Fields in any other location (like dottemplates) are evaluated on every access.

Viewing the top layers a minimal configuration would look like follows:

```json
{
    "seed" : 123,
    "window" : {...},
    "sounds" : [...],
    "dotgroups" : [...]
}
```

### Window configuration

The window section has three pretty self explanatory sections, `width`, `height`, and `bgcolor`:

```json
"window" : {
    "width" : 1920,
    "height" : 1080,
    "bgcolor" : [0, 0, 0]
}
```

Width and Height are simpily pixel counts, `bgcolor` on the other hand is an RGB triplet on a scale from 0 to 1 (so [1.0, 0, 0] would be red for example)

### Sound configuration

The sound system consists of multiple audio samples grouped into a larger track. Each sample will play and loop if necessary for the specified duration (seconds) before moving onto the next sample. Once the end of the track is reached the player loops back to the beginning and repeats the process.

```json
"sounds" : [
    {
        "type" : "file",
        "filename" : "drip.ogg",
        "duration" : 10
    },
    {
        "type" : "file",
        "filename" : "beets.mp3",
        "duration" : 4
    }
]
```

Currently the only clip type is file which has one parameter of its own (filename). However, it is likely that some sort of tone generation will be added in the future. Currently the audio portion of this program is the least configureable, and it is a major target of future improvement.

### Dot Configuration

Each dot has 3 time parameters; `duty`, `phase`, and `period`. Duty and phase are both fractional and on a scale of 0 to 1 represent what percentage of the time the dot is on, and in what part of its cycle it turns on respectivly. The period parameter indicates how long the total on off cycle is in seconds. It also has two spatial parameters `loc` which is a two element list that represents its initial coordinates on the xy plane in pixles, and `radius` which is its radius in pixles. It also has one special parameter `motile` which indicates whether or not the dot should randomize its location on each appearence. There is also a color parameter which works the same as `bgcolor` in the window section.

Dot configuration is split into a template and a groups section. A group must contain at minimum a `count` (number of dots in said group) and dot `template` (which may be empty `{}` if all parameters are specified in the group). Any parameter in the group overides the parameter in the template. Any expression in the group is evaluated only once upon group initilization, wheras any expression in the template is evaluated on the creation of every dot. This allows the creation of a group of dots with a uniform but randomized color, but with randomly distributed radii within the group for example.

```json
"periods" : [
    0.1,
    0.2,
    0.3
],
"template" : {
    "duty" : 0.5,
    "phase" : "expr:random.random()",
    "radius" : 50,
    "loc" : [
        "expr:random.random()*config['window']['width']",
        "expr:random.random()*config['window']['height']"
    ],
    "motile" : true
},
"dotgroups" : [
    {
        "count" : 15,
        "period" : "expr:random.choice(config['periods'])",
        "color" : [0.5, 0.5, 0.2],
        "template" : "expr:config['template']"
    },
    {
        "count" : 15,
        "period" : "expr:random.choice(config['periods'])",
        "color" : "expr:[random.random() for i in range(3)]",
        "template" : "expr:config['template']"
    }
]
```

The Dot Configuration above shows vigorous use of expressions. For example the template for both dot groups is the same, and it is shared by an expression that replaces itself with a reference to the part of the config labeled template. Additionally we can see an expression that replaces itself with a randomly selected period from the list in the config file.