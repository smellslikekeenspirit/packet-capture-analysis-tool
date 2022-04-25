import packet_parser


def compute(nodes):
    print('called compute function in in compute_metrics.py')

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
        reply_delay_time_pairs = {}
        sum_RTTs = 0
        sum_delay = 0
        sum_hops = 0

        for index, data in df.iterrows():
            # if this node sent a request
            if data['Source'] == node_IPs[node_number-1] and data['Source'] != data['Destination'] \
                    and data['Type (Request/Reply)'] == 'request':
                request_sent = request_sent + 1
                request_bytes_sent = request_bytes_sent + int(data['Length'])
                request_data_sent = request_data_sent + int(data['Length']) - 42
                # store time when this request was sent for reference when its corresponding reply is found
                request_time_pairs[data['No.']] = data['Time']
                    
            # if this node received a request from another node
            elif data['Source'] != node_IPs[node_number-1] and data['Source'] != data['Destination'] \
                    and data['Type (Request/Reply)'] == 'request':
                request_recv = request_recv + 1
                request_bytes_recv = request_bytes_recv + int(data['Length'])
                request_data_recv = request_data_recv + int(data['Length']) - 42
                reply_delay_time_pairs[data['No.']] = data['Time']
            # if this node sent a reply to another node
            elif data['Source'] == node_IPs[node_number-1] and data['Source'] != data['Destination'] \
                    and data['Type (Request/Reply)'] == 'reply':
                replies_sent = replies_sent + 1
                if data['Associated Request/Reply No.'] in reply_delay_time_pairs.keys():
                    delay = float(data['Time']) - float(reply_delay_time_pairs[data['Associated Request/Reply No.']])
                    sum_delay += delay 
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

            if '192.168.100' in data['Source'] and '192.168.100' in data['Destination']:
                sum_hops = sum_hops + 1
            elif '192.168.200' in data['Source'] and '192.168.200' in data['Destination']:
                sum_hops = sum_hops + 1
            else:
                sum_hops = sum_hops + 3
        f = open("output.csv", "a")
        f.write("Node " + str(node_number) + "\n")
        f.write("Echo Requests Sent, Echo Requests Recieved, Echo Replies Sent, Echo Replies Recieved\n")
        f.write(str(int(request_sent / 2)) + "," + str(int(request_recv / 2)) + "," +  str(int(replies_sent / 2)) + "," + str(int(replies_recv / 2)) + "\n")
        f.write("Echo Request Bytes Sent, Echo Request Data Sent\n")
        f.write(str(int(request_bytes_sent / 2)) + "," + str(int(request_data_sent / 2)) + "\n")
        f.write("Echo Request Bytes Recieved, Echo Request Bytes Recieved\n")
        f.write(str(int(request_bytes_recv / 2)) + "," + str(int(request_data_recv / 2)) + "\n")
        f.write("Average RTT (milliseconds): " + str(round(sum_RTTs/request_sent * 1000, 2)) + "\n")
        f.write("Echo Request Throughput (kB/sec): " + str(round((request_bytes_sent/sum_RTTs) / 1000, 1)) + "\n")
        f.write("Echo Request Goodput (kB/sec): " + str(round((request_data_sent/sum_RTTs) / 1000, 1)) + "\n")
        f.write("Average Reply Delay (microseconds): " + str(round(sum_delay/replies_sent * 1000000, 2)) + "\n")
        f.write("Average Echo Request Hop Count: " + str(round(sum_hops/(request_sent + replies_sent + request_recv + replies_recv),2)) + "\n\n\n")
        f.close()

compute(packet_parser.parse())
