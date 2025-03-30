# Hashiwokakero
This project explores AI techniques to solve the Hashiwokakero (Bridges) puzzle, a logic-based game where islands (nodes) must be connected with bridges while following specific constraints. 
### Chạy code generate_CNF
```bash
cd generate_CNF
```
```bash
py main.py
```
- sẽ thấy được file CNF được sinh ra trong thư mục `generate_CNF/data`
- dựa vào đó để áp dụng các thuật toán A*/Brute Force/Backtracking để giải bài toán
- đề xuất tạo code thuật toán trong thư mục `generate_CNF/func` để dễ quản lý
- khi chạy thuật toán chỉ cần chạy hàm trong `main.py` và truyền vào file CNF đã sinh ra
- có thể tham khảo bên nhánh 'tan' để xem cách giải bằng pySAT

## Make sure you have the python-sat library installed
To install the library, run the following command in your terminal:
```bash
pip install python-sat
```
## Choose method to run by changing directory
There are 3 methods to solve the problem. You can choose the method you want to run by changing the directory to the method you want to run. Here is the list of methods:
- 1: Brute force
```bash
cd brute-force
```
- 2: Backtracking
```bash
cd backtracking
```
- 3: SAT
```bash
cd pySAT
```

## How to run the code
To run the code, run the following command in your terminal:
```bash
py main.py
```
Enter your number of input your want to test, then enter the input. The output file will be created in output folder.

## Description of the input
- input 1 is sample in the assignment
- input 2 is sample in the assignment
- input 3 is sample in the assignment
- input 4 and 5, I created them by myself to test the code
- input 5 is 6x6
- input 6 is 7x7
- input 7 is 11x11
- input 8 is 13x13
- input 9 is 17x17
- input 10 is 20x20