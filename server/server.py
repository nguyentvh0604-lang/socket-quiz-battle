import socket
import threading


HOST = '0.0.0.0'
PORT = 9999

clients = [] 
scores = {}  
lock = threading.Lock() 

#câu hỏi và đáp án
qna = [
    ("29 + 100 = ?", "129"),
    ("Ngay Bac Ho doc ban tuyen ngon doc lap (ngay/thang/nam):", "2/9/1945"),
    ("Oxi hoa Dong tao ra gi:", "oxit cua dong"),
    ("Hien tai doi moi nhat cua Iphone la:", "Iphone 17"),
    ("C++ la mot dang ngon ngu lap trinh (Dung/Sai):", "Dung")
]
#thêm client mới
def add_client(conn, name):
    with lock:
        clients.append(conn)
        scores[name] = 0
#gửi tin nhắn đến tất cả client        
def broadcast(message):
    for client in clients:
        try:
            client.send(message.encode('utf-8'))
        except:
            clients.remove(client) 
#xử lý client            
def handle_client(conn, addr):
    try:
        #tên
        conn.send("Hay nhap ten cua ban: ".encode('utf-8'))
        name = conn.recv(1024).decode('utf-8')
        add_client(conn, name)
        #câu hỏi
        for q, a in qna:
            conn.send(f"\nCauhoi: {q}\nTraloi: ".encode())

            #nhận và xử lí chuẩn hóa đáp án
            raw_answer = conn.recv(1024).decode('utf-8').strip()
            answer = ' '.join(raw_answer.split())
        #kiểm tra đáp án đúng hay không, nếu đúng tính điểm, sai thì gửi đáp án đúng
            if answer.lower() == a.lower():
                with lock:
                    scores[name] += 1
                conn.send("Chinh xac!\n".encode('utf-8'))
            else:
                conn.send(f"Sai roi! Dap an dung la: {a}\n".encode('utf-8'))
        
        conn.send("\nBan da hoan thanh tat ca cau hoi! Cho xem bang xep hang...\n".encode('utf-8'))
        send_leaderboard()
            
    except:
        print(f"Lỗi kết nối với {addr}")
    finally:
        conn.close()
#gửi bảng xếp hạng
def send_leaderboard():
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    board = "\n--- BANG XEP HANG ---\n"
    for rank, (name, score) in enumerate(sorted_scores, 1):
        board += f"{rank}. {name}: {score} diem\n"
    broadcast(board)
#khởi động server    
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("Server đang lắng nghe kết nối...")
    
    while True:
        conn, addr = server.accept() 
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
if __name__ == "__main__":
    start_server()