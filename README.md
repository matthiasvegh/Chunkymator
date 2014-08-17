Chunkymator [![Build Status](https://travis-ci.org/matthiasvegh/Chunkymator.png?branch=master)](https://travis-ci.org/matthiasvegh/Chunkymator)
===========

A json generator for Chunky

Requirements: python 2.x, numpy, scipy, and a batch of jsons from Chunky.

Usage
=====
Create a couple of scenes in chunky that differ only in their x,y,z positions and camera angles (pitch, yaw).
Other attributes are not currently interpolated.
Once that's done, fire up morph.py, enter the number of scenes, and drag/drop or type the (absolute) filepaths of each scene.
If all went well, morph.py should start spewing out coordinate data for the interpolated frames, 
once that's done, it will start saving the generated .jsons as interpolated<N>.json.

Then use chunkys command-line render tool to render all of the files.

Command Line Options
=====================
- `-o` or `--outputdir` this specifies where to place generated .jsons
- `-f` or `--frame-rate` set this to the framerate you intend to play the animation. (default is 25)
- `-s` or `--traveling-speed` by default, this is 5.4 m/s, which is half of what minecraft's flight speed is.

Camera options
--------------
- `-x` or `--focus-on-x`
- `-y` or `--focus-on-y`
- `-z` or `--focus-on-z`
These switches specify where to point the camera while it is traveling. This is useful is you want to showcase a specific building. If they are left out, camera points in the direction of travel.

Rendering
=========
Use python to iterate over all the output files and invoke chunky.
Pseudocode:
```
for i in range(NumberOfFramesGenerated):
    subprocess.call(["java", "-jar", "/path/to/ChunkyLauncher.jar", "-render", "interpolated-"+str(i), "-scene-dir /directory/specified/for/outputs/", "-target 5"])
```
