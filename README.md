# HTB-Under-Construction
Vào dịp cuối năm trong lúc mọi người đang bận rộn dọn dẹp nhà cửa, sắp sửa đồ mới đón tết thì mình nhận được một challenge HackTheBox ở mức medium từ một người anh vừa mới quen qua một nhóm học tập trên facebook.
Challenge này cho mình hẳn source web, sau khi tải source về và wow NodeJs, mình mù tịt với ngôn ngữ này :((. Đi sơ qua một vòng mình thấy có 2 file _JWWTHelper.js_ và _DBHelper.js_ làm mình nghĩ đến ***JWT attack*** và ***SQL injection***. 
Đọc qua file _DBHelper.js_ thấy được các câu truy vấn không được lọc kĩ càng gì cả. Nhưng mình lại chưa biết làm thế nào để có thể inject vào các câu truy vấn đó được. Thôi thì quay qua đọc file _JWTHelper.js_ xem như thế nào.
Có vẻ như là public key được lồng ở trong token của user (mình đoán vậy kkkk). Để chắc chắn cho suy đoán của mình thì mình đã đăng ký một user và đăng nhập với user vừa tạo để lấy giá trị session đem lên JWT.io kiểm chứng.
![image](https://user-images.githubusercontent.com/94473469/151861915-52a6b594-2ca4-4a2d-8f1a-3a39cd11e210.png)
Bởi vì có public key nên mình nghĩ chắc chắn phải có gì đó liên quan đến authen. Thử google một vòng với từ khoá `JWT authen attack`. Mình phát hiện được [hacktricks](https://book.hacktricks.xyz/pentesting-web/hacking-jwt-json-web-tokens#change-the-algorithm-rs256-asymmetric-to-hs256-symmetric-cve-2016-5431-cve-2016-10555) có viết về kĩ thuật thay đổi thuật toán từ RS256 sang HS256. 
Check lại thuật toán JWT ở challenge này thì tình cờ thấy nó dùng thuật toán HS256. [Google theo kĩ thuật này mình đã được thông não] (https://habr.com/en/post/450054/).
Do thuật toán HS256 sử dụng khoá bí mật để đánh dấu và xác thực mỗi message, còn thuật toán RS256 thì sử dụng private key để đánh dấu message và public key để xác thực athen. Vì vậy, nếu thay đổi từ thuật toán RS256 sang HS256 thì public key sẽ được sử dụng như khoá bí mật và khi đó thuật toán HS256 dùng để xác thực chữ ký.
Sau khi thực hiện theo các bước ở site trên mình đã tạo ra được một token mới với thuật toán **HS256** và **user admin**. Tiến hành inject token mới để bypass authen thì mình lại nhận được một kết quả khá là hụt hẫn với thông tin là ***user admin không tồn tại :((((***.
![image](https://user-images.githubusercontent.com/94473469/151865255-57f93480-dda0-4363-bead-dcb8e7faf473.png)
Trong message ở hình trên có nhắc đến database mình nghĩ ngay đến file _DBHelper.js_ lúc nãy. Trong file mình thấy có hàm checkUser. Mình đoán kiểu gì khi login hàm này cũng được gọi ra.
![image](https://user-images.githubusercontent.com/94473469/151866758-04c1d864-7c8d-461f-b079-73b0dd40287d.png)
Với kinh nghiệm đã từng dev web laravel mình check thử một vòng trong thư mục routes. Cuối cùng mình cũng đã tìm được route login.
![image](https://user-images.githubusercontent.com/94473469/151867184-df99d1bf-d240-48e2-9340-a33ab2cde224.png)
Khi login hàm **checkUser** sẽ được gọi ra và truy vấn xuống database. Input truyền vào chính là username nằm trong phần data của token.
Mình cũng không rõ lắm về cú pháp của sqlite nên mình chèn đại cú pháp union của mysql xem kết quả trả về như thế nào :))).
![image](https://user-images.githubusercontent.com/94473469/151867946-0290a535-6648-42ce-8e88-827f94b3acf2.png)
Wow chính nó, chính là sql injection đây mà. Do không rành về cú pháp sqlite nên mình google dùng một vài payload trên [git] (https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/SQLite%20Injection.md).
Thả nhẹ payload `Extract table name` thì mình có được table ***flag_storage***
![image](https://user-images.githubusercontent.com/94473469/151868780-40c0c85e-6376-4c3a-b36c-89e0e99269a1.png)
Hy vọng flag nằm trong table này. Minh tiếp tục lấy cột trong table và nội dung của cột chứa flag.
![image](https://user-images.githubusercontent.com/94473469/151869160-70667db3-5e02-4c02-bfd3-47f2b92fd730.png)
![image](https://user-images.githubusercontent.com/94473469/151869262-cadf3065-9ad4-47ba-ba62-556924989b3e.png)
Đem flag vừa tìm lên HTB submit 
> thành công.

# POC
![image](https://user-images.githubusercontent.com/94473469/152088040-f523b90f-4a42-493c-a0af-1583678ce01a.png)

###### Cám ơn các bạn đã ghé qua đây :))))
