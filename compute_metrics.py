import os
import re
import pandas as pd

def compute(nodes):
	requestSent = 0
	requestRecv = 0
	repliesSent = 0
	repliesRecv = 0
	requestByte = 0
	repliesByte = 0
	requestData = 0
	repliesData = 0

	totalRTT = 0
	totalHop = 0

	print('called compute function in in compute_metrics.py')
	#Split all the information from the dictionaries into a massive list, remove blank spaces, newline characters, |, etc
	fields = nodes[1].to_markdown().split(' ')
	key = []
	for item in fields:
		if item != '' and item != '|' and item != '\n' and item != '|\n|':
			key.append(item)
	#remove the header of the dictionary
	for i in range(0, 14):
		del key[0]
	n = 11
	#Compute the information. If i % 11 is 0 then it's the start of a new entry. Add (1:10) to get other information in that line
	for i in range(len(key)):
		if i % n == 0:
			"""
			key[i + 1] == No.
                        key[i + 2] == Time
                        key[i + 3] == Source
			key[i + 4] == Destination
                        key[i + 5] == Length
                        key[i + 6] == Type (Request/Reply)
			key[i + 7] == ID
                        key[i + 8] == Seq
                        key[i + 9] == TTL
			key[i + 10] == Associated Request/Reply No.
			"""
			if key[i + 3] == '192.168.100.1' and key[i + 3] != key[i + 4] and key[i + 6] == 'request':
				requestSent = requestSent + 1
				requestByte = requestByte + int(key[i + 5])
			elif key[i + 3] == '192.168.100.1' and key[i + 3] != key[i + 4] and key[i + 6] == 'reply':
				repliesSent = repliesSent + 1
			elif key[i + 4] == '192.168.100.1' and key[i + 3] != key[i + 4] and key[i + 6] == 'request':
				requestRecv = requestRecv + 1
			elif key[i + 4] == '192.168.100.1' and key[i + 3] != key[i + 4] and key[i + 6] == 'reply':
				repliesRecv = repliesRecv + 1
			else:
				pass

			if key[i + 6] == 'request':
				requestByte = requestByte + int(key[i + 5])
			elif key[i + 6] == 'reply':
				repliesByte = repliesByte + int(key[i + 5])
			else:
				pass

			
	print(requestSent / 4)
	print(repliesSent / 4)
	print(requestRecv / 4)
	print(repliesRecv / 4)
	print(requestByte)
	print(repliesByte)
