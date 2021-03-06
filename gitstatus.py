#!/usr/bin/env python
from __future__ import print_function
from subprocess import Popen, PIPE
import sys

# change this symbol to whatever you prefer
prehash = ':'

def getStatus():
	git_status_call = Popen(['git', 'status', '--porcelain', '--branch'], stdout=PIPE, stderr=PIPE)
	gitOutput, error = git_status_call.communicate()

	error_string = error.decode('utf-8')
	gitOutput = gitOutput.decode('utf-8')

	if 'fatal' in error_string:
		return


	#TODO parse gitOutput for this
	branch = Popen(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=PIPE, stderr=PIPE).communicate()[0].decode("utf-8").replace('\n', '')

	splitOutput = gitOutput.replace(']', '').replace(',', '').split('\n')

	stats = [line[:2] for line in splitOutput]

	nb_staged = 0
	nb_changed = 0
	nb_untracked = 0
	nb_conflicts = 0

	for entry in stats:
		if entry == ' M':
			nb_changed += 1
		elif entry == 'M ':
			nb_staged += 1
		elif entry == '??':
			nb_untracked += 1
		elif entry == 'A ':
			nb_staged += 1
		elif entry == 'UU':
			nb_conflicts += 1


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


if __name__ == "__main__":
	getStatus()
