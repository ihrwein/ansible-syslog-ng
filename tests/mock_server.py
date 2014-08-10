import getopt
import sys
import socket
import threading
from threading import Timer

TIMED_OUT = False

def timeout_handler(parsed_opts):
    print("timeout expired")
    host = parsed_opts["address"]
    port = parsed_opts["port"]

    global TIMED_OUT
    TIMED_OUT = True
    socket_mode = socket.SOCK_STREAM if "enable-tcp" in parsed_opts else socket.SOCK_DGRAM
    s = socket.socket(socket.AF_INET, socket_mode)
    
    if "enable-tcp" in parsed_opts:
        s.connect((host, port))
    else:
        s.sendto("TIMEOUT", (host, port))


def parse_cli_params():
    parsed_opts = {}
    long_opts =  ["timeout=]", "enable-tcp", "enable-udp", "address=", "port="]
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "T:tua:p:",long_opts)
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err)) # will print something like "option -a not recognized"
        sys.exit(2)
    output = None
    for o, a in opts:
        if o in ("-T", "--timeout") :
            parsed_opts["timeout"] = float(a)
        elif o in ("-t", "--enable-tcp"):
            parsed_opts["enable-tcp"] = True
        elif o in ("-u", "--enable-udp"):
            parsed_opts["enable-udp"] = True
        elif o in ("-a", "--address"):
            parsed_opts["address"] = a
        elif o in ("-p", "--port"):
            parsed_opts["port"] = int(a)
        else:
            print("o={0} a={1}".format(o, a))
            assert False, "unhandled option"
    assert len(parsed_opts) == len(long_opts) - 1
    return parsed_opts

def main():
    parsed_opts = parse_cli_params()

    timer = Timer(parsed_opts["timeout"], timeout_handler, args=[parsed_opts])
    timer.start()

    socket_mode = socket.SOCK_STREAM if "enable-tcp" in parsed_opts else socket.SOCK_DGRAM
    host = parsed_opts["address"]
    port = parsed_opts["port"]
    timeout = parsed_opts["timeout"]
    
    s = socket.socket(socket.AF_INET, socket_mode)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))

    if "enable-tcp" in parsed_opts.keys():
        s.listen(1)

    if "enable-tcp" in parsed_opts.keys():
        conn, addr = s.accept()
        conn.close()
        return 1 if TIMED_OUT else 0
 
    d, a = s.recvfrom(2)
    return 1 if TIMED_OUT else 0

if __name__ == "__main__":
    sys.exit(main())
