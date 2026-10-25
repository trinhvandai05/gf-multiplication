
# Em chào cô giáo, code em là cả người cả AI code cho sạch với chuẩn logic ạ

# Nhân hai đa thức trong GF(2^4) và GF(2^8)

Chương trình cài đặt phép nhân hai đa thức trong trường hữu hạn GF(2^4) và GF(2^8), sử dụng phép XOR và phép nhân với x (`xtime`).

Ngôn ngữ: **Python**, không yêu cầu thư viện bên ngoài.

## 1. Phân tích bài toán

Bài toán yêu cầu tính:

$$
h(x)=f(x)g(x)\bmod m(x)
$$

Trong đó:

- `f(x)`, `g(x)` là hai đa thức cần nhân.
- `m(x)` là đa thức bất khả quy xác định trường.
- `h(x)` là kết quả sau phép nhân và lấy dư.

Các hệ số của đa thức thuộc:

$$
GF(2)=\{0,1\}
$$

Một phần tử của GF(2^n) được biểu diễn dưới dạng:

$$
f(x)=f_{n-1}x^{n-1}+\cdots+f_1x+f_0
$$

với mỗi hệ số $f_i$ bằng 0 hoặc 1.

Ví dụ trong GF(2^4):

$$
f(x)=x^3+x+1
$$

Biểu diễn dưới dạng nhị phân:

```text
f(x) = 1011
       ||||
       |||+-- he so x^0 = 1
       ||+--- he so x^1 = 1
       |+---- he so x^2 = 0
       +----- he so x^3 = 1
```

Như vậy, mỗi đa thức có thể biểu diễn bằng một số nguyên, với mỗi bit tương ứng với một hệ số.

## 2. Tư duy phân rã bài toán

Mục tiêu ban đầu là xây dựng hàm:

```python
multiply(f, g, m)
```

Thay vì trực tiếp nhân hai đa thức rồi thực hiện phép chia lấy dư, ta phân tích một đa thức thành các hạng tử.

Giả sử:

$$
f(x)=f_0+f_1x+f_2x^2+\cdots+f_{n-1}x^{n-1}
$$

Khi nhân với $g(x)$:

$$
\begin{aligned}
f(x)g(x)
={}&f_0g(x)+f_1xg(x)\\
&+f_2x^2g(x)+\cdots\\
&+f_{n-1}x^{n-1}g(x)
\end{aligned}
$$

Từ đây ta nhận thấy:

1. Các hệ số $f_i$ chỉ nhận giá trị 0 hoặc 1.
2. Nếu $f_i=0$, bỏ qua hạng tử tương ứng.
3. Nếu $f_i=1$, cộng $x^ig(x)$ vào kết quả.
4. Mỗi hạng tử $x^ig(x)$ có thể được tạo từ hạng tử trước đó bằng cách nhân thêm với $x$.

Do đó, bài toán lớn được phân rã thành hai phép toán cơ sở:

- Cộng hai đa thức bằng XOR.
- Nhân một đa thức với $x$, có rút gọn theo $m(x)$.

Từ hai phép toán này, ta xây dựng được phép nhân tổng quát.

## 3. Hàm XOR — cộng hai đa thức

Trong GF(2), phép cộng được thực hiện theo modulo 2.

| a | b | (a+b) mod 2 | a XOR b |
|---|---|---|---|
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 1 | 1 |
| 1 | 1 | 0 | 0 |

Như vậy, phép cộng hai đa thức tương đương với XOR các hệ số tương ứng.

Ví dụ:

$$
(x^3+x)+(x^2+x+1)=x^3+x^2+1
$$

Biểu diễn nhị phân:

```text
  1010
^ 0111
------
  1101
```

Cài đặt Python:

```python
def xor(a, b):
    return a ^ b
```

Trong Python, toán tử `^` thực hiện XOR theo bit.

Hàm này là phép toán cộng cơ sở, được sử dụng trong cả `xtime()` và `multiply()`.

## 4. Hàm xtime — nhân đa thức với x

Ta xây dựng một hàm thực hiện:

$$
\operatorname{xtime}(g)=xg(x)\bmod m(x)
$$

Giả sử:

$$
g(x)=b_{n-1}x^{n-1}+\cdots+b_1x+b_0
$$

Nhân với $x$:

$$
xg(x)=b_{n-1}x^n+\cdots+b_1x^2+b_0x
$$

Ta xét hai trường hợp.

### 4.1. Trường hợp bit cao nhất bằng 0

Nếu $b_{n-1}=0$, phép nhân không tạo ra hạng tử $x^n$.

