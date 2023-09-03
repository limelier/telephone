import socket
import sys
import urllib.parse

from typing import Tuple, TypeAlias, Optional

Host: TypeAlias = str
Port: TypeAlias = int
Address: TypeAlias = Tuple[Host, Port]


def client(destination: Optional[Address]):
    print(f"client sending to {destination}")
    print()

    while True:
        try:
            inp = input(" > ")
        except EOFError:
            break
        send(inp, destination)


def server(port: Port, destination: Optional[Address]):
    addr = ("", port)  # all interfaces
    if socket.has_dualstack_ipv6():
        server_socket = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
    else:
        server_socket = socket.create_server(addr)

    print(f"server listening on port {port}")
    if destination is not None:
        print(f"and sending to {destination}")
    print()

    while True:
        (client_socket, address) = server_socket.accept()
        size = int.from_bytes(client_socket.recv(4), "big")
        message = str(client_socket.recv(size), "utf-8")
        print(f"received from {client_socket.getpeername()[0]}")
        print("->", message)

        send(message, destination)


def send(message: str, destination: Optional[Address]):
    if destination is None:
        print("")
        return

    s = socket.create_connection(destination)

    data = bytes(message, "utf-8")
    size = len(data)

    s.send(int.to_bytes(size, 4, "big"))
    s.send(data)

    s.close()

    print(f"sent to {destination}")
    print()


def usage():
    print(
        f"""Usage:
./telephone client [<destination_host:port>]
./telephone server <bind_port> [<destination_host:port>]""",
        file=sys.stderr)
    exit(1)


def parse_destination(dest: str) -> Optional[Address]:
    try:
        result = urllib.parse.urlsplit("//" + dest)
        return result.hostname, result.port
    except ValueError:
        print(f"Invalid destination: {dest}", file=sys.stderr)
        sys.exit(1)


def main():
    argc = len(sys.argv)
    if argc < 2:
        usage()

    destination = None
    if sys.argv[1] == 'client' and argc <= 3:
        # args: self, client, [dest]
        if argc == 3:
            destination = parse_destination(sys.argv[2])
        client(destination)
    elif sys.argv[1] == 'server' and argc in range(3, 5):
        # args: self, server, port, [dest]
        if argc == 4:
            destination = parse_destination(sys.argv[3])
        port = int(sys.argv[2])
        server(port, destination)
    else:
        usage()


if __name__ == '__main__':
    main()
