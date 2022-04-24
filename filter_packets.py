import os


def write_packet_to_file(packet, filename):
	"""
	writes given packet to a file
	:param packet: ICMP packet represented as a list of strings
	:param filename: filename representing the node the packet is from
	:return: None
	"""
	# If the filename is Node*.txt, let name of file containing its filtered packets be Node*.filtered.txt
	filtered_filename = filename.replace(".txt", "") + "_filtered.txt"
	# write each line of packet to file
	with open(filtered_filename, 'a') as f:
		for line in packet:
			f.write(line)


def filter():
	"""
	Extracts ICMP packets of Type 8 (request) and Type 0 (reply) from Node files
	:return: None
	"""
	print('called filter function in filter_packets.py')
	for file in os.listdir(os.getcwd()):
		# if filename is of format Node*.txt
		if file.startswith("Node") and file.endswith(".txt"):
			with open(file) as f:
				# initialize empty packet at start of file
				packet = []
				# set inclusion flag to 0, meaning this packet will not be added to filtered file
				include_packet = 0
				for line in f:
					# if this line is the first line of a packet
					if line.startswith("No."):
						# implies we have finished reading the previous packet
						# check if previous packet should be included
						if include_packet:
							write_packet_to_file(packet, file)
						# set inclusion flag for new packet to 0
						include_packet = 0
						# re-initialize empty packet
						packet = []
					# check if this line is the second line of a packet which we can use to identify type
					elif "Echo (ping) request" in line or "Echo (ping) reply" in line:
						# include this packet
						include_packet = 1
					# add every line to its packet
					packet.append(line)


	
