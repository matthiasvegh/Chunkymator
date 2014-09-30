Chunkymator [![Build Status](https://travis-ci.org/matthiasvegh/Chunkymator.png?branch=master)](https://travis-ci.org/matthiasvegh/Chunkymator) [![Code Health](https://landscape.io/github/matthiasvegh/Chunkymator/master/landscape.png)](https://landscape.io/github/matthiasvegh/Chunkymator/master) [![Coverage Status](https://img.shields.io/coveralls/matthiasvegh/Chunkymator.svg)](https://coveralls.io/r/matthiasvegh/Chunkymator?branch=master)
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
- `-o` or `--outputdir` this specifies where to place generated .jsons
- `-f` or `--frame-rate` set this to the framerate you intend to play the animation. (default is 25)
- `-s` or `--traveling-speed` by default, this is 5.4 m/s, which is half of what minecraft's flight speed is.
- `-t` or `--length` in this mode, the length of the animation is not defined by the total distance to be traveled, but is set explicitly.

Camera options
--------------
- `-x` or `--focus-on-x`
- `-y` or `--focus-on-y`
- `-z` or `--focus-on-z`
These switches specify where to point the camera while it is traveling. This is useful is you want to showcase a specific building. If they are left out, camera points in the direction of travel.

Rendering
=========
Use render_all.py to iterate over all the scenes and invoke chunky.
```
./render_all.py -c /path/to/Chunky-Launcher.jar -t 10 /path/to/scene1 /path/to/scene2 ...
```
