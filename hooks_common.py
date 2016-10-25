import os
import sys
import re
import sh

git = sh.git.bake(_tty_out=False)

def config_description(config_key):
    return {
            "commitprefix" : "feature name",
            "issue" : "issue number"
    }[config_key]

def config_keys():
    return ["commitprefix", "issue"]

# TODO: Replace this hard-coded list with a configurable set of keys in
# .git/config, with a default set in a version-controlled file (probably factor
# aliases-gitconfig into a more general config file to be included).
def excluded_branch_regexes():
    return ["master", "trunk", "release_.*", "HEAD"]

def get_current_branch():
    try:
        return git("rev-parse", "--abbrev-ref", "HEAD").strip()
    except sh.ErrorReturnCode:
        return None

def get_parent_branch(branch):
    try:
        return git("rev-parse", "--abbrev-ref", "{0}@{{u}}".format(branch)).strip()
    except sh.ErrorReturnCode:
        return None

def is_root_feature_branch(branch):
    parent = get_parent_branch(branch)
    return parent == None or is_excluded_branch(get_parent_branch(branch))

def is_excluded_branch(branch):
    if branch is None:
        return False
    for r in excluded_branch_regexes():
        if re.match(r, branch) != None:
            return True
    return False

def get_branch_config(branch, key):
    return git.config( "--get", "branch.{0}.{1}".format(branch, key) ).strip()

def get_all_branch_config(branch, key):
    return git.config( "--get-all", "branch.{0}.{1}".format(branch, key)
            ).strip().split("\n")

def set_branch_config(branch, key, value):
    return git.config( "branch.{0}.{1}".format(branch, key), value ).strip()
    # TODO: Fix bug here

def has_branch_config(branch, key):
    try:
        git.config( "--get-all", "branch.{0}.{1}".format(branch, key) ).strip()
    except sh.ErrorReturnCode:
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

