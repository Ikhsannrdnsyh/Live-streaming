import socket
import cv2
import pickle
import struct
import threading

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Socket Bind
server_socket.bind(('192.168.43.156', 9999))

# Socket Listen
server_socket.listen(5)
print("Listening at ('192.168.43.156', 9999)")

# Buat kamera
camera = cv2.VideoCapture(0)

def send_frame(conn, addr):
    try:
        if conn:
            while True:
                # Ambil gambar dari kamera
                success, frame = camera.read()
                if not success:
                    break
                
                # Mengirim gambar ke client
                data = pickle.dumps(frame)
                message_size = struct.pack("Q", len(data))
                conn.sendall(message_size + data)
                
                # Menghentikan proses jika tombol 'q' ditekan
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
        conn.close()

    except Exception as e:
        print(f"Client {addr} disconnected")
        pass

while True:
    # Menerima koneksi dari client
    conn, addr = server_socket.accept()
    print(f"Connected to {addr}")
    
    # Buat thread untuk setiap koneksi ke client
    thread = threading.Thread(target=send_frame, args=(conn,addr))
    thread.start()

# Tutup server setelah selesai
server_socket.close()
