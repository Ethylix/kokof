# -*- coding:utf-8 -*-
## kokof/config.py
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


import re
import string



class Config:
	'''manage config files'''
	def __init__(self, commandsPath='conf/commands', \
										serversPath='conf/servers'):

		self.commandsPath = commandsPath
		self.serversPath = serversPath
		self.answer = {}




	def serversConfig(self, serversPath='conf/servers'):
		
		self.serversPath = serversPath
		try:
			self.serverConfFile=open(self.serversPath)
		except:
			print '## ! Cannot open ' + \
			       self.serversPath
			return False

		print '## READING SERVERS CONF FILE'
		while True:
			self.serverConf = self.serverConfFile.readline()
			
			if self.serverConf == '':
				self.serverConfFile.close()
				print '## END SERVERS CONF FILE'
				break
			
			self.serverConf = self.serverConf.replace('\n','')
			self.serverConfLine = string.split(self.serverConf, ' ')

			if(self.serverConfLine[0] == 'server'):
				self.currentConfServer = self.serverConfLine[1]
			   	print '# ' + self.serverConfLine[1] + ' server found'
				self.currentConfServer = self.serverConfLine[1]

			if(self.serverConfLine[0] == 'host'):
				self.host = self.serverConfLine[1]
				print '# ' + self.currentConfServer + ' host: ' + self.host
			
			if(self.serverConfLine[0] == 'port'):
				self.port = int(self.serverConfLine[1])
				print '# ' + self.currentConfServer + ' port: ' \
															+ str(self.port)
			
			if(self.serverConfLine[0] == 'nick'):
				self.nick = self.serverConfLine[1]
				print '# ' + self.currentConfServer + ' nick: ' + self.nick
			
			if(self.serverConfLine[0] == 'ident'):
				self.ident = self.serverConfLine[1]
				print '# ' + self.currentConfServer + ' ident: ' + self.ident 
			
			if(self.serverConfLine[0] == 'realname'):
				self.realname = self.serverConfLine[1]
				print '# ' + self.currentConfServer + ' realname: ' \
															+ self.realname
			if(self.serverConfLine[0] == 'join'):
				self.join = string.split\
				          (self.serverConfLine[1], ',')
				print '# ' + self.currentConfServer + ' join channels : ' \
														+ ' '.join(self.join)
			if(self.serverConfLine[0] == 'quit'):
				self.quit = ' '.join(self.serverConfLine[1:])
				print '# ' + self.currentConfServer + ' quit message: ' \
																+ self.quit
			if(self.serverConfLine[0] == 'version'):
				self.version = ' '.join(self.serverConfLine[1:])
				print '# ' + self.currentConfServer + ' declared version : ' \
																+ self.version
			if(self.serverConfLine[0] == 'masters'):
				self.masters = string.split (self.serverConfLine[1], ',')
				print '# ' + self.currentConfServer + ' masters: ' \
													 + ' '.join(self.masters)


	def commandsConfig(self, commandsPath='conf/commands'):

		self.commandsPath = commandsPath
		self.answer = {}
		
		try:
			self.commandConfFile = open(self.commandsPath)
		except:
			print '## ! Cannot open ' + self.commandsPath
			return False

		print '##READING COMMANDS CONF FILE'
		while True:
			self.commandConf = self.commandConfFile.readline()
			if self.commandConf == '':
				self.commandConfFile.close()
				print '##END COMMANDS CONF FILE'
				break
			
			self.commandConf = self.commandConf.replace('\n','')

			self.regexpSingleEntryCommand = re.compile('^(\S+) "(.*)"$')
			self.regexpDualEntryCommand = re.compile('^(\S+) "(.*)" "(.*)"$')


			if(self.regexpSingleEntryCommand.search(self.commandConf)):
				
				self.commandConfLine= self.regexpSingleEntryCommand.\
													findall(self.commandConf)

				if(self.commandConfLine[0][0]=='die'):
					self.die = self.commandConfLine[0][1]
					print '#Will die on "' + self.die + '".'
			
			if(self.regexpDualEntryCommand.search(self.commandConf)):
				
				self.commandConfLine = self.regexpDualEntryCommand.\
													findall(self.commandConf)
				
				if(self.commandConfLine[0][0]=='answer'):
					self.answer[self.commandConfLine[0][1]] = \
													self.commandConfLine[0][2]
					print '#Will answer "' + self.commandConfLine[0][2] \
								+ '" to "' + self.commandConfLine[0][1] + '"'
