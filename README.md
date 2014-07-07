Chunkymator
===========

A CVF generator for Chunky

Requirements: python 2.x, numpy, scipy, and a batch of jsons from Chunky.

Usage
=====
Create a couple of scenes in chunky that differ only in their x,y,z positions and camera angles (pitch, yaw).
Other attributes are not currently interpolated.
Once that's done, fire up morph.py, enter the number of scenes, and drag/drop or type the (absolute) filepaths of each scene.
If all went well, morph.py should start spewing out coordinate data for the interpolated frames, 
once that's done, it will start saving the generated .jsons as interpolated<N>.json.

Then use chunkys command-line render tool to render all of the files.

Rendering
=========
Use python to iterate over all the output files and invoke chunky.
Pseudocode:
```
for i in range(NumberOfFramesGenerated):
    subprocess.call(["java", "-jar", "/path/to/ChunkyLauncher.jar", "-render", "interpolated-"+str(i), "-scene-dir /directory/specified/for/outputs/", "-target 5"])
```
