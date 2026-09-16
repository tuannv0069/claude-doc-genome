---
scope: project
documentType: Research
status: Completed with stated verification limits
researchedAt: 2026-09-16
sourceCommit: 156a886
---

# Cơ chế cấu hình Codex và cách nối với genome

## §1 Phạm vi và mức độ bằng chứng

Tài liệu phục vụ việc bổ sung Codex vào genome đã viết lại. Bản nghiên cứu phân biệt điều tài liệu OpenAI mô tả, điều đã quan sát ở máy hiện tại và phần còn cần thử khi triển khai. [Kế hoạch triển khai](ke-hoach-ho-tro-codex.md) dùng các kết quả này. Những phép thử và sản phẩm được thực hiện sau giai đoạn nghiên cứu nằm trong [báo cáo triển khai](ket-qua-trien-khai-codex.md); các giới hạn dưới đây mô tả bằng chứng tại giai đoạn nghiên cứu.

Máy hiện tại có `codex-cli 0.154.0-alpha.6.2`. Đã đọc trợ giúp CLI, các trang chính thức và chạy `codex debug prompt-input` trên một Git repository tạm. Phép thử chỉ tìm các dấu hiệu nhân tạo trong đầu vào được dựng; không gọi model để thực hiện nhiệm vụ, không in chỉ dẫn riêng của nhà cung cấp hoặc người dùng, không đổi cấu hình cá nhân. Nó dùng cấu hình người dùng hiện có, nên không phải môi trường hoàn toàn cách ly. [Kết quả cục bộ](codex/local-loading-results.json) ghi rõ các trường hợp.

Các URL Codex cũ trên `developers.openai.com` chuyển hướng đến `learn.chatgpt.com`. Hai URL dẫn đến cùng trang không được tính thành hai nguồn độc lập. Các hành vi của bản CLI alpha này cũng chưa đại diện cho mọi bản Codex hoặc mọi giao diện desktop.

## §2 Chỉ dẫn bằng AGENTS.md

Theo [tài liệu AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md), Codex dựng chuỗi chỉ dẫn từ cấp người dùng và từ gốc project xuống thư mục làm việc. Tại mỗi cấp, `AGENTS.override.md` được ưu tiên trước `AGENTS.md`, rồi mới đến tên dự phòng được cấu hình. File con bổ sung hoặc ghi đè chỉ dẫn trước đó trong chuỗi; không thay toàn bộ chuỗi cha. Việc nạp gắn với lúc bắt đầu phiên.

Thử nghiệm cục bộ cho thấy: chạy ở gốc chỉ có dấu hiệu của root; chạy ở thư mục con có cả root và child; thêm override thì dấu hiệu của child thường biến mất, còn root và override vẫn có. `CLAUDE.md` và file Markdown đặt trong `.codex/rules` không tự xuất hiện trong đầu vào của fixture.

Hệ quả thiết kế: hướng dẫn cần trước khi hành động phải có đường vào qua `AGENTS.md`. Một đường dẫn được viết trong file không đồng nghĩa với nội dung đích đã được nạp. Các quy trình dài vẫn cần lệnh đọc rõ điều kiện và đối tượng. Việc bắt đầu ở root rồi sửa một file sâu trong cây không được mặc định tương đương với khởi chạy Codex tại thư mục chứa file đó; cần có ca kiểm tra riêng.

## §3 Giới hạn đầu vào là giới hạn kỹ thuật

