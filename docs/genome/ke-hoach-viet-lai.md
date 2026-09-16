---
scope: project
documentType: Rewrite Plan
status: Implemented
source: skills/init-project
sourceVersion: 4.0.0
plannedAt: 2026-09-15
---

# Kế hoạch viết lại genome cho Claude Code

## §1 Mục tiêu và quyền thực hiện

Viết lại toàn bộ hướng dẫn trong repository `D:/Code/claude-doc-genome` bằng câu đầy đủ, đúng ngữ pháp và dễ hiểu đối với con người. Người dùng đã cho phép triển khai ngay sau khi sửa kế hoạch, tự xử lý các bước thực hiện và kiểm tra mà không chờ xác nhận thêm. Không commit, push, tạo tag hoặc phát hành trong công việc này.

Khả năng đọc hiểu là tiêu chí biên soạn và nghiệm thu của lần viết lại, không phải chính sách văn phong mới được phân phối cho các project. Genome chỉ sở hữu hướng dẫn và quy trình làm việc của AI. Yêu cầu riêng về giọng văn, số câu, từ nên dùng, heading, bảng hay cách mở đầu và kết thúc phải thuộc hướng dẫn riêng của loại sản phẩm đó tại project sử dụng.

Loại bỏ skill `document-writer` và toàn bộ cơ chế triển khai Codex. Chỉ giữ Claude Code trong bundle, quy trình cài đặt, công cụ bảo trì và tài liệu sử dụng. Giữ quyết định và changelog lịch sử để truy nguyên. Không triển khai thay đổi sang Hi Tuấn C hay project khác trong đợt này.

## §2 Thiết kế cần bảo toàn

Giữ mô hình một nguồn chuẩn cho mỗi yêu cầu, phân biệt dữ liệu portable với dữ liệu project, định tuyến hướng dẫn khi cần, kiểm tra bằng chứng, quản lý tác động của thay đổi, ghi nhớ bài học và quyết định, cùng cơ chế đưa cải tiến từ bản sử dụng về bundle. Giữ hợp đồng dữ liệu có chương trình đọc nếu còn hữu ích; sửa cả producer, consumer và kiểm thử khi thay hợp đồng.

Không giữ câu chữ cũ vì nó đã tồn tại hoặc đang được test bằng so khớp chuỗi. Bỏ các giới hạn từ, dòng và số câu phục vụ nén chữ. Các trường cần thiết cho bằng chứng và vận hành vẫn được giữ, nhưng không biến chúng thành khuôn trình bày bắt buộc cho mọi tài liệu của người dùng.

## §3 Nguồn chỉnh sửa và theo dõi

Bản gốc ở commit `13fc9fa26e9e7d54e0cc58c818d196d5b284cd52`, phiên bản 4.0.0, gồm 61 file dưới `skills/init-project/`. Danh mục và hash ban đầu đã được lưu trong vùng làm việc. [Thiết kế gốc](thiet-ke-goc.md) mô tả bản này, không phải hướng dẫn triển khai mới.

Sửa portable ở bản live trước: `.claude/rules/`, `.agent-workspace/guide/general/`, `.agent-workspace/guide/roles/` và `.agent-workspace/tooling/`. Sau khi kiểm tra, chép chính xác về nhóm tương ứng trong bundle. Template, `SKILL.md` và script cấp repo được sửa trực tiếp. Không viết lại lịch sử bài học và quyết định để chúng trông như được soạn theo tiêu chí mới.

Mỗi nhóm có danh sách file, báo cáo thay đổi ý nghĩa và bằng chứng trong `.agent-workspace/tasks/genome-natural-language/`. Người kiểm tra độc lập đọc bản hoàn chỉnh. Các nhóm chạy song song sở hữu những file riêng; tích hợp và kiểm tra liên kết diễn ra sau khi chúng hoàn tất.

## §4 Các đợt thực hiện

### P0. Chuẩn bị và thu hẹp phạm vi

Ghi nhận thiết kế và danh mục nguồn. Xóa `document-writer`, renderer và test Codex, tiêu chuẩn Codex, guide về hai harness và bề mặt Codex của repo. Sửa router, manifest, hook, metadata và hướng dẫn liên quan. Không xóa file ở các project đã cài trước đây.

### P1. Viết lại rule và kiến trúc tài liệu

Xóa `rule-writing-standards.md` và `conversational-output.md` ở live và bundle. Viết lại các rule còn lại bằng câu đầy đủ; chuyển trách nhiệm công việc hữu ích sang nguồn sở hữu. Viết lại `doc-system-mechanics.md`, `markdown.md` và `mermaid.md`. Giữ liên kết, phạm vi, cú pháp và dữ liệu cần thiết; bỏ chính sách trình bày chung. Cập nhật những nơi dẫn đến hai file đã xóa.

