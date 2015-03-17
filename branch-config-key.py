#!/usr/local/bin/python

from __future__ import print_function
from hooks_common import *
from subprocess import *
import sys

branch = get_current_branch()

if len(sys.argv) == 1:
    print("Error: must specify the config key")
    exit(1)

command = [ "git",
            "config",
            "branch.{0}.{1}".format(branch, sys.argv[1]) ]

if len(sys.argv) > 2:
    command.append( sys.argv[2] )

try:
    output = check_output( command )
except CalledProcessError as e:
    output = e.output
    
print(output)
