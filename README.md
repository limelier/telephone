# Telephone protocol reference

This repository contains the reference for a simple "telephone" protocol. This protocol involves reading messages from
standard input or from an incoming connection, printing them, and optionally relaying them to another destination, like
the children's game of the same name.

## Protocol
Each packet is structured as a `size` header and a `data` payload.
### size
The `size` header is 4-byte big endian integer marking the size of the `data` payload in bytes.
### data
The `data` block is a block of `size` bytes encoding a message in UTF-8.

## Reference implementation

This repository contains a very crude example implementation, `telephone.py`. This implementation lacks a lot of bells and whistles like error handling and send/recv buffering, but it should be sufficient for simple usage tests.

The usage for the implementation is one of the following:
- `python telephone.py client [<host:port>]` will listen for messages on standard input and optionally relay them to the given host.
- `python telephone.py server <bind_port> [<host:port>]` will listen for messages on the binding port and optionally relay them to the given host.

If the machine supports IPV6, it will be used.

### example usage
#### client with destination
```
$> python telephone.py client my-hostname:5555
client sending to ('my-hostname', 5555)

 > hello world
sent to ('my-hostname', 5555)

 > supports utf-8 😋
sent to ('my-hostname', 5555)

```

#### server with destination
```
$> python telephone.py server 5555 localhost:6666
server listening on port 5555
and sending to ('localhost', 6666)

received from ####
-> hello world
sent to ('localhost', 6666)

received from ####
-> supports utf-8 😋
sent to ('localhost', 6666)
```

#### server without destination
```
~/docs/telephone/python
$> python telephone.py server 6666
server listening on port 6666

received from ::1
-> hello world

received from ::1
-> supports utf-8 😋
```