### P2. Viết lại quy trình và vai trò

Viết lại toàn bộ guide còn lại, bảy vai trò và router vai trò. Bảo toàn các bước truy nguồn, lập kế hoạch, sửa lỗi, review, kiểm chứng, phân công và quản lý vùng làm việc. Bỏ khung câu và giới hạn độ dài của báo cáo, bài học, quyết định và vai trò. Ghi rõ thay đổi hành vi nếu việc bỏ khuôn trình bày làm đổi hợp đồng mà công cụ đang đọc.

### P3. Viết lại template và quy trình triển khai

Viết lại bảy template, `skills/init-project/SKILL.md`, hướng dẫn bảo trì và root `CLAUDE.md` để toàn bộ chỉ dẫn được nạp sau cài đặt dùng cách diễn đạt mới. Giữ placeholder và metadata cần thiết. Không sinh Codex và không thêm skill viết tài liệu chung để thay thế.

### P4. Cập nhật công cụ theo thiết kế mới

Rà soát các script Python còn lại và bốn script Node. Loại gate khóa số dòng, số từ hoặc câu chữ. Scanner cần xử lý đoạn văn nhiều dòng; test trigger kiểm tra hợp đồng định tuyến thay vì buộc giữ câu tiếng Anh cũ. Gate role, decision, lesson và wiki tiếp tục kiểm tra dữ liệu, bằng chứng và liên kết.

Sửa đồng thời updater và manifest để quản lý đủ roles, tooling và bảy template. Bổ sung xử lý file nghỉ dùng: chỉ tự xóa file có bằng chứng là bản genome chưa bị sửa; giữ sửa đổi cục bộ và báo conflict khi không chứng minh được quyền sở hữu. Không ghi phiên bản hoàn tất khi còn conflict hoặc template chưa được xử lý. Kiểm thử cập nhật sạch, thêm file, xóa file, sửa đổi cục bộ và template project trên fixture; không chạy cập nhật thật lên project người dùng.

### P5. Tích hợp và kiểm tra độc lập

Đối chiếu hash live–bundle, kiểm tra liên kết vận hành và bảo đảm không còn yêu cầu đọc nguồn đã xóa. Chạy các test có liên quan, doc lint và kiểm tra phiên bản. Kiểm tra cài mới và cập nhật trên project tạm. Đọc lại Markdown được phân phối để tìm câu thiếu nghĩa, mâu thuẫn hoặc quy tắc văn phong còn sót.

Các tình huống đánh giá gồm hội thoại, giải thích kỹ thuật, lập kế hoạch, tài liệu khách hàng, lời kể tiếng Việt và cập nhật project đã sửa cục bộ. Với tài liệu và lời kể, kiểm tra genome không tự áp khuôn hành văn. Nếu chạy so sánh bằng phiên Claude thực tế, dùng hai project độc lập ngoài repo (`baseline-claude`, `new-claude`), cùng model và cấu hình; kiểm kê chỉ dẫn cấp người dùng và thư mục cha. Không dùng phiên hiện tại còn mang rule cũ làm thử nghiệm cô lập. Nếu chưa thực hiện được phép so sánh thực tế, ghi đúng giới hạn đó.

### P6. Bàn giao

Chuẩn bị phiên bản major mới bằng `scripts/sync-version.mjs` vì bundle loại thành phần cũ. Ghi kết quả, kiểm tra và giới hạn vào `ket-qua-viet-lai.md`. Bản làm việc hoàn tất trong repo gốc để người dùng xem diff. Phát hành và triển khai sang project khác là thao tác riêng sau này.

## §5 Điều kiện hoàn thành

Mọi file hướng dẫn đang phân phối đã được đọc và viết lại hoặc có lý do kỹ thuật cụ thể để giữ nguyên dữ liệu. Không còn chính sách văn phong chung, `document-writer` hay đường triển khai Codex. Quy trình và công cụ thống nhất về nơi đặt file, schema và cách cập nhật. Ghi nhận thay đổi ý nghĩa; không giấu việc bỏ trách nhiệm công việc trong lần sửa câu chữ.

Bản triển khai vượt qua kiểm tra cấu trúc, test hành vi công cụ và review độc lập. Bằng chứng chỉ phản ánh điều đã thực hiện. Chất lượng đầu ra Claude trên project thật vẫn cần phản hồi sau triển khai; không cam kết mức cải thiện chưa đo.

Kết quả thực hiện và những giới hạn kiểm chứng được ghi trong [báo cáo triển khai](ket-qua-viet-lai.md).
