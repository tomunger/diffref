import sys
import os
import json
import argparse

import datadiff


def diffFiles (leftFile, rightFile):
	try:
		with open(leftFile, 'r') as fp:
			left = json.load(fp)
	except Exception as e:
		print "{}:  Error reading left file: {}".format(leftFile, e.message if e.message else " ".join(e.args))
		return False
	try:
		with open(rightFile, 'r') as fp:
			right = json.load(fp)
	except Exception as e:
		print "{}:  Error reading right file: {}".format(rightFile, e.message if e.message else " ".join(e.args))
		return False


	try:
		dd = datadiff.diff(left, right, fromfile=leftFile, tofile=rightFile, context=10000)
	except TypeError as e:
		print "{} - {}: Error: {}".format(leftFile, rightFile, e.message if e.message else " ".join(e.args))
		return False

	isMatch = not bool(dd)
	if isMatch:
		print "{} - {}: Match".format(leftFile, rightFile)
		return True
	print "{} - {}: Differ".format(leftFile, rightFile)
	print str(dd)
	return False



parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, 
								 description=
"""Diff files in two directories
""")

#parser.add_argument('-lf', help='message log file name - required')
parser.add_argument('left', help='left directory')
parser.add_argument('right', help='left directory')

args = parser.parse_args()


try:
	if not os.path.exists(args.left):
		raise Exception ("'{}' not found".format(args.left))
	if not os.path.exists(args.right):
		raise Exception ("'{}' not found".format(args.right))

	isMatch = diffFiles(args.left, args.right)

	if not isMatch:
		sys.exit(1)
	sys.exit(0)

except Exception as e:
	print e.message
sys.exit(-1)


