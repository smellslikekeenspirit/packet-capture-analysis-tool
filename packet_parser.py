import os
import re
import pandas as pd


def parse():
    """
    for every file ending in "filtered.txt", it makes a dataframe containing all relevant information
    from all packet summary lines in the file and stores the dataframes in a dictionary where the
    key is the node number
    :return: dictionary of length 4 where each key, representing a node, contains a dataframe
    """
    print('called parse function in packet_parser.py')
    nodes = {}
    for file in os.listdir(os.getcwd()):
        # if filename ends in "filtered.txt"
        if file.endswith("filtered.txt"):
            data = []
            with open(file) as f:
                for line in f:
                    # if line is a summary line
                    if "Echo (ping) request" in line or "Echo (ping) reply" in line:
                        # remove parentheses
                        line = line.replace("(", "").replace(")", "")
                        # simplify line by removing unnecessary words
                        line = re.sub(r'\breply in\b | \brequest in\b| \bid=\b| \bseq=\b| \bttl=\b| \bEcho ping\b| '
                                      r'\bICMP\b', '', line)
                        # reduce multiple whitespaces into one
                        line = " ".join(line.split())
                        # split by whitespace and comma
                        line = re.split(r'[ ,]+', line)
                        # append summary line to data
                        data.append(line)
                # create dataframe for this node
                df = pd.DataFrame(data, columns=['No.', 'Time', 'Source', 'Destination', 'Length',
                                                 'Type (Request/Reply)', 'ID', 'Seq', 'TTL',
                                                 'Associated Request/Reply No.'])
                # get number of node from name of file
                node_number = file.replace("Node", "").replace("_filtered.txt", "")
                # use number of node as key in nodes dictionary for efficient retrieval in future
                nodes[int(node_number)] = df
    return nodes
