# -*- coding:utf-8 -*-
## kokof/input.py
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


import string



class Input:
	'''manage what is received from the socket'''


	def recognize(self, line):
		'''recognize something useful from something master says on a channel'''
		if(' '.join(line[3:]) == self.die):
			self.s.send('QUIT :' + self.quit + '\r\n')
			exit()

		elif(self.answer.has_key(' '.join(line[3:]))):
			self.s.send('PRIVMSG ' + line[2] + ' :' \
                            + self.answer[' '.join(line[3:])] + '\r\n')
			return True

		else:
			return False


	def command(self, line):
		'''check if a privmsg from is a known command/CTCP'''
		if(line[3] == 'say'):
			if(line[5] == '/me'):
				self.s.send('PRIVMSG ' + line[4] + ' :\001ACTION ' + ' '.join(line[6:]) + '\001\r\n')
			else:
				self.s.send('PRIVMSG ' + line[4] + ' :' + ' '.join(line[5:]) + '\r\n')

		elif(line[3] == '\001VERSION\001'):
				self.s.send('NOTICE ' + self.sender(line[0]) + ' :\001VERSION ' + self.version + '\001\r\n')
				print 'NOTICE ' + self.sender(line[0]) + ' :\001VERSION ' + self.version



	def interpret(self):
		'''interpret messages from the socket and launch appropriate methods'''

		for line in self.input:
			print line
			
			line = string.rstrip(line)
			line = string.split(line)


			if(len(line)>3):
				line[3] = line[3][1:]

				if(self.isMaster(line[0])):
					if(line[2] == self.nick):
						self.command(line)

					else:
						self.recognize(line)


		# joins
				elif(self.joinLock==0):
					if((line[1] == '376') or (line[1]== '422') ):
						for chan in self.join:
							self.s.send('JOIN %s\r\n' % chan)
						self.joinLock = 1

		 # Protocol
			elif(line[0] == 'PING'):
				self.s.send('PONG ' + line[1] + '\r\n' )
