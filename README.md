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