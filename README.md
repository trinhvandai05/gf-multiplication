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

## Đối chiếu kết quả
Sau khi chạy lệnh python run_tests.py ta thu được kết quả sau:
PS D:\HUST\20261\ltmm\deadline2510\tests> python run_tests.py

Kiem traGF(2^4)
kiem tra xor(10, 7) -> True
kiem tra xor(15, 15) -> True
kiem tra xor(5, 3) -> True
kiem tra xor(0, 11) -> True
kiem tra xtime(0, 19) -> True
kiem tra xtime(1, 19) -> True
kiem tra xtime(5, 19) -> True
kiem tra xtime(10, 19) -> True
kiem tra xtime(8, 19) -> True
kiem tra xtime(8, 25) -> True
kiem tra xtime(8, 31) -> True
kiem tra multiply(0, 11, 19) -> True
kiem tra multiply(1, 11, 19) -> True
kiem tra multiply(11, 5, 19) -> True
kiem tra multiply(11, 6, 19) -> True
kiem tra multiply(2, 8, 25) -> True
kiem tra multiply(2, 8, 31) -> True
kiem tra multiply(15, 15, 19) -> True

Kiem traGF(2^8)
kiem tra xor(87, 131) -> True
kiem tra xor(255, 255) -> True
kiem tra xor(0, 170) -> True
kiem tra xor(160, 15) -> True
kiem tra xtime(0, 283) -> True
kiem tra xtime(1, 283) -> True
kiem tra xtime(87, 283) -> True
kiem tra xtime(174, 283) -> True
kiem tra xtime(71, 283) -> True
kiem tra xtime(142, 283) -> True
kiem tra xtime(128, 283) -> True
kiem tra xtime(128, 285) -> True
kiem tra multiply(0, 131, 283) -> True
kiem tra multiply(1, 131, 283) -> True
kiem tra multiply(87, 19, 283) -> True
kiem tra multiply(87, 131, 283) -> True
kiem tra multiply(2, 128, 283) -> True
kiem tra multiply(2, 128, 285) -> True
kiem tra multiply(83, 202, 283) -> True

Kiem tra toan bo chuong trinh
kiem tra full GF(2^4) -> True
kiem tra full GF(2^4) -> True
kiem tra full GF(2^8) -> True

Tong ket: 40/40 dung

PS D:\HUST\20261\ltmm\deadline2510\tests> python run_tests.py --custom
GF(2^4) hay GF(2^8)? (4/8): 4
Ham (xor/xtime/multiply/full): xor
a (binary): 1011
b (binary): 0101
Dap an dung (binary): 1110

kiem tra xor -> True
Ket qua thuc te: 1110

Tham số --custom để người dùng tự kiểm tra với test key của mình
