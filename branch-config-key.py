#!python

from __future__ import print_function
from hooks_common import *
import sh
import sys

branch = get_current_branch()

if len(sys.argv) == 1:
    print("Error: must specify the config key")
    exit(1)

command_args = [ "branch.{0}.{1}".format(branch, sys.argv[1]) ]
if len(sys.argv) > 2:
    command_args.append( sys.argv[2] )

try:
    output = git.config( *command_args )
except sh.ErrorReturnCode as e:
    output = e.stderr
    
print(output)