Ta chỉ cần dịch trái một bit:

```python
g << 1
```

Ví dụ với 4 bit:

```text
g = 0101

g << 1 = 1010
```

Tương ứng:

$$
x(x^2+1)=x^3+x
$$

Không cần rút gọn.

### 4.2. Trường hợp bit cao nhất bằng 1

Nếu $b_{n-1}=1$, khi nhân với $x$ sẽ xuất hiện hạng tử $x^n$.

Tuy nhiên, phần tử kết quả trong GF(2^n) phải có bậc nhỏ hơn $n$.

Do đó, cần rút gọn theo đa thức bất khả quy $m(x)$.

Viết:

$$
m(x)=x^n+r(x)
$$

Vì:

$$
m(x)\equiv0\pmod{m(x)}
$$

nên trong GF(2):

$$
x^n\equiv r(x)\pmod{m(x)}
$$

Như vậy, sau khi dịch trái và loại bỏ bit vượt quá $n$ bit, ta XOR với phần $r(x)$ của đa thức bất khả quy.

### 4.3. Công thức tổng quát

Đặt:

```python
BITS = n
MASK = (1 << BITS) - 1
TOP_BIT = 1 << (BITS - 1)
```

Khi đó:

```text
shifted = (g << 1) & MASK

Neu bit cao nhat cua g = 1:
    shifted = shifted XOR (m & MASK)

Tra ve shifted
```

Trong đó:

- `BITS`: số bit của trường.
- `MASK`: mặt nạ giữ $n$ bit thấp.
- `TOP_BIT`: mặt nạ kiểm tra bit cao nhất.
- `m & MASK`: phần đa thức dùng để thay thế $x^n$.

### 4.4. Ví dụ trong GF(2^4)

Chọn đa thức bất khả quy:

$$
m(x)=x^4+x+1
$$

Biểu diễn:

```text
m(x) = 10011 = 0x13
```

Ta có:

$$
x^4\equiv x+1\pmod{m(x)}
$$

Giả sử:

$$
g(x)=x^3+x
$$

Dạng nhị phân:

```text
g = 1010
```

Bit cao nhất bằng 1.

Thực hiện:

```text
g             = 1010
g << 1        = 10100
Lay 4 bit thap=  0100

m & 1111      =  0011

                  0100
                ^ 0011
                ------
                  0111
```

Kết quả:

$$
\operatorname{xtime}(g)=x^2+x+1
$$

Cài đặt:

```python
def xtime(g, m):
    carry = g & TOP_BIT

    shifted = (g << 1) & MASK

    if carry:
        shifted = xor(shifted, m & MASK)

    return shifted
```

Như vậy, `xtime()` vừa thực hiện phép nhân với $x$, vừa đảm bảo kết quả được rút gọn theo $m(x)$.

## 5. Xây dựng hàm multiply(f, g, m)

Sau khi có `xor()` và `xtime()`, ta có thể xây dựng phép nhân hai đa thức bất kỳ.

Nhắc lại:

$$
f(x)=\sum_{i=0}^{n-1}f_ix^i
$$

Do đó:

$$
f(x)g(x)=\sum_{i=0}^{n-1}f_ix^ig(x)
$$

Đặt:

$$
G_0(x)=g(x)
$$

$$
G_{i+1}(x)=\operatorname{xtime}(G_i(x))
$$

Các hạng tử lần lượt là:

$$
G_0=g,\quad G_1=xg,\quad G_2=x^2g,\ldots
$$

với mỗi hạng tử đều được rút gọn theo $m(x)$.

Khi đó:

$$
\boxed{
h(x)=\bigoplus_{i=0}^{n-1}f_iG_i(x)
}
$$

Chỉ những hạng tử có $f_i=1$ mới được XOR vào kết quả.

### 5.1. Thuật toán

```text
Input: f, g, m

result = 0
term = g

For i = 0 to n-1:

    fi = (f >> i) & 1

    If fi == 1:
        result = XOR(result, term)

    If i < n-1:
        term = xtime(term, m)

Return result
```

Giải thích:

- `result`: biến lưu tổng các hạng tử đã được chọn.
- `term`: hạng tử hiện tại, bằng $x^ig(x)\bmod m(x)$.
- `(f >> i) & 1`: lấy hệ số $f_i$.
- `xor(result, term)`: cộng hạng tử vào kết quả.
- `xtime(term, m)`: sinh hạng tử tiếp theo.

### 5.2. Cài đặt