Trang AGENTS.md mô tả giới hạn mặc định 32 KiB cho chuỗi tài liệu; [Advanced Configuration](https://learn.chatgpt.com/docs/config-file/config-advanced#project-instructions-discovery) lại diễn đạt `project_doc_max_bytes` theo từng file. Đây là điểm tài liệu chưa thống nhất.

Trong fixture, đặt ngân sách 12 byte làm dấu hiệu root không còn đầy đủ. Đặt 50 byte với root và override, mỗi file riêng đều ngắn hơn 50 byte, giữ được dấu hiệu root nhưng mất dấu hiệu override. Kết quả phù hợp với việc giới hạn tổng chuỗi trên bản cài hiện tại. Không suy ra từ phép thử này cách mọi client xử lý toàn bộ nguồn chỉ dẫn.

Genome cần phát hiện phần chỉ dẫn bị thiếu hoặc cắt. Cách xử lý là phân tầng nội dung và kiểm tra đầu vào thực tế; không tái tạo luật ép câu ngắn hay nén chữ. Cũng không tự tăng giới hạn trong cấu hình cá nhân để che một thiết kế nạp quá nhiều.

## §4 Cấu hình chạy và mức độ tin cậy

[Config Basics](https://learn.chatgpt.com/docs/config-file/config-basic) mô tả thứ tự ưu tiên: tham số CLI, cấu hình project gần thư mục làm việc, profile được chọn, cấu hình người dùng, mặc định được quản lý, cấu hình hệ thống và mặc định chương trình. Cấu hình project `.codex/config.toml` chỉ có hiệu lực khi project được tin cậy. Chính sách tổ chức có thể đặt thêm ràng buộc bắt buộc.

CLI hiện tại xác nhận có `--config`, `--profile` với file `<name>.config.toml`, `--strict-config`, lựa chọn sandbox và approval. Chưa thử đầy đủ ma trận ưu tiên hoặc project trusted/untrusted. Cần kiểm tra đó trước khi bộ cài ghi bất kỳ khóa cấu hình nào.

Đề xuất cho genome: chỉ tạo cấu hình project khi một khả năng đã chọn thực sự cần nó. Không đặt model, mức suy luận, quyền mạng, sandbox hoặc approval chung cho mọi project. Không thay đổi cấu hình toàn cục hay tự cấp trust. `model_instructions_file` thay chỉ dẫn tích hợp theo [Configuration Reference](https://learn.chatgpt.com/docs/config-file/config-reference); nó không phải nơi thích hợp để chèn thêm genome.

## §5 Skill: khả năng được chọn theo công việc

[Build skills](https://learn.chatgpt.com/docs/build-skills) mô tả `SKILL.md` với `name`, `description` và nội dung quy trình. Codex công bố danh mục trước, rồi đọc nội dung khi chọn skill. `.agents/skills` là đường dẫn project được tài liệu hiện tại hướng dẫn; `agents/openai.yaml` cung cấp metadata bổ sung, không phải định nghĩa subagent TOML.

Fixture có hai skill tên khác nhau, một trong `.agents/skills`, một trong `.codex/skills`. Bản CLI hiện tại phát hiện cả hai tên, nhưng không đưa dấu hiệu nằm trong thân skill vào đầu vào ban đầu. Điều này xác nhận đường dẫn project `.agents/skills` đang hoạt động và nhánh `.codex/skills` vẫn được nhận ở bản đã thử. Không nên dùng việc thư mục người dùng chưa tồn tại để kết luận một đường dẫn không được hỗ trợ.

Kế hoạch chọn `.agents/skills` cho bản cài mới; đường cũ chỉ là tình huống tương thích cần phát hiện. Cần tránh cài hai bản cùng tên. Việc skill xuất hiện trong danh mục chưa chứng minh nó được kích hoạt đúng, nên còn cần thử lời yêu cầu tự nhiên và cách gọi tường minh trong phiên thực thi.

## §6 Vai trò trong genome và subagent của Codex

[Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) mô tả agent tùy chỉnh bằng TOML tại `.codex/agents/` hoặc thư mục agent cá nhân. Các trường bắt buộc hiện tại là `name`, `description`, `developer_instructions`. Cấu hình model và quyền có quy tắc kế thừa riêng; không nên sao chép schema hay frontmatter của agent Claude sang nguyên trạng.

Vai trò genome là góc nhìn và tiêu chí kiểm tra, có thể được một agent chính sử dụng. Nó không đồng nghĩa với việc phải mở một tác nhân mới. Chỉ tạo subagent khi công việc cần phân công hoặc kiểm tra độc lập; phần hướng dẫn của agent dẫn tới vai trò và quy trình có nguồn chuẩn. Giữ khác biệt về mức thẩm quyền: một chỉ dẫn đặt trong `developer_instructions` không được vô tình nâng toàn bộ chính sách project lên cấp cao hơn.

Đã đặt một agent TOML nhân tạo trong fixture, nhưng phép dựng danh sách thông điệp không hiển thị nó. Kết quả đó không đủ kết luận agent được hoặc không được đăng ký, vì định nghĩa công cụ không được kiểm chứng trong phép thử này. Việc nhận schema, xuất hiện trong danh mục, spawn, nhận context và kế thừa quyền còn phải thử riêng.

## §7 Rules, hooks và MCP có trách nhiệm khác nhau

[Rules](https://learn.chatgpt.com/docs/agent-configuration/rules) của Codex là chính sách thực thi lệnh, dùng file `.rules` và điều kiện như `prefix_rule`. Nó không phải lớp Markdown quy định phương pháp làm việc. Đây cũng là lý do không dùng `.codex/rules/*.md` làm nơi kỳ vọng Codex tự nạp luật genome. Chính sách lệnh chỉ được tạo khi project có nhu cầu cụ thể và có ca kiểm tra khớp/không khớp.

[Hooks](https://learn.chatgpt.com/docs/hooks) hỗ trợ các sự kiện vòng đời, có thể nhận cấu hình từ `hooks.json`, TOML hoặc plugin. Các hook phù hợp có thể cùng chạy; trust được gắn với định nghĩa hook. Hook project chưa trusted không nên được coi là đang bảo vệ workflow. Genome cốt lõi cần chạy được khi hook chưa bật; nếu thêm hook cho kiểm tra máy móc, phải có đường kiểm tra trực tiếp tương đương. Chưa chạy hook trong nghiên cứu này.

[MCP](https://learn.chatgpt.com/docs/extend/mcp) cung cấp công cụ và nguồn dữ liệu qua STDIO hoặc HTTP. Cấu hình thuộc `config.toml`; các client local trên cùng host có thể dùng chung cấu hình đó. Genome không cần một MCP server chỉ để đọc các guide đã có trên đĩa. Tích hợp bên ngoài, credential và quyền truy cập vẫn thuộc project/người dùng. Chưa thêm hoặc kết nối MCP mới.

## §8 Đóng gói và các giao diện sử dụng

[Build plugins](https://learn.chatgpt.com/docs/build-plugins) phân biệt workflow trong skill với gói phân phối. [Package your plugin](https://developers.openai.com/plugins/build/plugins) hiện mô tả root `plugin.json` và phần mở rộng OpenAI; `.codex-plugin/plugin.json` vẫn là định dạng tương thích được hỗ trợ. CLI cài hiện tại có nhóm lệnh quản lý plugin, nhưng chưa cài thử gói genome bằng một định dạng nào trong nghiên cứu này.

Khuyến nghị triển khai core qua project trước, rồi thử gói phân phối Codex riêng. Có thể bắt đầu với manifest tương thích của Codex sau khi xác minh loader trên bản được hỗ trợ; không thay manifest Claude hoặc coi manifest Claude là manifest Codex. Cài plugin phân phối skill cũng không tự làm genome trở thành chỉ dẫn bắt buộc trong mọi project.

Desktop, CLI và IDE cần được nghiệm thu theo phạm vi riêng. Phép dựng prompt CLI giúp kiểm tra lớp nạp; phiên desktop mới vẫn cần thử chọn project, CWD, worktree và skill. Không dùng kết quả CLI để tuyên bố đã kiểm tra UI desktop, môi trường remote hoặc cloud.

## §9 Kết luận cho thiết kế

Có đủ cơ sở để thiết kế bộ Codex theo các cửa vào riêng của nền tảng. Người dùng chọn hai bộ genome độc lập và chấp nhận cập nhật hai nơi. Vì vậy kế hoạch không dùng chung nguồn rule hoặc sinh Codex từ Claude. Chưa có cơ sở để chỉ đổi tên thư mục Claude thành Codex, khôi phục toàn bộ renderer cũ, hoặc mặc định mọi tính năng hiện hành đều có trên client khác.

Những điều phải kiểm tra thêm trước khi phát hành gồm: ma trận trust/config, agent tùy chỉnh, plugin loader, thực thi skill, chỉ dẫn ở thư mục con khi đổi đối tượng làm việc, và hành vi trong phiên desktop mới. Các mục này được đặt thành điều kiện nghiệm thu trong kế hoạch, không được ghi là đã đạt từ những thử nghiệm chỉ dựng đầu vào.
