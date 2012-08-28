# -*- coding:utf-8 -*-
## kokof/kokof.py
##
## Copyright (C) 2009 Daniel Faucon <koolfy AT geekmx.org>
##
## Kokof is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; version 3 only.
##
## Kokof is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Kokof. If not, see <http://www.gnu.org/licenses/>.
##

import sys
import socket
import string
import re
from config import *
from input import * 


class Misc:
	'''Miscelaneous useful tools'''
	def isJoin(self, toCheck):
		'''Check if the given chan is in the autojoin list'''
		if toCheck in self.join: 
			return True                 

	def isMaster(self, toCheck):
		'''Check if given person is master'''
		if toCheck[1:] in self.masters:
			return True
		else:
			return False

	def sender(self, toCheck):
		'''Gives the message sender's pseudo'''
		
		self.regexpSender = re.compile('^(.*?)!.*$')
		
		if(self.regexpSender.search(toCheck[1:])):
			self.result = self.regexpSender.findall(toCheck[1:])
			return self.result[0]


class Server(Misc, Config, Input):
	'''Construct needed variables for the server'''
	def __init__(self,\
	             host='irc.geeknode.org',\
		     port=6667,\
	             nick='kokof',\
		     ident='kokof',\
		     realname='kokof',\
		     join='#kokof',\
		     masters='koolfy!koolfy@Koolfy.users.geeknode.org,' + \
		             'roidelapluie!pivo@roidelapluie.users.geeknode.org',\
		     quit='AaArghh.',\
		     die='!die',\
		     version='Kokof SVN',\
		     answer = {}):
		
		self.host = host
		self.port = port
		self.nick = nick
		self.ident = ident
		self.realname = realname
		self.join = string.split(join, ',')
		self.masters = string.split(masters, ',')
		self.readbuffer = ''
		self.quit = quit
		self.die = die
		self.version = version
		self.answer = answer


	def connect(self):
		'''Connect to the server'''
		self.s = socket.socket( )
		
		try:
			self.s.connect((self.host, self.port))
		except:
			print '## ! Could not connect to ' + self.host + ':' \
                                                        + str(self.port)
			return False

		self.s.send('NICK %s\r\n' % self.nick)
		self.s.send('USER %s %s bla :%s\r\n' % \
                                    (self.ident, self.host, self.realname))
		self.joinLock = 0
		return True

	def listen(self):
		'''Listens the server and replies'''
		self.readbuffer = self.readbuffer + self.s.recv(1024)
		self.input = string.split(self.readbuffer, '\n')
		self.readbuffer = self.input.pop()
		return self.input




#__[Main]__##

if __name__ == '__main__':
	geeknode = Server()
	geeknode.commandsConfig()
	geeknode.serversConfig()
	if(geeknode.connect()):
		while True :
			geeknode.listen()
			geeknode.interpret()
