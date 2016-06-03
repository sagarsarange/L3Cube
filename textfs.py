'''
4) Textfs - A text based file system

Mr. Ramesh, programmer by profession is very obsessed with his room partner Mr. Suresh.  Suresh leaves no opportunity to break into and check out important and private files of Ramesh. One fine day Ramesh decides to implement his own file system Textfs that could store important files without revealing much information about them. Textfs will be a text based file system meaning all the data regarding contents of file system(meta-data) and the actual data of files will go in a single text file. The only principle that this file system is based on is - simplicity.
As the only factor under consideration is simplicity and not efficiency he decides to write a user mode command line application. This application has following major goals :
1.  Create a new file (create command)
2. Copy content of external files into these newly created files (copy command)
3.  Print contents of internal files (echo command)
4. Delete existing file (delete command)
5. List all files (ls command)

Again in order to keep things simple he agrees on some limitations:
1. Application will only create/copy/print *text* files
2. Application will only allow copying contents from external files(eg : /usr/readme.txt can be copied to readme.txt created by the application); it won't allow editing of contents.
3. Application will act as a command interpreter and accept only five commands create, copy, echo, ls  and delete with relevant parameters ; all text files directly go into Textfs without any folder structure.
4. Textfs will store all the contents inside a single file meaning the minimal super block, the minimal inode list and the storage block will all be placed inside dynamically increasing text file.

Textfs will allow Ramesh to hide all private text files unless and until Suresh gets hold of the application.

'''
import shelve,time,sys,datetime
import random
class File(object):
	def __init__(self,name,type,parent=None,text=''):
		self.list=[]
		self.name=name
		if type=='file':
			self.inode=random.randint(0,100000)
		self.type=type
		self.time=int(time.time())
		self.parent=parent
		self.text=text
	def is_file(self,name):		#function to see if the file exists
		for node in self.list:
			if node.name==name:
				return True
		return False
	def is_dir(self,name):		#function to see if the directory exists
		if(self.is_file(name)) and self.get(name).type=='dir':
			return True
		return False
	def get(self,name):			#returns file name
		for node in self.list:
			if node.name==name:
				return node 
	def add(self,name,type,text=''):	#adds a new file or directory
		self.list.append(File(name,type,self,text))
	def remove(self,name):			#removes a file or directory
		self.list.remove(self.get(name))
	def stat(self):				#prints the list of files and directories
		print 'Listing',self.name
		for node in self.list:
			if node.type=='file':
				print 'Name:',node.name,'\tCreated:',datetime.datetime.fromtimestamp(node.time).strftime('%Y-%m-%d %H:%M:%S'),'\tType:',node.type,'\tInode:',node.inode
			else:
				print 'Name:',node.name,'\tCreated:',datetime.datetime.fromtimestamp(node.time).strftime('%Y-%m-%d %H:%M:%S'),'\tType:',node.type
	def echo(self):				#prints contents of the file 
		print 'Reading file:',self.name
		print "Contents of the file: ",self.text
		return self.text
	def senddata(self):
		return self.text

class FileSystem(object):
	COMMANDS=['ls','mkdir','chdir','rmdir','create','echo','delete','help','copy','cd','exit']
	def __init__(self):
		self.io=shelve.open('file.sys',writeback=True)		#maintains data of the file system like a super block
		if self.io.has_key('fs'):
			self.root=self.io['fs']
		else:
			self.root=File('/','dir')
		self.curr=self.root
		self.tt=self.root
	def mkdir(self,cmd):				#adds a directory
		if len(cmd)<2 or cmd[1]=='':
			print 'mkdir-make directory'
			print 'usage:mkdir <dir_name>'
		else:
			name=cmd[1]
			if self.curr.is_file(name)==False:
				self.curr.add(name,'dir')
			else:
				print 'already exists'
	def chdir(self,cmd):				#to change the directory
		if len(cmd)<2 or cmd[1]=='':
			print 'chdir-change directory'
			print 'usage:chdir <dir_name>'
		else:
			name=cmd[1]
			a=name.split('/')
			for i in a:
				if i == '':
					self.curr=self.tt
				elif i == '..':
					if self.curr.parent is not None:
						self.curr=self.curr.parent
				elif self.curr.is_dir(i):
					self.curr=self.curr.get(i)
				else:
					print 'invalid directory'
		
	def rmdir(self,cmd):				#removes a directory
		if len(cmd)<2 or cmd[1]=='':
			print 'rmdir-remove directory'
			print 'usage:rmdir <dir_name>'
		else:
			name=cmd[1]
			if self.curr.is_dir(name):
				self.curr.remove(name)
				print 'Directory deleted'
			else:
				print 'invalid name'
	def delete(self,cmd):				#removes a file
		if len(cmd)<2 or cmd[1]=='':
			print 'delete-remove file'
			print 'usage:delete <file_name>'
		else:
			name=cmd[1]
			if self.curr.is_file(name) and not self.curr.is_dir(name):
				self.curr.remove(name)
				print 'deleted'
			else:
				print 'invalid'
	def ls(self,cmd):				#lists the files and directories present
		if len(cmd)>1:
			print 'ls-list status'
			print 'usage-ls'
		self.curr.stat()
	def create(self,cmd):				#creates a file
		if len(cmd)<2 or cmd[1]=='':
			print 'create-make file'
			print 'usage:create <file_name>'
		else:
			name=cmd[1]
			if self.curr.is_file(name)==False:
				self.curr.add(name,'file',raw_input("Enter file content:"))
			else:
				print 'already exists'
	def echo(self,cmd):				#prints file contents
		if len(cmd)<2 or cmd[1]=='':	
			print 'echo-read a file'
			print 'usage:echo <file_name>'
		else:
			name=cmd[1]
			if self.curr.is_file(name):
				self.curr.get(name).echo()
			else:
				print 'invalid'
	def copy(self,cmd):				#copies file content from one file to another
		if len(cmd)<3 or cmd[1]=='':
			print 'copy-copy files'
			print 'usage:copy <new file> <old file>'
		else:
			temp=self.curr
			a=cmd[2].split('/')
			for i in a:
				if i=='.':
					continue	
				elif i=='':
					self.curr=self.tt
				else:
					if self.curr.is_dir(i):
						self.curr=self.curr.get(i)	
					elif self.curr.is_file(i):
						name1=cmd[1]
						obj=self.curr.get(i)
						temp.add(name1,'file',obj.senddata())
					else:
						print "file does not exist"						
			self.curr=temp		
						
				
	def save(self):						
		self.io['fs']=self.root
		self.io.sync()
	def help(self,cmd):
		print 'Commands : mkdir,chdir,rmdir,ls,create,delete,echo,copy,exit'
	def exit(self,cmd):
		sys.exit(0)
def main():
	fs=FileSystem()				
	while True:
		cmd=raw_input('> ').split(' ')
		method=None
		try:
			method=getattr(fs,cmd[0])
		except AttributeError:
			print'Invalid command'
		if method is not None and cmd[0] in FileSystem.COMMANDS and callable(method):
			method(cmd)
			fs.save()
		else:	
			print'Invalid command'
main()
