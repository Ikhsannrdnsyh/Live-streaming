import socket
import cv2
import pickle
import struct
import pyshine as ps

# Socket Create
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Socket Connect
client_socket.connect(('192.168.225.74', 9999))

# Buat window untuk menampilkan gambar
cv2.namedWindow('image', cv2.WINDOW_NORMAL)

while True:
    # Menerima data gambar dari server
    data = b""
    payload_size = struct.calcsize("Q")
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024)
        if not packet:
            break
        data += packet
    packet_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q",packet_msg_size)[0]
    
    while len(data) < msg_size:
        data += client_socket.recv(4*1024)
    
    # Mengubah data gambar menjadi objek gambar OpenCV
    frame_data = data[:msg_size]
    frame = pickle.loads(frame_data)
    
    # Menambahkan teks pada gambar
    text = "FROM SERVER"
    frame = ps.putBText(frame,text,10,10,vspace=10,
            hspace=1,font_scale=0.7) 
    
    # Menampilkan gambar di window
    cv2.imshow('image',frame)
    
    # Menghentikan proses jika tombol 'q' ditekan
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tutup window setelah selesai
cv2.destroyAllWindows()

# Tutup koneksi setelah selesai
client_socket.close()
