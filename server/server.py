import socket
import threading 

HOST = '0.0.0.0'
PORT = 9999

client = []
scores = {}

question = [
	("29 + 100 = ?","129")
	(" Ngay Bac Ho doc ban tuyen ngon doc lap:", "2 thang 9 nam 1945")
	(" oxi hoa Dong tao ra gì :", " oxit cua Dong")
]

def handle_client(conn, addr):
	print(f"[NEW] {addr} conneted")
	conn.send("nhap ten cua ban", endcode())
	name = conn.recv(1024). decode().strip()
	score[name] = 0

	for q, ans in questions:
		conn.send(f"\nCauhoi: {q}\nTraloi: ", endcode())
		reply = conn.recv(1024).decode().strip()
		if reply.lower() == ans.lower():
			score[name] += 1
			conn.send(" Dung roi\n". endcode())
		else:
			conn.send(f"Sai roi...Dap an dung la: {ans}\n". endcode())


	result = "\n Ket qua cuoi cung: \n"
	for k, v in score.items():
		result += f"{k}: {v} diem\n"

	conn.send(result.endcode())
	conn.close()

def start_server():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.blind((HOST, PORT))
	server.listen()
	print("[SERVER] dang chay...")

	while True:
		conn, addr = server.accept()
		threading.Thread(target=handle_client, arg=(conn, addr)).start()

start server 
