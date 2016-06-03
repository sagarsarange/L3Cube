'''
3.Write a program to list duplicate files from hard drive
------------------------------------------------------------------------
The aim of this assignment is to list all the duplicate files from the hard drive and give user option to remove them or merge them.

Usage : python Duplicate.py folder_path
'''
import sys
import os
import hashlib

def compare(similar):
	hashes=[]
	
	#checking hash values of first 20 characters of each file
	#if the first 20 lines are not same then the files are definitely not duplicates
	for file in similar:
		fo=open(file, 'rb')
		h = hashlib.sha1()
		line=fo.read(20)
		h.update(line)
		hashes.append(h.digest())
		fo.close()
	
	#removing files that cannot be duplicates from the list of similar files
	flag=0
	for i in range(0, len(hashes)):
		if flag==1:
			i-=1
		if(hashes.count(hashes[i])==1):
			similar.pop(i)
			hashes.pop(i)
			flag=1
	hashes[:]=[]
	
	#checking hash values of the entire files that can be duplicates
	for file in similar:
		h = hashlib.sha1()
		fo=open(file, 'rb')
		line = 0
       		while line != b'':
           		line=fo.read(1024)
           		h.update(line)
		hashes.append(h.digest())
	
	#generating final list of duplicate files
	flag=0
	for i in range(0, len(hashes)):
		if flag==1:
			i-=1
		if(hashes.count(hashes[i])==1):
			similar.pop(i)
			hashes.pop(i)
			flag=1
	return similar
#----------------------------------------------------------------	
a=dict()
duplicates=dict()

if (sys.argv[1:]):
	arg=sys.argv[1]
else:
	arg="/home"

#traversing the filesystem tree
for root, dirs, files in os.walk(arg, topdown=True):
    for name in files:
        name= root+"/"+name
	
	similar=[]
	statinfo = os.stat(name)
        size=statinfo.st_size
	a.setdefault(size, [])
	a[size].append(name)					#grouping files according to their sizes
	similar=a.get(size)					#files having same size have the posibility of being duplicates
	
	if(len(similar)>1):
		dup=[]
		dup=compare(similar)				#obtaining list of duplicate files from list of same sized files
		for item in dup:
			duplicates.setdefault(size, [])
			if( item not in duplicates[size]):
				duplicates[size].append(item)	#grouping duplicates by size
print 
print
print "Sets of duplicates are:"
for key in duplicates.keys():
	print "------------------------------------------------------------------------"
	print "Duplicate file(s): "
	n=0							# n represents the number of duplicates
	for item in duplicates[key]:
		print n, "" , item
		n=n+1
	print
	ch=raw_input("Merge files??(y) ")
	if(ch=='y'):
		print "Enter the indices of the two files to be merged ( 0 -",i-1,")"
		fl1=int(input("File 1: "))
		fl2=int(input("File 2: "))
		f2 = open(duplicates[key][fl2])
		f2_contents = f2.read()
		f2.close()
		f3 = open(duplicates[key][fl1], "a") 		# open in `a` mode to append
		f3.write(f2_contents) 				# merge the contents
		f3.close()
		os.remove(duplicates[key][fl2])
		del duplicates[key][fl2]
		n=n-1
		print "Files merged."
	if(n > 1):
		print "-------------------------------------"
		print "Duplicate file(s): "
		i=0
		for item in duplicates[key]:
			print i, "" , item
			i=i+1
		print
		ch=raw_input("Delete duplicates??(y) ")
		if(ch=='y'):
			filei=input("Enter file no which should not be deleted: ")
			i=0
			for item in duplicates[key]:
				if(i != filei):
					os.remove(duplicates[key][i])
				i=i+1
			print "Duplicates removed."
		print
