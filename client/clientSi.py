import socket

HOST = '127.0.0.1'  # IP server quiz
PORT = 9999         # Port server quiz

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to the quiz server!")

        while True:
            # Nhận câu hỏi từ server
            question = s.recv(1024).decode()
            if not question:
                break  # Server kết thúc
            print("\nQuestion:", question)

            # Gửi đáp án
            answer = input("Your answer: ")
            s.sendall(answer.encode())

            # Nhận phản hồi từ server
            response = s.recv(1024).decode()
            print("Server says:", response)

    print("Quiz ended. Thanks for playing!")

if __name__ == "__main__":
    main()
