import socket
import threading
import sys

# Pega o IP inserido 
if sys.argv[1]:
    server_ip = str(sys.argv[1])
else:
    server_ip = '152.89.254.25'

if 2 in sys.argv:
    server_port = int(sys.argv[2])
else:
    server_port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))

server_socket.listen(5)

print(f"Server is listening on {server_ip}:{server_port}")

connected_clients = []


stored_position = 0
stored_ytba = ""
stored_playbutton = ""


def handle_client(client_socket):
    global stored_position, stored_ytba, stored_playbutton

    try:
        while True:

            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"Received from client: {data}")


            check = ['PButton', 'YTBA', 'Message', 'Position', 'PFalse', 'PTrue', 'Sync',
                     'PStore']

            for var in check:
                if var in data:
                    if var == 'PStore':

                        position = float(data.split(',')[0].replace('PStore', ''))
                        stored_position = position
                    elif var == 'YTBA':

                        ytba = data.split(',')[0].replace('YTBA', '')
                        stored_ytba = ytba

                    response = data


                    if 'Sync' in data:
                        response = f"Position{stored_position},YTBA{stored_ytba},PlayButton{stored_playbutton}"
                    if var == 'PStore':
                        pass
                    elif data.split(',')[0].replace('PButton', '') == stored_playbutton:
                        pass
                    else:
                        for client in connected_clients:
                            client.send(response.encode('utf-8'))
                        print(f"Sent to all clients: {response}")
                    if var == 'PButton':
                        playbutton = data.split(',')[0].replace('PButton', '')
                        stored_playbutton = playbutton

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:

        connected_clients.remove(client_socket)

        client_socket.close()



while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")


    connected_clients.append(client_socket)


    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
