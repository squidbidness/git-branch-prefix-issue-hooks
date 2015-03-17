import sys
import subprocess
import re

#TODO: Refactor prepare-commit-msg in terms of new functions in here
#TODO: Add convenience commands such as 'git config-branch issue [...]'

def config_description(config_key):
    return {
            "commitprefix" : "feature name",
            "issue" : "issue number"
    }[config_key]

def config_keys():
    return ["commitprefix", "issue"]

def excluded_branch_regexes():
    return ["master", "trunk", "release_.*", "HEAD"]

def get_current_branch():
    return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip()

def get_parent_branch(branch):
    return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "{0}@{{u}}".format(branch)]).strip()

def is_root_feature_branch(branch):
    return is_excluded_branch(get_parent_branch(branch))

def is_excluded_branch(branch):
    for r in excluded_branch_regexes():
        if re.match(r, branch) != None:
            return True
    return False

def get_branch_config(branch, key):
    return subprocess.check_output(["git",
                                    "config",
                                    "--get",
                                    "branch.{0}.{1}".format(branch, key)]).strip()

def get_all_branch_config(branch, key):
    return subprocess.check_output(["git",
                                    "config",
                                    "--get-all",
                                    "branch.{0}.{1}".format(branch, key)]
                                  ).strip().split("\n")

def set_branch_config(branch, key, value):
    return subprocess.check_output(["git",
                                    "config",
                                    "branch.{0}.{1}".format(branch, key),
                                    value]).strip()
    # TODO: Fix bug here

def has_branch_config(branch, key):
    try:
        subprocess.check_output(["git",
                                 "config",
                                 "--get-all",
                                 "branch.{0}.{1}".format(branch, key)]).strip()
    except subprocess.CalledProcessError:
        return False

    return True

def do_not_warn_branch_config(branch, key):
    if has_branch_config(branch, "nowarn"):
        return key in get_all_branch_config(branch, "nowarn")
    else:
        return False

def turn_off_warning_instruction(branch, key):
    return ( "This warning can be turned (off|on) for this branch with:\n"
             "    git config (--add|--unset) branch.{branch}.nowarn {key}"
             .format(branch=branch, key=key) )

def no_config_warning(branch, config_key):
    return ( "\n"
             "Warning: No '{config_key}' git config found for "
             "this branch or for a branch it is tracking, so no "
             "{description} will be automatically inserted in "
             "commit messages.  You can configure one with the "
             "command:\n"
             "    git config branch.{branch}.{config_key} [{description}]\n"
             .format( config_key=config_key,
                      description=config_description(config_key),
                      branch=branch )
             + turn_off_warning_instruction(branch, config_key) )

