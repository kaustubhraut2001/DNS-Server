import dns.resolver
import dns.message
import dns.rdatatype
import dns.query
import dns.zone
import socket

# Define a simple DNS record
zone_data = """
$ORIGIN example.com.
@       IN      SOA     ns1.example.com. admin.example.com. (
                        2023101001 ; Serial
                        3600       ; Refresh
                        1800       ; Retry
                        1209600    ; Expire
                        3600       ; Minimum TTL
                        )
        IN      NS      ns1.example.com.
        IN      A       192.168.1.1
ns1     IN      A       192.168.1.2
"""

# Parse the zone data
zone = dns.zone.from_text(zone_data, origin='example.com')

def handle_query(data, addr):
    request = dns.message.from_wire(data)
    response = dns.message.make_response(request)

    qname = request.question[0].name
    qtype = dns.rdatatype.to_text(request.question[0].rdtype)

    if qname in zone:
        rrset = zone.find_rrset(qname, qtype)
        if rrset:
            response.answer.append(rrset)

    return response.to_wire()

def run_server(host='0.0.0.0', port=53):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f'DNS server is running on {host}:{port}')

    while True:
        data, addr = sock.recvfrom(512)
        response = handle_query(data, addr)
        sock.sendto(response, addr)

if __name__ == '__main__':
    run_server()
