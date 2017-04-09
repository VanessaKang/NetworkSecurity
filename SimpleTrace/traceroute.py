#!/usr/bin/python

import optparse
import socket
import sys
import time

#Internet control message protocol

icmp = socket.getprotobyname('icmp')
udp = socket.getprotobyname('udp')

def create_sockets(ttl):
    """
    Sets up sockets necessary for the traceroute.  We need a receiving
    socket and a sending socket.
    """
    #receiving socket will need to accept the ICMP packets from the routers
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    #we are using UDP to send packets
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
    """
	Set socket options and timeout value for the recv socket
	"""
    send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    return recv_socket, send_socket

def main(dest_name, port, max_hops, timeout):
    #IP address from a domain name
    dest_addr = socket.gethostbyname(dest_name)
    #time to live will initially be 1 so that we can kill the packet at the first router
    ttl = 1

    while True:
        #we need to call the function above to create the sockets
        recv_socket, send_socket = create_sockets(ttl)
        recv_socket.settimeout(timeout)
        #Receving socket that we created will be listening to a certain port
        recv_socket.bind(("", port))
        #Sending socket that we have created will send to the same port, we're not sending any data
        send_socket.sendto("", (dest_name, port))

        """
	    Record the current time
	    """
            #this is the current time of the program
        begin_time = time.time()

        curr_addr = None
        curr_name = None

        #Since we can get a timeout error(ICMP requests are blocked), we have to use try-except blocks
        try:
            # socket.recvfrom() gives back (data, address), but we
            # only care about the latter.
            # The format of address is a tuple with IP where for the blocksize is set
            _, curr_addr = recv_socket.recvfrom(512)
            #address is given as tuple (IP,port) 
            curr_addr = curr_addr[0]

            #the current time is taken and the begin time is differenced to get round trip time
            #(this is in miliseconds) 
            current_time = time.time()
            round_trip_time = (current_time - begin_time)*1000

            #try to grab the name of the address, if not use the address as the name 
            try:
                curr_name = socket.gethostbyaddr(curr_addr)[0]
            except:
                curr_name = str(curr_addr)

        except socket.timeout:
            #In the Assignment description, it said to increment TTL and send a new packet on timeout
            #Since ttl is outside of the try-except block, after this exception it will increment itself
            #-----Here is the sending a new packet line 
            send_socket.sendto("", (dest_name, port))
        except socket.error:
            pass
        finally:
            send_socket.close()
            recv_socket.close()


        if curr_addr is not None:
            #prints the information of the packets 
            curr_addr = str(curr_addr)
            current_hop_info =  str(ttl) + "    " + str(curr_name) + "(" +curr_addr + ")  " +str(round_trip_time) + "ms"
            print current_hop_info
        else:
            print str(ttl) + " *"


        ttl += 1
        #if the address reacches destination or if ttl reaches max_hops(hoped for too long), it should end
        if curr_addr == dest_addr or ttl > max_hops:
            break

    return 0

if __name__ == "__main__":
    parser = optparse.OptionParser(usage="%prog [options] hostname")
    parser.add_option("-p", "--port", dest="port",
                      help="Port to use for socket connection [default: %default]",
                      default=33434, metavar="PORT")

    parser.add_option("-m", "--max-hops", dest="max_hops",
                      help="Max hops before giving up [default: %default]",
                      default=30, metavar="MAXHOPS")
    """
 	Add an option of timeout value; default value is 5 second
    """
    parser.add_option("-t", "--timeout", dest="timeout",
                    help="Time out value is [default: %default]",
                    default=5, metavar="TIMEOUT")

    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("No destination host")
    else:
        dest_name = args[0]

    sys.exit(main(dest_name=dest_name, port=int(options.port), max_hops=int(options.max_hops), timeout=int(options.timeout)))
