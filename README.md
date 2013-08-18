Chunkymator
===========

A CVF generator for Chunky

Requirements: python 2.x, numpy, scipy, and a batch of CVFs from Chunky.

Usage
=====
Create a couple of scenes in chunky that differ only in their x,y,z positions and camera angles (pitch, yaw).
Other attributes are not currently interpolated.
Once that's done, fire up morph.py, enter the number of scenes, and drag/drop or type the (absolute) filepaths of each scene.
If all went well, morph.py should start spewing out coordinate data for the interpolated frames, 
once that's done, it will start saving the generated .cvfs as interpolated<N>.cvf.

Then use chunkys command-line render tool to render all of the files.

Rendering
=========
Use bash or powershell to iterate over all the output files and invoke chunky.
Pseudocode:
```
for i in range(NumberOfFramesGenerated):
    if(!os.path.exists("interpolated-"str(i)+".png")):
        #so if we ^C this script and restart it, we won't rerender everything.
        print "rendering "+str(i)
        call(["java", "-jar", "chunky.jar",..., "interpolated-"+str(i)+".cvf"])
```
