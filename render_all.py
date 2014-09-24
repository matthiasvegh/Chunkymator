#!/usr/bin/env python
import subprocess
import optparse
import os


def get_command(scene, chunkyPath, target):
    dirname = os.path.dirname(scene)
    filename = os.path.basename(scene)

    return ["java", "-jar", chunkyPath, "-render", filename, "-scene-dir", dirname, "-target", target]


def get_commands(scenes, chunkyPath, target):
    return [get_command(scene, chunkyPath, target) for scene in scenes]


def run_command(command, dryRun=None):

    if dryRun is not None:
        print command
        return


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
    parser.add_option("-n", "--dry-run", dest="dryRun",
                      default=False,
                      help="Do not actually run commands, just print them",
                      metavar="BOOL")

    (options, scenes) = parser.parse_args()
    if options.chunky is None:
        print "You must supply the path to Chunky-Launcher.jar"
        return 1

    commands = get_commands(scenes, options.chunky, options.target)
    for command in commands:
        run_command(command, options.dryRun)

if __name__ == "__main__":
    main()
