import packet_parser


def compute(nodes):
    request_sent = 0
    request_recv = 0
    replies_sent = 0
    replies_recv = 0
    request_bytes_sent = 0
    request_bytes_recv = 0
    replies_byte = 0
    requestData = 0
    repliesData = 0

    totalRTT = 0
    totalHop = 0

    # list of node IP addresses where index i represents IP of node i+1 (index 0 = IP of node 1)
    node_IPs = ['192.168.100.1', '192.168.100.2', '192.168.200.1', '192.168.200.2']

    print('called compute function in in compute_metrics.py')
    for node_number in nodes.keys():
        print("Node ", node_number)
        # dataframe for this node
        df = nodes[node_number]
        for index, data in df.iterrows():
            if data['Source'] == node_IPs[node_number-1] and data['Source'] != data['Destination'] \
                    and data['Type (Request/Reply)'] == 'request':
                request_sent = request_sent + 1
                request_bytes_sent = request_bytes_sent + int(data['Length'])
            elif data['Source'] == node_IPs[node_number-1] and data['Source'] != data['Destination'] \
                    and data['Type (Request/Reply)'] == 'reply':
                replies_sent = replies_sent + 1
            elif data['Source'] != node_IPs[node_number-1] and data['Source'] != data['Destination'] \
                    and data['Type (Request/Reply)'] == 'request':
                request_recv = request_recv + 1
                request_bytes_recv = request_bytes_recv + int(data['Length'])
            elif data['Source'] != node_IPs[node_number-1] and data['Source'] != data['Destination'] \
                    and data['Type (Request/Reply)'] == 'reply':
                replies_recv = replies_recv + 1
            else:
                pass

        print(request_sent)
        print(request_recv)
        print(replies_sent)
        print(replies_recv)
        print(request_bytes_sent)
        print(request_bytes_recv)


compute(packet_parser.parse())
