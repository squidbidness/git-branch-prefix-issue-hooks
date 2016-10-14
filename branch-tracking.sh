#!/bin/bash
if [ "$#" -lt 1 ]
then
	git rev-parse --abbrev-ref @{u}
else
	git branch --set-upstream-to "$1"
fi
