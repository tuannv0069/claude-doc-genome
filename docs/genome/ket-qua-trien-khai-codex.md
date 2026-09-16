---
scope: project
documentType: Implementation Report
status: Implemented with client verification limits
implementedAt: 2026-09-16
baselineCommit: 156a886
---

# Kết quả xây dựng genome độc lập cho Codex

Báo cáo này ghi kết quả của đợt triển khai ban đầu. Nguồn Codex sau đó đã chuyển về một skill duy nhất tại `skills/init-codex-genome/`; [báo cáo tổ chức lại nguồn](to-chuc-nguon-codex.md) mô tả cấu trúc và lệnh hiện hành. Các tên đường dẫn, cây live và lệnh `promote` dưới đây được giữ để đọc đúng bằng chứng của đợt thử trước.

## Sản phẩm đã được xây dựng

Bộ Codex nằm hoàn toàn trong [`codex/`](../codex/index.md), có phiên bản riêng `1.0.0`. Bộ Claude giữ phiên bản `5.0.0`, nguồn portable, bundle và công cụ triển khai hiện có. Hai bộ không dùng chung nguồn rule, không import công cụ của nhau và không sinh chỉ dẫn Codex từ Claude. README gốc chỉ bổ sung lối vào bộ Codex; CI có phần kiểm tra riêng cho từng bộ và kiểm tra khả năng cùng tồn tại.

Nguồn Codex gồm tám rule, mười sáu guide và bảy role. AGENTS, năm router project và sáu template kết nối các phần đó thành một bản sử dụng thực tế. [Bản đồ nghĩa vụ](../codex/workflow-obligations.md) chỉ rõ ba mươi trách nhiệm được giữ lại, từ đọc hướng dẫn trước hành động đến bằng chứng, xác minh, bài học, quyết định và đưa cải tiến về bundle của chính bộ Codex.

Các file được viết bằng câu đầy đủ. Bộ genome không đặt luật văn phong chung cho câu trả lời, tài liệu hay kịch bản. Những yêu cầu riêng của từng loại đầu ra tiếp tục thuộc project hoặc skill của đầu ra đó. Role phần mềm không tự áp vào công việc sáng tạo.

## Cài đặt và bảo trì

Skill [`init-codex-genome`](../../skills/init-codex-genome/SKILL.md) và CLI Python hỗ trợ `init`, `update`, `recover`, `check`, `promote`, `verify` và `health`. Project đích và root sản phẩm được chỉ định rõ; công cụ không lấy root Git cha làm đích mặc định.

Bộ cài quản lý một vùng trong `AGENTS.md`, các mục ignore và những file ghi trong manifest Codex. Nội dung ngoài vùng AGENTS được giữ nguyên. Bản cập nhật đối chiếu hash của nội dung đã triển khai; chỉnh sửa cục bộ hoặc file chưa rõ chủ sở hữu tạo conflict. Mọi lần apply gắn với hash của dry run đã xem xét. Khi có conflict, không ghi các thay đổi của kế hoạch và không nâng phiên bản hoàn tất. Nhật ký giao dịch hỗ trợ phục hồi khi việc ghi bị gián đoạn; dữ liệu phục hồi cũng được kiểm tra hash trước khi sử dụng.

Adoption bản Codex cũ cần hợp nhất có review và hash đúng trạng thái. File còn thuộc manifest Claude không được Codex nhận quyền sở hữu hay xóa. Bộ cài kiểm kê các tham chiếu renderer cũ và không báo migration hoàn tất khi còn khả năng sinh lại AGENTS. Lịch sử cũ giữ nguyên mặc định; việc nhập một số bản ghi là thao tác có chọn lọc, giữ nguồn gốc và ánh xạ ID.

Bản source author skill dưới `.agents/skills/`; bộ đóng gói chuyển nó vào `skills/` của plugin. Gói phân phối dùng manifest tương thích `.codex-plugin/plugin.json`, có README riêng với đường dẫn đúng cho người nhận. Bộ cài không thêm model, permission, trust, hook, MCP hoặc cấu hình toàn cục.

## Kiểm tra đã thực hiện

Các kết quả cấu trúc và công cụ được lưu trong [implementation-checks.json](codex/implementation-checks.json).

Các lượt review độc lập có hồ sơ riêng về [hướng dẫn](codex/guidance-review.md), [công cụ triển khai](codex/tooling-review.md) và [đóng gói](codex/packaging-review.md).

| Phạm vi | Kết quả quan sát |
|---|---|
| Codex trong repository | 38 ca: 37 đạt, một ca symlink thiếu quyền tạo trên Windows. Ca junction thực tế đạt. |
| Chỉ sao chép riêng `codex/` ra ngoài repository | 36 ca đạt; bỏ qua ca symlink và ca cùng tồn tại vì cố ý không có nguồn Claude. |
| Tính toàn vẹn hướng dẫn | 37 tài liệu live đạt kiểm tra; live và bundle không còn drift. |
| Cùng tồn tại | Cài hai bộ theo cả hai thứ tự và chạy hai updater đều giữ nguyên phần của bộ kia. |
| Bộ Claude | 18 ca triển khai đạt; sáu script kiểm thử portable không có lỗi; lint 39 file đạt và version mirror vẫn là 5.0.0. |
| Review độc lập | Bảy phát hiện về tooling, ba phát hiện về đóng gói và hai điểm không khớp giữa guide với bộ kiểm tra đã được sửa và kiểm tra lại. |
| Plugin | Gói thật được cài trong Codex home tạm; skill xuất hiện, thân skill chưa bị nạp sẵn; wrapper trong cache lập được kế hoạch cài mới. |

