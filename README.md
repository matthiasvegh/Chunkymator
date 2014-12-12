Chunkymator [![Build Status](https://travis-ci.org/matthiasvegh/Chunkymator.png?branch=master)](https://travis-ci.org/matthiasvegh/Chunkymator) [![Code Health](https://landscape.io/github/matthiasvegh/Chunkymator/master/landscape.png)](https://landscape.io/github/matthiasvegh/Chunkymator/master) [![Coverage Status](https://img.shields.io/coveralls/matthiasvegh/Chunkymator.svg)](https://coveralls.io/r/matthiasvegh/Chunkymator?branch=master) [![Stories in Ready](https://badge.waffle.io/matthiasvegh/Chunkymator.png?label=ready&title=Ready)](https://waffle.io/matthiasvegh/Chunkymator)
===========

A json generator for Chunky

Requirements: python 2.x, numpy, scipy, and a batch of jsons from Chunky.
A demonstration video is available [here](http://youtu.be/jW9V5HSIIlw)

Usage
=====
Create a couple of scenes in chunky that are of the same map, with same resolution, chunk lists etc.
Most attributes of the scene are interpolated, including camera position, orientation, clouds, sun, colours, intensity and so on.
Once that's done, fire up morph.py, enter the number of scenes, and drag/drop or type the (absolute) filepaths of each scene.
If all went well, morph.py should start spewing out coordinate data for the interpolated frames,
once that's done, it will start saving the generated .jsons as interpolated<N>.json.

Then use chunkys command-line render tool to render all of the files.

Command Line Options
=====================
- `-o` or `--outputdir` this specifies where to place generated .jsons.
- `-f` or `--frame-rate` set this to the framerate you intend to play the animation. (default is 25)
- `-s` or `--traveling-speed` by default, this is 5.4 m/s, which is half of what minecraft's flight speed is.
- `-t` or `--length` in this mode, the length of the animation is not defined by the total distance to be traveled, but is set explicitly.

Camera options
--------------
- `-x` or `--focus-on-x`
- `-y` or `--focus-on-y`
- `-z` or `--focus-on-z`
These switches specify where to point the camera while it is traveling. This is useful is you want to showcase a specific building. If they are left out, camera points in the direction of travel.

Sun movement control
--------------------
- `-S` or `--override-sun` this option turns the sun movement mechanism on,
becuase the time between keyframes is controlled by Chunkymator, the speed of the sun moving across the sky can be difficult to get right.

Consider the following example:

| Sun position | 0 | 1 | 2 | 3 |
|--------------|---|---|---|---|
|      90°     |   |   |   | x |
|      60°     |   |   |   |   |
|      30°     |   |   |   |   |
|       0°     | x | x | x |   |

Using the sun override switch will alter this to become:

| Sun position | 0 | 1 | 2 | 3 |
|--------------|---|---|---|---|
|      90°     |   |   |   | x |
|      60°     |   |   | x |   |
|      30°     |   | x |   |   |
|       0°     | x |   |   |   |

This works as expected for monotonous sequences, but also works for non monotonous ones:

| Sun position | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|--------------|---|---|---|---|---|---|---|
|      90°     |   |   | x |   |   | x |   |
|      45°     |   |   |   |   |   |   |   |
|       0°     | x | x |   | x | x |   | x |

| Sun position | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|--------------|---|---|---|---|---|---|---|
|      90°     |   |   | x |   |   | x |   |
|      45°     |   | x |   | x |   |   |   |
|       0°     | x |   |   |   | x |   | x |

In the latter case, monotonous sections are discovered and then linearized.

Rendering
=========
Use render_all.py to iterate over all the scenes and invoke chunky.
```
./render_all.py -c /path/to/Chunky-Launcher.jar -t 10 /path/to/scene1 /path/to/scene2 ...
```
