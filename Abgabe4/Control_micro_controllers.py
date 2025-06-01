import socket

# CRC 4
gen_poly_4 = 0b1_0011
# CRC 6
gen_poly_6 = 0b100_0011
# CRC 8
gen_poly_8 = 0b1_1010_0111
# CRC 16
gen_poly_16 = 0b1_1000_0000_0000_0101

errors_per_ten_thousand = (5).to_bytes(4, 'big')
text_bytes_per_message = b''.join([x.to_bytes(4, 'big') for x in list(range(1, 101, 10))])
length_of_byte_array = (len(text_bytes_per_message)).to_bytes(4, 'big')
polynome_list = b''.join([x.to_bytes(4, 'big') for x in [gen_poly_4, gen_poly_6, gen_poly_8, gen_poly_8]])
# 4 + 16 + 4 + x*4
configuration_message = errors_per_ten_thousand + polynome_list + length_of_byte_array + text_bytes_per_message

HOST = '192.168.178.64'  # Localhost
PORT_A = 65001        # Port to listen on
PORT_B = 65002        # Port to listen on

sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender_socket.bind((HOST, PORT_A))
sender_socket.listen()
print(f"Server listening on {HOST}:{PORT_A}")
conn, addr = sender_socket.accept()
with conn:
    print('Connected by', addr)
    conn.sendall(configuration_message)


receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver_socket.bind((HOST, PORT_B))
receiver_socket.listen()
print(f"Server listening on {HOST}:{PORT_B}")
conn, addr = receiver_socket.accept()
with conn:
    print('Connected by', addr)
    anzahl_korrekter_uebertragungen = int.from_bytes(conn.recv(4), 'big')
    anzahl_crc_detektierte_fehler = int.from_bytes(conn.recv(4), 'big')
    anzahl_sequenz_fehler = int.from_bytes(conn.recv(4), 'big')
    anzahl_duplikate = int.from_bytes(conn.recv(4), 'big')
    anzahl_nicht_detektierter_fehler = int.from_bytes(conn.recv(4), 'big')