CI Windows và Linux đã được khai báo. Các kiểm tra trên được chạy tại máy Windows hiện tại; chưa có kết quả chạy workflow trên GitHub và chưa coi Linux là đã kiểm chứng tại máy này.

## Quan sát Codex thực thi

Baseline là `codex-cli 0.154.0-alpha.6.2`. [Chín kiểm tra cấu hình và nạp](codex/capability-results.json) đã đạt, gồm trust, ưu tiên config, fallback AGENTS và skill khi chạy từ thư mục con. Các phép thử dùng dữ liệu nhân tạo và chỉ lưu trường cần kiểm chứng, không lưu prompt riêng hay credential.

Ba lượt thử hành vi đầu tiên chạm giới hạn 240 giây. Probe khi đó không giữ sự kiện dở dang, nên không đủ dữ liệu kết luận nguyên nhân hoặc coi đó là lỗi tuân thủ genome. Một phép thử đọc file độc lập sau đó thành công. Những lượt sau giữ bằng chứng tốt hơn và được báo cáo riêng, không thay thế hay xóa kết quả ban đầu.

Ở [lượt viết đoạn kể](codex/behavior-conversation-2-results.json), agent đã đọc lesson router, role router và ba rule nền rồi trả lời bằng đoạn văn tiếng Việt. Không có role phần mềm nào bị ép vào công việc này. Đây là một mẫu quan sát, không phải bằng chứng rằng mọi đầu ra sau này đều đạt chất lượng văn chương.

Ở [lượt tạo AGENTS trong thư mục con](codex/behavior-artifact-2-results.json), agent khởi chạy từ root, đọc chuẩn AGENTS trước khi tạo `docs/sample/AGENTS.md`, đọc lại file và kiểm tra tham chiếu. File kết quả có đúng chỉ dẫn hư cấu được yêu cầu và repository thử không có commit. Một lệnh tìm tham chiếu trả mã 1; kết quả tạo file được xác nhận riêng bằng đọc file, không chỉ dựa vào lời báo hoàn tất của model.

Ở [lượt gọi skill khởi tạo](codex/behavior-skill-2-results.json), agent đọc skill từ bên ngoài project, kiểm tra dry run rồi apply đúng hash đã xem xét. Agent bổ sung thông tin project ngoài vùng managed, tạo router tài liệu và một role biên tập riêng cho project nhật ký hư cấu. Bộ xác minh sau đó đạt với 38 file; manifest và bundle cùng phiên bản 1.0.0. Không có yêu cầu xác nhận lại việc cài đặt đã được cấp quyền. Người kiểm tra cũng đọc lại các file kết quả và chạy verifier độc lập.

Ở [phiên mới sau khi khởi tạo](codex/behavior-followup-results.json), agent đọc các router và rule nền, sau đó đọc role `journal-editor` vừa tạo cùng phần giới thiệu project. Agent trả lời bằng một đoạn nhật ký tiếng Việt trong chat, đúng phạm vi yêu cầu. Phép thử này xác nhận việc tiếp tục nạp và định tuyến trong một phiên CLI mới của project đó.

Review cuối đã đọc toàn bộ nguồn hướng dẫn để đối chiếu trách nhiệm công việc và tìm các luật văn phong chung còn sót. Hai điểm cần sửa là cách khai báo metadata của lesson chưa đủ rõ và verifier đòi các mục §1–§5 trong role dù hướng dẫn chỉ yêu cầu §6 làm điểm định tuyến. Tài liệu metadata đã được bổ sung; verifier hiện chấp nhận role viết bằng văn xuôi với §6, có ca kiểm thử cho cả trường hợp hợp lệ và thiếu điểm định tuyến.

Ở [lượt xử lý phản hồi giả định](codex/behavior-records-results.json), agent được yêu cầu lưu một lesson và một decision từ tình huống kiểm thử. Agent đọc guide tương ứng, ghi rõ nguồn giả định, giữ yêu cầu biên tập trong phần giới thiệu project và lưu lý do bác bỏ phương án khác vào decision. Lần kiểm tra đầu phát hiện hai lỗi dữ liệu: dùng Markdown link thay khóa tên file trong lesson router và thiếu `scope` của decision. Agent tự sửa, đồng thời ghi thêm lesson riêng về chính lỗi bảo trì vừa xảy ra. Người kiểm tra đã đối chiếu các bản ghi với fixture và chạy lại verifier: 41 file đạt. Hai hợp đồng dữ liệu này cũng đã được giải thích rõ hơn trong guide để người tạo bản ghi không phải đọc mã parser mới biết.

## Giới hạn và trạng thái bàn giao

Hai phép thử agent tùy chỉnh không xác nhận được spawn, kể cả khi bật `agents.enabled=true` trong lần gọi thử. Vì vậy bộ lõi dùng role guide và khả năng phân công thực sự có sẵn; không phân phối agent TOML như một tính năng đã được chứng nhận.

Chưa kiểm chứng qua một phiên UI desktop mới, IDE, remote hoặc cloud. Giới hạn này được ghi trong [tài liệu tương thích](../codex/compatibility.md) và quyết định về nghiệm thu client. Kết quả CLI không được dùng để thay thế kết quả UI.

Phép thử lesson và decision có yêu cầu ghi nhận tường minh; nó không chứng minh model luôn tự nhận diện mọi tình huống cần ghi. Việc agent tự ghi thêm lỗi bảo trì là một quan sát riêng trong cùng lượt thử. Các kết quả trên không thay thế việc tiếp tục đánh giá khi dùng genome trong project thực tế.

Chưa commit, push, phát hành hoặc triển khai lên Hi Tuấn C. Thay đổi hiện nằm trong repository nguồn; gói phân phối có thể dựng lại bằng công cụ của riêng bộ Codex.