```python
def multiply(f, g, m):
    result = 0
    term = g

    for i in range(BITS):
        bit = (f >> i) & 1

        if bit:
            result = xor(result, term)

        if i < BITS - 1:
            term = xtime(term, m)

    return result
```

Đây là toàn bộ logic toán học của phép nhân.

Thuật toán có $n$ vòng lặp, sử dụng một số phép toán bit cố định trong mỗi vòng đối với hai trường 4 bit và 8 bit.

## 6. Ví dụ tính toán đầy đủ

Xét trong GF(2^4):

$$
f(x)=x^3+x+1
$$

$$
g(x)=x^2+1
$$

$$
m(x)=x^4+x+1
$$

Biểu diễn:

```text
f = 1011
g = 0101
m = 10011
```

Phân tích:

$$
f(x)=x^3+x+1
$$

Nên:

$$
f(x)g(x)=x^3g(x)+xg(x)+g(x)
$$

Các giá trị tạo ra bởi `xtime()`:

| i | f_i | x^i*g mod m | result |
|---|---|---|---|
| 0 | 1 | 0101 | 0101 |
| 1 | 1 | 1010 | 1111 |
| 2 | 0 | 0111 | 1111 |
| 3 | 1 | 1110 | 0001 |

Tổng XOR:

```text
  0101
^ 1010
^ 1110
------
  0001
```

Vậy:

$$
\boxed{
f(x)g(x)\bmod m(x)=1
}
$$

Kết quả:

```text
Binary: 0001
Hex:    0x1
Decimal: 1
```

## 7. Tổ chức chương trình

```text
GF_Polynomial_Multiplication/
│
├── gf2m4.py
├── gf2m8.py
├── run.py
├── README.md
│
└── .vscode/
    ├── tasks.json
    └── launch.json
```

### gf2m4.py

Cài đặt phép nhân trong GF(2^4).

Các hằng số:

```python
BITS = 4
MASK = 0b1111
TOP_BIT = 0b1000
```

Danh sách đa thức bất khả quy:

```python
MODULI = (0x13, 0x19, 0x1F)
DEFAULT_MODULUS = 0x13
```

Ba hàm toán học:

```python
xor(a, b)
xtime(g, m)
multiply(f, g, m)
```

### gf2m8.py

Cài đặt cùng thuật toán nhưng áp dụng cho GF(2^8).

Các hằng số:

```python
BITS = 8
MASK = 0b11111111
TOP_BIT = 0b10000000
```

Đa thức mặc định:

```python
DEFAULT_MODULUS = 0x11B
```

Chương trình có danh sách 30 đa thức bất khả quy bậc 8.

Ba hàm toán học vẫn là:

```python
xor(a, b)
xtime(g, m)
multiply(f, g, m)
```

Như vậy, hai trường sử dụng cùng một ý tưởng thuật toán. Khác biệt chính là số bit và đa thức bất khả quy.

### run.py

`run.py` là chương trình điều khiển.

Nó thực hiện:

1. Nhận tham số từ terminal.
2. Xác định trường GF(2^4) hoặc GF(2^8).
3. Chuyển dữ liệu nhị phân sang số nguyên.
4. Lựa chọn đa thức bất khả quy.
5. Gọi `run_gf4()` hoặc `run_gf8()`.
6. In kết quả ở dạng đa thức, nhị phân, hexadecimal và thập phân.

Các hàm này phục vụ nhập và xuất, không làm thay đổi thuật toán nhân.

## 8. Hướng dẫn sử dụng run.py

Yêu cầu: Python 3.9 trở lên.

Không cần cài thêm thư viện.

Mở terminal trong thư mục project.

### 8.1. Nhân trong GF(2^4)

```powershell
py run.py --field 4 --f 1011 --g 0101
```

Mặc định sử dụng:

$$
m(x)=x^4+x+1
$$

Kết quả:

```text
h(x) = f(x)*g(x) mod m(x) = 1
Nhi phan: 0001
Hex: 0x1
Thap phan: 1
```

### 8.2. Nhập cả đa thức m(x)

```powershell
py run.py --field 4 --f 1011 --g 0101 --m 0x13
```

Các lựa chọn cho GF(2^4):

| m(x) | Hex |
|---|---|
| x^4 + x + 1 | 0x13 |
| x^4 + x^3 + 1 | 0x19 |
| x^4 + x^3 + x^2 + x + 1 | 0x1F |

### 8.3. Hiển thị từng vòng lặp

```powershell
py run.py --field 4 --f 1011 --g 0101 --m 0x13 --steps
```

Tham số `--steps` giúp quan sát:

