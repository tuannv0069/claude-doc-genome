---
scope: project
documentType: Implementation Report
status: Implemented
completedAt: 2026-09-16
sourceVersion: 4.0.0
preparedVersion: 5.0.0
---

# Kết quả viết lại genome

## §1 Kết quả trong repository gốc

Đã triển khai bản viết lại tại `D:/Code/claude-doc-genome`. Bộ phân phối hiện chỉ dành cho Claude Code. Toàn bộ 39 file Markdown và template còn lại đã được viết lại bằng câu đầy đủ, cùng với việc rà soát và sửa các công cụ có phụ thuộc vào cấu trúc cũ.

Bộ nguồn không còn `document-writer`, `rule-writing-standards.md`, `conversational-output.md` hay cơ chế triển khai Codex. Các hướng dẫn chung chỉ giữ trách nhiệm và quy trình làm việc. Khả năng đọc hiểu được dùng để biên soạn lần thay đổi này; không có một rule văn phong chung mới để thay chỗ bộ cũ.

Từ danh mục 61 file ban đầu, chín file được loại và 52 file được giữ lại có thay đổi. Trong số còn lại có 42 file portable, bảy template và ba file cấp skill. Toàn bộ 42 cặp live–bundle khớp byte. Danh mục gốc và hash nằm trong [thiết kế gốc](thiet-ke-goc.md); phạm vi đã thống nhất nằm trong [kế hoạch](ke-hoach-viet-lai.md).

Phiên bản 5.0.0 đã được chuẩn bị cục bộ và đồng bộ với metadata, README cùng manifest của repo. Chưa commit, push, tạo tag hoặc phát hành. Genome trong Hi Tuấn C và các project sử dụng khác chưa được triển khai lại; hai tài liệu kế hoạch cũ tại Hi Tuấn C đã chuyển thành con trỏ tới nguồn chính thức.

## §2 Những thay đổi về hành vi

Các giới hạn từ, dòng, số câu và khuôn trình bày chung đã được bỏ khỏi rule, guide, role, template và gate. Những dữ liệu thật sự được chương trình đọc, như trường metadata, cột router, định danh mục và chứng cứ wiki, vẫn có hợp đồng rõ ràng.

Quy trình sử dụng quyền thực hiện người dùng đã cấp, thay vì yêu cầu xác nhận lặp lại. Việc chưa rõ phạm vi vẫn cần được làm rõ. Vai trò phần mềm chỉ được chọn cho công việc phần mềm; kịch bản và nội dung sáng tạo sử dụng vai trò của project hoặc đi theo nhánh không có vai trò phù hợp. Kiểm tra chung vẫn giữ việc truy nguồn, phân tích phụ thuộc và xác minh kết quả.

Updater và manifest dùng chung map sáu nhóm portable và bảy template. Bản cập nhật giữ các sửa đổi cục bộ, chỉ xóa file nghỉ dùng khi có hash sở hữu khớp, và chưa ghi phiên bản hoàn tất nếu còn conflict hoặc template chưa được hợp nhất. Việc xác nhận template ghi nhận một lần review đã hoàn thành, không tự sửa các giá trị riêng của project.

Công cụ triển khai kiểm tra đường dẫn, liên kết tượng trưng, hard link, tên trùng do khác hoa thường trên Windows và sự hiện diện của các file gốc bắt buộc. Scanner đọc được đoạn văn nhiều dòng và lịch sử UTF-8 trên Windows. Một lần xác nhận drift gắn với nội dung đích đã được xem xét; thay đổi đích sau đó sẽ được phát hiện lại.

## §3 Bằng chứng kiểm tra

| Phần kiểm tra | Kết quả thực tế |
|---|---|
| Danh mục và bản sao portable | Đã đối chiếu 61 file đầu vào; 42 cặp live–bundle khớp hoàn toàn. |
| Công cụ triển khai Node | 18 ca đạt, không có ca lỗi hoặc bỏ qua trên máy Windows hiện tại. |
| Công cụ portable Python | Cả sáu bộ kiểm thử đều đạt. |
| Dữ liệu live | Gate bài học, vai trò, quyết định và wiki đều đạt. Các quyết định có nguồn đã nghỉ dùng được giữ lại với cảnh báo lịch sử hợp lệ. |
| Tài liệu và phiên bản | Doc lint và kiểm tra đồng bộ phiên bản đều đạt. |
| Project cài thử độc lập | Đã cài 42 file portable, tạo manifest với bảy template, chạy các gate thành công; updater không báo thêm, sửa, xóa hay conflict. |
| Template wiki | Bảng chứng cứ được thử với một, hai và ba trục; header, separator và dữ liệu có số cột tương ứng bằng nhau. |
| Rule-health | Đã xem xét 62 tín hiệu, gồm 56 tham chiếu cần đối chiếu sau khi viết lại và sáu trường hợp định tuyến hoặc module tùy chọn hợp lệ; lần quét sau không còn finding mở. |

Review độc lập các guide, role và template phát hiện việc chọn sai vai trò cho nội dung sáng tạo, separator wiki thiếu cột, mô tả phạm vi scanner chưa chính xác và gate còn áp vị trí heading. Các lỗi này đã được sửa và được người review kiểm tra lại.

Review độc lập công cụ triển khai phát hiện ba lỗi khác: ghi xuyên hard link, xử lý không nhất quán tên file khác hoa thường trên Windows, và ghi nhận hoàn tất khi thiếu các file gốc đã render. Các bản sửa đã được kiểm thử bằng tình huống tái hiện cụ thể. Vòng kiểm tra hồi quy cuối của phần mã này do agent chính thực hiện.

CI đã được cập nhật để chạy kiểm tra phiên bản, doc lint, các fixture triển khai và các bộ kiểm tra Python. Các lệnh đã chạy cục bộ thành công; workflow CI từ xa chưa chạy vì chưa push.

Danh mục file, hash và mã thoát của các lệnh kiểm tra được lưu trong [hồ sơ kiểm chứng](kiem-chung.json).

## §4 Kết quả thử đầu ra bằng Claude

Sau khi tài khoản được cấp lại lượt sử dụng, đã chạy 12 lượt viết đối chứng bằng Claude Opus 4.6, hai lượt hiệu chuẩn và một lượt đánh giá độc lập với nhãn cũ–mới được ẩn. Kết quả không đồng đều; chưa đủ cơ sở để khẳng định vấn đề văn phong đã được giải quyết. Các mẫu nguyên văn, nhận xét theo từng loại bài và giới hạn phép thử nằm trong [báo cáo so sánh đầu ra](so-sanh-dau-ra-claude.md).

Phép thử phát hiện bản mới bỏ qua hai mục tra cứu đầu nhiệm vụ trong cả sáu lượt ban đầu. Đã làm rõ hành động đọc và phạm vi áp dụng trong `CLAUDE.md` cùng template; sáu lượt thử sau sửa đều đọc đủ. Tuy nhiên, các câu trả lời vẫn thêm thông tin quy trình không phục vụ đầu ra được yêu cầu. Bộ nguồn giữ phạm vi hướng dẫn công việc và không thêm lại quy định văn phong chung. Chưa triển khai sang project sử dụng, commit hay push.
