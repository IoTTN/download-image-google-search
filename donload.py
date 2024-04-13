# import các gói cần thiết
from imutils import paths
import argparse
import requests
import cv2
import os
from datetime import datetime # Thêm thư viện datetime

# Xây dựng các cú pháp và phân tích các đối số
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--urls", required=True,
    help="đường dẫn đến tệp chứa các URL hình ảnh")
ap.add_argument("-o", "--output", required=True,
    help="đường dẫn đến thư mục đầu ra của các hình ảnh")
args = vars(ap.parse_args())

# lấy danh sách các URL từ tệp đầu vào, sau đó khởi tạo tổng số hình ảnh đã tải xuống
rows = open(args["urls"]).read().strip().split("\n")
total = 0

# loop qua các URL
for url in rows:
    try:
        # thử tải hình ảnh
        r = requests.get(url, timeout=60)
        
        # tạo tên tệp dựa trên thời gian hiện tại với độ chính xác đến mili giây
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S%f")[:-3] # định dạng thời gian với mili giây và loại bỏ ba chữ số cuối cùng (độ chính xác đến mili giây)
        filename = "{}.jpg".format(timestamp)
        p = os.path.sep.join([args["output"], filename])
        
        # lưu hình ảnh vào đĩa
        f = open(p, "wb")
        f.write(r.content)
        f.close()
        
        # cập nhật số lượng
        print("[INFO] đã tải xuống: {}".format(p))
        total += 1
        
    # xử lý nếu có bất kỳ ngoại lệ nào xảy ra trong quá trình tải xuống
    except Exception as e:
        print("[INFO] lỗi khi tải xuống {}...bỏ qua".format(url))
        print(e)

# loop qua các đường dẫn hình ảnh vừa tải xuống
for imagePath in paths.list_images(args["output"]):
    # khởi tạo biến xóa
    delete = False
    
    # thử tải hình ảnh
    try:
        image = cv2.imread(imagePath)
        
        # nếu hình ảnh là None thì xóa nó
        if image is None:
            delete = True
    
    # nếu OpenCV không thể tải hình ảnh, nó có thể bị hỏng nên chúng ta sẽ xóa nó
    except Exception as e:
        print("[INFO] lỗi khi tải hình ảnh {}...bỏ qua".format(imagePath))
        print(e)
        delete = True
    
    # kiểm tra xem hình ảnh có nên bị xóa không
    if delete:
        print("[INFO] đang xóa {}".format(imagePath))
        os.remove(imagePath)
