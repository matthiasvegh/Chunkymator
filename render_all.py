#!/usr/bin/env python
import subprocess
import optparse

def get_commands(scenes, chunkyPath, target):
    pass

def main():

    parser = optparse.OptionParser(
            usage="%prog [options] scene1 scene2 ...",
            description="Batch renderer for Chunky.")
    parser.add_option("-t", "--target", dest="target",
            default=1, type=int,
            help="How many SPP to render frames at.",
            metavar="NUM")
    parser.add_option("-c", "--chunky-jar", dest="chunky",
            type=str, help="Location of Chunky-Launcher.jar",
            metavar="FILE")

    (options, scenes) = parser.parse_args()
    if options.chunky is None:
        print "You must supply the path to Chunky-Launcher.jar"
        return 1

    for scene in scenes:
        print scene

if __name__ == "__main__":
    main()
