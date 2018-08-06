#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import Nsp
import pathlib
import re

global files
files = {}

global hasScanned
hasScanned = False

def get(key):
	return files[key]
	
def scan(base):
	global hasScanned
	if hasScanned:
		return

	hasScanned = True

	print('scanning ' + base)
	for root, dirs, _files in os.walk(base, topdown=False):
		#for name in dirs:
		#	if name[0] != '.':
		#		scan(root + '/' + name)
			
		for name in _files:
			if pathlib.Path(name).suffix == '.nsp' or pathlib.Path(name).suffix == '.nsx':
				path = os.path.abspath(root + '/' + name)
				if not path in files:
					print('new file found: ' + path)
					files[path] = Nsp.Nsp(path, None)
		save()

def removeEmptyDir(path, removeRoot=True):
	if not os.path.isdir(path):
		return

	# remove empty subfolders
	_files = os.listdir(path)
	if len(_files):
		for f in _files:
			if not f.startswith('.') and not f.startswith('_'):
				fullpath = os.path.join(path, f)
				if os.path.isdir(fullpath):
					removeEmptyDir(fullpath)

	# if folder empty, delete it
	_files = os.listdir(path)
	if len(_files) == 0 and removeRoot:
		print("Removing empty folder:" + path)
		os.rmdir(path)

def load(fileName = 'files.txt', map = ['id', 'path', 'version', 'timestamp']):
	try:
		with open(fileName , encoding="utf-8-sig") as f:
			firstLine = True
			for line in f.readlines():
				line = line.strip()
				if firstLine:
					firstLine = False
					if re.match('[A-Za-z\|\s]+', line, re.I):
						map = line.split('|')
						continue
				t = Nsp.Nsp()
				t.loadCsv(line, map)

				if not t.path:
					continue

				path = os.path.abspath(t.path)

				files[path] = Nsp.Nsp(path, None)
	except:
		pass

def save(fileName = 'files.txt', map = ['id', 'path', 'version', 'timestamp']):
	buffer = ''
	
	buffer += '|'.join(map) + '\n'
	for t in sorted(list(files.values())):
		buffer += t.serialize(map) + '\n'
		
	with open(fileName, 'w', encoding='utf-8') as csv:
		csv.write(buffer)