
def compute(nodes):
    print('called compute function in in compute_metrics.py')

    # list of node IP addresses where index i represents IP of node i+1 (index 0 = IP of node 1)
    node_IPs = ['192.168.100.1', '192.168.100.2', '192.168.200.1', '192.168.200.2']

    for node_number in nodes.keys():
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
        request_sending_times = {}
        request_receiving_times = {}
        request_ttls = {}
        sum_rtts = 0
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
                request_sending_times[data['No.']] = data['Time']
                # store TTL for reference when its corresponding reply is found
                request_ttls[data['No.']] = data['TTL']

            # if this node received a request from another node
            elif data['Source'] != node_IPs[node_number-1] and data['Source'] != data['Destination'] \
                    and data['Type (Request/Reply)'] == 'request':
                request_recv = request_recv + 1
                request_bytes_recv = request_bytes_recv + int(data['Length'])
                request_data_recv = request_data_recv + int(data['Length']) - 42
                # store time when this request was received for reference to calculate reply delay
                request_receiving_times[data['No.']] = data['Time']

            # if this node sent a reply to another node
            elif data['Source'] == node_IPs[node_number-1] and data['Source'] != data['Destination'] \
                    and data['Type (Request/Reply)'] == 'reply':
                replies_sent = replies_sent + 1
                if data['Associated Request/Reply No.'] in request_receiving_times.keys():
                    delay = float(data['Time']) - float(request_receiving_times[data['Associated Request/Reply No.']])
                    sum_delay += delay

            # if this node received a reply to a request it had sent
            elif data['Source'] != node_IPs[node_number-1] and data['Source'] != data['Destination'] \
                    and data['Type (Request/Reply)'] == 'reply':
                replies_recv = replies_recv + 1
                # when a reply is found, get its corresponding request and compute round trip time
                if data['Associated Request/Reply No.'] in request_sending_times.keys():
                    RTT = float(data['Time']) - float(request_sending_times[data['Associated Request/Reply No.']])
                    sum_rtts += RTT
                # when a reply is found, get its corresponding request and compute hop count from TTLs
                if data['Associated Request/Reply No.'] in request_ttls.keys():
                    hop_count = 1 + int(request_ttls[data['Associated Request/Reply No.']]) - int(data['TTL'])
                    sum_hops += hop_count

        # write metrics to file
        f = open("output.csv", "a")
        f.write("Node " + str(node_number) + "\n")
        f.write("Echo Requests Sent,Echo Requests Received,Echo Replies Sent,Echo Replies Received\n")
        f.write(str(request_sent) + "," + str(request_recv) + ","
                + str(replies_sent) + "," + str(replies_recv) + "\n")
        f.write("Echo Request Bytes Sent (bytes),Echo Request Data Sent (bytes)\n")
        f.write(str(request_bytes_sent) + "," + str(request_data_sent) + "\n")
        f.write("Echo Request Bytes Received (bytes),Echo Request Data Received (bytes)\n")
        f.write(str(request_bytes_recv) + "," + str(request_data_recv) + "\n")
        f.write("Average RTT (milliseconds)," + str(round(sum_rtts/request_sent * 1000, 2)) + "\n")
        f.write("Echo Request Throughput (kB/sec)," + str(round((request_bytes_sent/sum_rtts) / 1000, 1)) + "\n")
        f.write("Echo Request Goodput (kB/sec)," + str(round((request_data_sent/sum_rtts) / 1000, 1)) + "\n")
        f.write("Average Reply Delay (microseconds)," + str(round(sum_delay/replies_sent * 1000000, 2)) + "\n")
        f.write("Average Echo Request Hop Count," + str(round(sum_hops / request_sent, 2)) + "\n\n\n")
        f.close()
