import packet_parser


def compute(nodes):
    print('called compute function in in compute_metrics.py')

    totalRTT = 0
    totalHop = 0

    # list of node IP addresses where index i represents IP of node i+1 (index 0 = IP of node 1)
    node_IPs = ['192.168.100.1', '192.168.100.2', '192.168.200.1', '192.168.200.2']

    for node_number in nodes.keys():
        print("Node ", node_number)
        # dataframe for this node
        df = nodes[node_number]

        request_sent = 0
        request_recv = 0
        replies_sent = 0
        replies_recv = 0
        request_bytes_sent = 0
        request_bytes_recv = 0
        request_data_sent = 0
        request_data_recv = 0
        request_time_pairs = {}
        sum_RTTs = 0

        for index, data in df.iterrows():
            # if this node sent a request
            if data['Source'] == node_IPs[node_number-1] and data['Source'] != data['Destination'] \
                    and data['Type (Request/Reply)'] == 'request':
                request_sent = request_sent + 1
                request_bytes_sent = request_bytes_sent + int(data['Length'])
                request_data_sent = request_data_sent + int(data['Length']) - 42
                # store time when this request was sent for reference when its corresponding reply is found
                request_time_pairs[data['No.']] = data['Time']
            # if this node sent a reply to another node
            elif data['Source'] == node_IPs[node_number-1] and data['Source'] != data['Destination'] \
                    and data['Type (Request/Reply)'] == 'reply':
                replies_sent = replies_sent + 1
            # if this node received a request from another node
            elif data['Source'] != node_IPs[node_number-1] and data['Source'] != data['Destination'] \
                    and data['Type (Request/Reply)'] == 'request':
                request_recv = request_recv + 1
                request_bytes_recv = request_bytes_recv + int(data['Length'])
                request_data_recv = request_data_recv + int(data['Length']) - 42
            # if this node received a reply to a request it had sent
            elif data['Source'] != node_IPs[node_number-1] and data['Source'] != data['Destination'] \
                    and data['Type (Request/Reply)'] == 'reply':
                replies_recv = replies_recv + 1
                # when a reply is found, get its corresponding request and compute round trip time
                if data['Associated Request/Reply No.'] in request_time_pairs.keys():
                    RTT = float(data['Time']) - float(request_time_pairs[data['Associated Request/Reply No.']])
                    sum_RTTs += RTT
            else:
                pass

        print(request_sent)
        print(request_recv)
        print(replies_sent)
        print(replies_recv)
        print(request_bytes_sent)
        print(request_bytes_recv)
        print(request_data_sent)
        print(request_data_recv)
        print(round(sum_RTTs/request_sent * 1000, 2))


compute(packet_parser.parse())
