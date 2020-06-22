#!/usr/bin/python3

import subprocess
import os
import sys
import time

project_root = "/usr/src/app"

class bcolors:

    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def run():

	requirements_file = os.path.join(project_root, "requirements.txt")

	if not os.path.isfile(requirements_file):
		print("{} App folder does not have the requirements.txt file, you can create it by executing: {}".format(bcolors.WARNING, bcolors.ENDC))
		print("{} pip freeze > requirements.txt {}".format(bcolors.WARNING, bcolors.ENDC))
		sys.exit(os.EX_OSFILE)

	freee_command = ["pip", "freeze", "-r", requirements_file]
	result = subprocess.run(freee_command, 
		stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	if result.returncode != 0:
		print("{0} {1} {2}".format(bcolors.FAIL, result.stderr.decode(), bcolors.ENDC))
		sys.exit(result.returncode)

	if result.stderr:

		uninstalled = result.stderr.decode().strip().split("\n")
		"""
		WARNING: Requirement file [/usr/src/app/requirements.txt] contains request==2019.4.13, but package 'request' is not installed
		I use split to that message, position 67 is where start package name
		"""
		uninstalled = [x.split(",")[0][67:] for x in uninstalled]

		for package in uninstalled:
			if len(package.split("==")) == 1:
				print("{0} WARNING: {1} package does not specify version {2}".format(bcolors.WARNING, package, bcolors.ENDC))

		print("Installing dependencies")
		subprocess.call(["pip", "install", "-r", requirements_file])


	print("{0} All dependencies are installed {1}".format(bcolors.OKGREEN, bcolors.ENDC))


	exec_command(sys.argv)


def exec_command(args: []):
	#['entrypoint.py', 'python', '/usr/src/app/server.py']
	# I delete firts element
	del args[0]
	if args:
		subprocess.run(args)


if __name__ == "__main__":
		run()