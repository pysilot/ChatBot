<p> <em>Nhập môn Công nghệ thông tin -  Trường Đại học Khoa học tự nhiên, ĐHQG-HCM </em> </p>
<p> <em> Đồ án 
ChatBot - Nhóm 5 </em> </p>

## I. Cài đặt và thiết lập môi trường Streamlit

1. Thiết lập môi trường
```
pip install streamlit
```
2. Clone dự án 
```
git clone https://github.com/pysilot/ChatBot.git
cd ChatBot
```
3. Cài đặt thư viện cần thiết
```
pip install -r requirements.txt
```
## II. Khởi động sever
**Bước 1**. Vào Google Colab, chọn New Notebook và chọn tệp ``Gpt_oss_&_pinggy_&_ngrok.ipynb`` 

**Bước 2**. Chọn GPU T4 và Runtime type là Python 3

<img width="570" height="515" alt="screenshot_1766640111" src="https://github.com/user-attachments/assets/5a59f3e5-d3e9-4fb1-b1c5-aea701d3631f" />


**Bước 3**. Nhấn run all để chạy các cell. Để public ra Internet để mô hình có thể gọi, dán lệnh dưới đây vào terminal
```
ssh -p 443 -R0:localhost:11434 [qr@a.pin](mailto:qr@a.pin)
```
> Lưu ý: Nhấn chuột phải và chọn copy trong menu, nhấn tổ hợp phím CRTL + C sẽ ngắt kết nối.

<img width="565" height="123" alt="2" src="https://github.com/user-attachments/assets/97dc5431-da94-4401-8113-b919eb206bd8" />

> <p>Gõ "yes" để tiếp tục kết nối. </p>



## III. Khởi động giao diện sử dụng Chatbot
**Bước 1**. Sao chép đường link pinggy vào mô hình chatbot trong file chat_ui.py tại dòng 13 ``API_URL = "/api/generate"``

<img width="582" height="134" alt="image" src="https://github.com/user-attachments/assets/f514b61a-30e8-42eb-a472-44d871941510" />

>Lưu ý: Tại cuối đường link phải thêm /api/generate

**Bước 2**. Tại Terminal nhập lệnh 
```
streamlit run chat_ui.py
```
hoặc
```
py -m streamlit run chat_ui.py
```

## IV. Cấu trúc mã nguồn
<pre>
├── requirements.txt
├── README.md
└── src
    ├── backend
    │    └── Gpt_oss_&_pinggy_&_ngrok.ipynb
    ├── ui
    │    └── chat_ui.py
    └──.DS_Store
</pre>

## V. Một số hình ảnh khi sử dụng ChatBot

![z7234717304958_14cffa52aecc007feab8686c854d943d](https://github.com/user-attachments/assets/333547db-60fb-4c37-9627-7a185bfd515b)


<img width="1920" height="1080" alt="Screenshot (2)" src="https://github.com/user-attachments/assets/24dbaebc-cbd0-4082-92a2-ec9f363165d2" />

## V. Tiến độ Đồ án
<img width="1292" height="380" alt="screenshot_1762838054" src="https://github.com/user-attachments/assets/7ef19393-c680-4b63-bd65-c0c4509288b0" />

