git-prefix-issue-hooks
======================

### Hooks and scripts for automatically preparing commit messages with a feature prefix and an issue number from the local branch config.

Place the files in your working directory's .git/hooks sub-directory.  You can do this by cloning the repository directly into that directory, then updates can be installed automatically with `git pull origin master`.

Requires a python installation; assumes the binary is located at `/usr/bin/python`

#### Required git branch config keys `commitprefix` and `issue`

There are two core git config keys used in these hooks: `commitprefix` and `issue`.  `commitprefix` should be a short name to identify the feature or branch with which a commit should be associated.  These are configured per-branch using `git config branch.<branch_name>.(commitprefix|issue)`.  When `commitprefix` is configured for the current git branch, commit messages in the editor or generated with the `git commit -m` command-line switch will be prepended with the `commitprefix` value enclosed in parentheses.  `issue` is any task-tracking (Jira, etc.) issue number associated with the branch.  It will be appended in its own paragraph to the end of the commit message.

In `.git/config`, `commitprefix` or `issue` show up as a per-branch key, for example:

```
[branch "snout\_"]
    remote = ...
    merge = ...
    issue = AN-99435
    commitprefix = snout
```

#### Branch config key warnings

Unless the current branch is one of a number of excluded branch names such as `master` or `trunk`, or `HEAD` for detached head mode, a warning will be output to the console or inserted as a comment in the commit message if either `commitprefix` or `issue` is not set.  These warnings can be turned off for a given branch by setting `git config branch.<branch\_name>.nowarn true` (Note that any value will work, including, counterintuitively, `false`, since what the hook checks is whether the key `nowarn` exists at all).

#### Branch inherited config upon creation/checkout

When a new branch is created, the `post-checkout` hook will check if the new branch is set to track another branch.  If it is, the values for `commitprefix` and `issue` will be inherited from the branch it is tracking, for convenience.  Note that this will happen whenever a non-excluded branch is checked out (unless it already has `commitprefix` and `issue`), not only when it is created.  I find it convenient to set git's configuration so that new branches automatically track the current branch, to take advantage of this feature.

#### Convenince commands/aliases

These hooks come with some convenience aliases for more easily querying and setting `commitprefix` and `issue`, in the file `aliases-gitconfig`.  These aliases need to be included in your git config file, either by manually copying-and pasting the file contents into .git/config, or preferrably by using git's [include] config key in .git/config (assuming your version of git supports it).  This way updates to `aliases-gitconfig` will be picked up automatically:

```
[include]
    path = hooks/aliases-gitconfig
```

The resulting aliases are `git branch-commitprefix` and `git branch-issue`.  Use them without an argument to check the current value, or with an argument to set a new value, similar to how `git config` works.