- Hệ số $f_i$ đang xét.
- Hạng tử $x^ig(x)$.
- Kết quả sau mỗi phép XOR.

### 8.4. Nhân trong GF(2^8)

Ví dụ:

```powershell
py run.py --field 8 --f 01010111 --g 10000011 --m 0x11B --steps
```

Với:

$$
m(x)=x^8+x^4+x^3+x+1
$$

Kết quả:

```text
h(x) = x^7 + x^6 + 1
Nhi phan: 11000001
Hex: 0xC1
Thap phan: 193
```

### 8.5. Liệt kê đa thức bất khả quy

Đối với GF(2^4):

```powershell
py run.py --field 4 --list-moduli
```

Đối với GF(2^8):

```powershell
py run.py --field 8 --list-moduli
```

### 8.6. Kiểm tra biên dịch

```powershell
py run.py --compile
```

Lệnh này sử dụng `py_compile` để kiểm tra cú pháp và tạo bytecode `.pyc`.

Python không yêu cầu biên dịch trước khi chạy.

Có thể kết hợp kiểm tra cú pháp và chạy:

```powershell
py run.py --compile --field 4 --f 1011 --g 0110
```

### 8.7. Xem trợ giúp

```powershell
py run.py --help
```

### 8.8. Các tham số hỗ trợ

| Tham số | Ý nghĩa |
|---|---|
| `--field` | Chọn trường 4 hoặc 8 |
| `--f` | Đa thức f(x) dạng nhị phân |
| `--g` | Đa thức g(x) dạng nhị phân |
| `--m` | Đa thức bất khả quy dạng số nguyên, ví dụ 0x13 |
| `--steps` | Hiển thị từng bước tính |
| `--list-moduli` | Liệt kê các đa thức bất khả quy |
| `--compile` | Kiểm tra cú pháp chương trình |
| `--help` | Xem hướng dẫn tham số |

Lưu ý:

- `--f` và `--g` được nhập dưới dạng nhị phân.
- `--m` có thể nhập ở dạng hexadecimal như `0x13`.
- Giá trị đầu vào không được vượt quá số bit của trường.
- Nếu không nhập `--field`, mặc định là GF(2^4).
- Nếu không nhập `--m`, chương trình sử dụng đa thức bất khả quy mặc định.

Trên Linux/macOS có thể thay `py` bằng `python3`.

## 9. Chạy bằng VS Code

### Cách 1: Sử dụng terminal

1. Mở thư mục project trong VS Code.
2. Chọn `Terminal > New Terminal`.
3. Nhập lệnh, ví dụ:

```powershell
py run.py --field 4 --f 1011 --g 0101 --m 0x13 --steps
```

### Cách 2: Sử dụng Ctrl + Shift + B

1. Mở nguyên thư mục project.
2. Chọn Python interpreter.
3. Nhấn `Ctrl + Shift + B`.
4. Chọn trường GF(2^4) hoặc GF(2^8).
5. Nhập f và g dưới dạng nhị phân.

VS Code sẽ sử dụng cấu hình trong `.vscode/tasks.json` để chạy chương trình.

Task này dùng đa thức bất khả quy mặc định và hiển thị các bước tính.

### Cách 3: Debug bằng F5

Nhấn `F5`, sau đó chọn cấu hình tương ứng:

- `GF(2^4): F5`
- `GF(2^8): F5`

Có thể thay các giá trị `args` trong `.vscode/launch.json` để thay đổi dữ liệu đầu vào.

## 10. Kết luận

Bài toán ban đầu là:

$$
f(x)g(x)\bmod m(x)
$$

Thay vì triển khai trực tiếp một thuật toán nhân và chia đa thức phức tạp, ta phân rã bài toán:

```text
Bai toan nhan hai da thuc
            |
            v
   Phan tich f(x) thanh
   f0 + f1*x + ... + fn*x^n
            |
            v
    Can hai phep toan
       /         \
      v           v
  xor(a,b)    xtime(g,m)
      \           /
       \         /
        v       v
     multiply(f,g,m)
            |
            v
     h(x) = f*g mod m
```

Trong đó:

- `xor()` thực hiện phép cộng.
- `xtime()` thực hiện phép nhân với x và rút gọn.
- `multiply()` phân tích f(x) theo các hệ số và sử dụng hai hàm trên để tạo tích.

Nhờ vậy, phần lõi toán học chỉ gồm **3 hàm nhỏ**, có thể áp dụng cho cả GF(2^4) và GF(2^8) mà không cần thay đổi ý tưởng thuật toán.
