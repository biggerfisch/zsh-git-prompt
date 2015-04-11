#!/usr/bin/env python
from __future__ import print_function
from subprocess import Popen, PIPE
import sys

# change this symbol to whatever you prefer
prehash = ':'

git_status_call = Popen(['git', 'status', '--porcelain', '--branch'], stdout=PIPE, stderr=PIPE)
gitOutput, error = git_status_call.communicate()

error_string = error.decode('utf-8')

if 'fatal' in error_string:
	sys.exit(0)

# NEED TO FIX AFTER THIS LINE

#TODO parse gitOutput for this
branch = Popen(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=PIPE, stderr=PIPE).communicate()[0]

splitOutput = gitOutput.replace(']', '').split('\n')

stats = [line[:2] for line in splitOutput]

nb_staged = 0
nb_changed = 0
nb_untracked = 0
nb_conflicts = 0

for entry in stats:
	if entry == ' M':
		nb_changed++
	else if entry == 'M ':
		nb_staged++
	else if entry == '??':
		nb_untracked++
	else if entry == 'A ':
		nb_staged++
	else if entry == 'UU':
		nb_conflicts++


staged = str(nb_staged)
conflicts = str(nb_conflicts)
changed = str(nb_changed)
untracked = str(nb_untracked)

splitFirstLine = splitOutput[0].split()

ahead = splitFirstLine[splitFirstLine.index('[ahead')+1] if '[ahead' in splitFirstLine else 0
behind = splitFirstLine[splitFirstLine.index('[behind')+1] if '[behind' in splitFirstLine else 0

if branch == 'HEAD':
	branch = prehash + Popen(['git','rev-parse','--short','HEAD'], stdout=PIPE).communicate()[0].decode("utf-8")[:-1]


out = ' '.join([
	branch,
	str(ahead),
	str(behind),
	staged,
	conflicts,
	changed,
	untracked,
	])
print(out, end='')

