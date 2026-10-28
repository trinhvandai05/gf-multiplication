# Trịnh Văn Đại
# Trình bày
## Phân tích bài toán
Bài toán lập trình tính kết quả phép nhân f(x) với g(x) trong trường hữu hạn GF(2^4) và GF(2^8)
Trong chương trình có các hàm sau:
1. Hàm xor() có chức năng xor 2 chuỗi bit nhị phân
2. Hàm xtime() có chức năng trả kết quả phép toán xg(x) mod m(x)
3. Hàm multiply() để nhân f(x) với g(x) trong trường hữu hạn bằng cách tách thành phần của f(x) nhân lần lượt với g(x) rồi cộng kết quả lại
## Hướng dẫn test chương trình
Bước 1: clone repo: git clone https://github.com/trinhvandai05/gf-multiplication.git
Bước 2: di chuyern tới nơi lưu chương trình: cd path
Bước 3: Không cần cài đặt thêm thư viện gì hết. Chạy python run.py --field 4 --f 1011 --g 0110 --m 0x19 --steps
Lưu ý: --field 4/8 là chọn GF(2^4 hoặc 2^8), --f và --g để nhập hàm cần nhân dạng nhị phân, --m để truyền tham số m(x) dạng nhị phân, --steps có hoặc không để hiển thị nhân từng bước
## Benchmark
Bộ benchmark được lưu ở tests/benchmark.json
Để test chương trình tiến hành các bước sau
1. cd test
2. python run_tests.py để test toàn bộ benchmark với từng hàm xor/ xtime/ multiply
3. python run_tests.py --custom để test dựa trên input của người dùng tự muốn kiểm tra
