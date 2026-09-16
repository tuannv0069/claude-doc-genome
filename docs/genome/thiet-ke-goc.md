---
scope: project
documentType: Design Extraction
status: Historical baseline
source: skills/init-project
sourceVersion: 4.0.0
extractedAt: 2026-09-15
---

# Thiết kế gốc của genome

## §1 Nguồn và phạm vi bản trích xuất

Tài liệu này mô tả repository chính thức `D:/Code/claude-doc-genome` ở commit `13fc9fa26e9e7d54e0cc58c818d196d5b284cd52`, trước lần viết lại. Bundle phiên bản 4.0.0 có 61 file. Bản triển khai trong Hi Tuấn C có 59 file và một số nội dung vai trò khác, nên không dùng bản đó thay cho nguồn chính thức.

Đây là hồ sơ thiết kế lịch sử. Tên file đã bị loại vẫn được ghi để giải thích đầu vào của lần thay đổi; chúng không phải con trỏ yêu cầu AI đọc file đang tồn tại. Có thể đọc đúng nội dung gốc bằng `git show 13fc9fa26e9e7d54e0cc58c818d196d5b284cd52:<đường-dẫn>`. [Kế hoạch viết lại](ke-hoach-viet-lai.md) sở hữu phạm vi triển khai mới.

## §2 Kiến trúc và trách nhiệm

Genome có một phần dùng chung được sao chép nguyên bản và một phần được tạo riêng cho mỗi project. Phần dùng chung gồm rule, guide, vai trò và công cụ. Phần riêng gồm file chỉ dẫn gốc, các router, thông số project và những module chỉ được thêm khi có nhu cầu thực tế.

File chỉ dẫn gốc cung cấp thông tin project và điều kiện đọc các hướng dẫn. Rule luôn nạp giữ các trách nhiệm cần biết trước khi hành động. Rule có `paths:` chỉ phục vụ nhóm file liên quan. Guide chứa quy trình được đọc theo task. Router và liên kết bằng `§ID` nối chúng với nhau; mỗi yêu cầu có một nguồn chuẩn để giảm sai lệch giữa các bản sao.

`.agent-workspace/guide/` chứa cách làm việc, còn `docs/` chứa sản phẩm của project. Bài học ghi các phương pháp đã thất bại; nhật ký quyết định ghi lý do mà diff không thể phục dựng. Wiki giữ nhận định đã có bằng chứng về tài liệu đối tượng. Task workspace giữ trạng thái tạm của công việc đang chạy.

## §3 Nguồn live và bundle

Repo tự sử dụng genome của nó. Rule được chỉnh ở `.claude/rules/`; guide và vai trò ở `.agent-workspace/guide/`; công cụ ở `.agent-workspace/tooling/`. `check` đối chiếu chúng với bundle; `promote` chép cải tiến từ live về bundle. Template và `skills/init-project/SKILL.md` được chỉnh trực tiếp. Chủ sở hữu phiên bản là `skills/init-project/VERSION`.

Bản gốc còn có bề mặt Codex, tiêu chuẩn riêng và renderer để sinh file từ nguồn. Nó cũng phân phối skill `document-writer` với hai file. Người dùng đã quyết định loại cả hai phần này; không bảo toàn chúng trong thiết kế mới. Việc giữ thông tin lịch sử ở tài liệu này không có nghĩa chúng vẫn được hỗ trợ.

## §4 Quy trình làm việc của AI

Trước khi làm task, agent tra router bài học và vai trò. Một vai trò chính dẫn dắt công việc; phần điều kiện hoàn thành của vai trò kiểm tra bổ sung góc nhìn. Router gốc có các vai trò nghiệp vụ, kỹ thuật, thực thi, kiểm thử, quản lý, bảo mật và chuyển ngữ, với khả năng thêm vai trò project.

Các guide quản lý việc lập kế hoạch, phân công, review, truy nguyên lỗi, phân tích ảnh hưởng, tạo gate kiểm chứng và quản lý worktree. Thiết kế yêu cầu tác giả xác định cách kiểm tra trước khi thực hiện, đọc cả hai phía của quan hệ phụ thuộc và kiểm chứng dựa trên bằng chứng thay vì chỉ khẳng định đã đúng.

Bài học đi từ bản ghi sự cố đến hướng dẫn ổn định khi có đủ bằng chứng. Quyết định có quan hệ thay thế để ghi được lý do đổi hướng mà không sửa lịch sử. Wiki phân biệt nhận định chưa xác minh, đã có nguồn và bị bác bỏ; dữ liệu bằng chứng có schema để công cụ kiểm tra.

## §5 Khởi tạo và bảo trì

`init` quét project, xác định module và thông số, sao chép portable, điền template, thêm hướng dẫn project cần thiết, ghi manifest rồi kiểm tra. File riêng đã tồn tại phải được hợp nhất, không bị ghi đè. Runtime, kiểm thử trình duyệt và wiki là các module theo nhu cầu; genome không cài chúng vì phỏng đoán.

Bốn script Node có thật trong repo gốc: `update.mjs`, `init-manifest.mjs`, `sync-version.mjs` và `doc-lint.mjs`. Bản trích xuất từ Hi Tuấn C trước đây không tìm thấy chúng vì đó là bản triển khai, không phải checkout nguồn chính thức.

Updater gốc so ba giá trị: hash bundle mới, nội dung live và hash lần triển khai trong manifest. File thiếu được thêm; file chưa sửa cục bộ được cập nhật; sửa đổi cục bộ trở thành conflict. Công cụ không xóa file đã nghỉ dùng, không sửa router và chỉ cảnh báo template đổi. Nó còn ghi phiên bản mới khi vẫn có conflict, nên chỉ nhìn `manifest.version` chưa chứng minh đã cập nhật hoàn tất.

Map gốc của updater và manifest thiếu roles và tooling. Danh mục template của chúng thiếu roles, decisions và wiki. Đây là khoảng trống triển khai đã xác nhận từ mã nguồn; bản viết lại phải giải quyết nếu muốn dùng công cụ cho toàn bộ bundle.

## §6 Các hợp đồng công cụ

Các gate Python kiểm tra router bài học, vai trò, nhật ký quyết định, wiki và các loại trigger. Scanner tìm dấu hiệu trùng lặp, liên kết hỏng, sai lệch portable và sự tích lũy rule. Một số gate đọc tên cột, marker, `§ID` hoặc khóa dữ liệu; đây là các hợp đồng cần xét cùng thay đổi tài liệu.

`doc-lint.mjs` gốc kiểm tra metadata, slot chưa điền, đường dẫn, router và tham chiếu mục. Nó còn áp trần số dòng cho `CLAUDE.md` và ngân sách rule luôn nạp. Hook chạy kiểm tra phiên bản, doc lint và trước đây có renderer Codex; CI gốc chỉ kiểm tra phiên bản. Không đánh đồng các gate có sẵn với những kiểm tra CI thực sự chạy.

## §7 Nguồn của quy định nén và văn phong

`rule-writing-standards.md` ưu tiên tiết kiệm token, dùng rule một dòng và giới hạn 15 từ. Các tiêu chuẩn CLAUDE, skill và subagent lặp lại yêu cầu bỏ qua khả năng đọc hiểu của con người. Nén chữ vì vậy là lựa chọn xuyên suốt hệ thống, không chỉ ở một file.

`conversational-output.md` quy định cách mở đầu, chia đoạn, dùng heading, bảng và kết thúc hội thoại. Guide bài học, quyết định, báo cáo lỗi và vai trò còn có giới hạn độ dài hoặc khuôn trình bày riêng. `document-writer` áp thêm chính sách lên tài liệu. Một phần kiểm thử và scanner phụ thuộc vào hình thức này.

Nguồn xác nhận các ràng buộc đang tồn tại. Phản hồi của người dùng xác nhận đầu ra khó đọc đã lặp lại trong nhiều project. Chưa có thử nghiệm đối chứng tách riêng mức ảnh hưởng của từng file; không coi quan hệ nhân quả định lượng là điều đã đo được.

## §8 Ý nghĩa cần giữ và thay đổi đã chọn

Giá trị cần giữ là quản lý tri thức, nguồn chuẩn, điều kiện đọc, bằng chứng và khả năng đưa cải tiến trở lại bundle. Cách diễn đạt cũ không phải một phần bắt buộc của thiết kế. Bản mới chỉ dành cho Claude Code và chỉ sở hữu quy trình làm việc; chính sách văn phong của từng sản phẩm thuộc project sử dụng.

Human readability là tiêu chí của công việc viết lại, không được đưa thành một bộ rule chung mới. Các file lịch sử như tài liệu này lưu đối chiếu; bundle đang phân phối phải chỉ nói về quy định hiện hành.

## §9 Phạm vi ngoài bundle

Lần viết lại còn phải xét `CLAUDE.md`, router live, `README.md`, `CONTRIBUTING.md`, metadata plugin, hook, CI và các script cấp repo. Chúng không nằm trong số 61 file dưới đây, nhưng tham gia hướng dẫn hoặc triển khai nên không thể bị bỏ qua.

## §10 Danh mục nguồn ban đầu

Mỗi đường dẫn bên dưới tương đối với `skills/init-project/` ở commit đã chốt. Hash ghi lại nội dung trước khi sửa, dùng để đối chiếu phạm vi và tránh bỏ sót. File chương trình cần rà soát hợp đồng và chuỗi hướng dẫn, không viết lại thuật toán chỉ để đổi câu chữ.

| File | SHA-256 ban đầu |
|---|---|
| `AUTHORS.md` | `36f86c45cb174b6c1bcbef2cbf7b9a1db5f77b6054811a9cd6ee34e571959684` |
| `portable/codex-rules/agents-md-standards.md` | `fb31b959133d796b4777ffa9e9b5e5fdb8e60ad910ef86db53168ddbe5df441b` |
| `portable/codex-rules/codex-agents-standards.md` | `7415622f8a30cf4d7bceb6c7b1f54220457925136bd4f87b9ad1fe2c05501b8e` |
| `portable/guide/bug-report-format.md` | `37b03f9ee0564f1112b32b3a24256df178c0d30daf29ff3363819a1ae49113e1` |
| `portable/guide/capability-packaging.md` | `74ba3b6675d8f499779039071d19bfb3be158e7d6deae2392ac71681ae2798ca` |
| `portable/guide/decision-journal.md` | `b37ea45078d8653890b3e6ab06c6e4b73335e594d64980f97acd2b3012f012b0` |
| `portable/guide/doc-system-mechanics.md` | `ed27f54b1c133873ecd286631bc5342efb7182a5d7ecfbe427bee921ce0363c2` |
| `portable/guide/five-why.md` | `1ebc6c35dbdbd4dc17744437df6351ce141913a64c903b97ac66edebe9e0446d` |
| `portable/guide/fix-impact-analysis.md` | `11d7ae1e3d409bf8d068af5af458e1a28c5765ef791243cda03e9647cc90f59b` |
| `portable/guide/harness-adapter.md` | `978c47d64e636be940642bedebdf86e6b6ab17289af17da1363d738e1d08784a` |
| `portable/guide/lesson-capture.md` | `0e318bc394c55efc41a4aa65e61f38d16bdad2ded500d4088183f7cea07a1be6` |
| `portable/guide/markdown.md` | `865c9c43b6d734b82e3d18e1b7631395f787261052d1a49bec9c4afd20b5db3c` |
| `portable/guide/mermaid.md` | `f8af731ed97e08a442dda65df9bc4fcb28cdd9d6f608d8043f5e618a0b09f723` |
| `portable/guide/orchestration-policy.md` | `0d61b3ded203cfc92a247e7ef90e21bb85d91d967bf75933817f4a53dca13356` |
| `portable/guide/review-checklist-method.md` | `c4e1e08425ff35dcbf55d2e4b59371cfe0564cb7d9c0e87f3477c33b73e49d14` |
| `portable/guide/role-selection.md` | `fee5f85c3eae95adeea722eeb9f2f15c43ae50a81d41237713ea076bd5162511` |
| `portable/guide/rule-health.md` | `babf08a1e1a93519feee8ac75822cb27ba948ff22fae38e59c05b3af6dcf7fcd` |
| `portable/guide/task-planning.md` | `194ca9a02f45b9fcd3ea0946d5e9d0b1be6189c3282a6c03f347d3efde19ac1b` |
| `portable/guide/verification-gate-design.md` | `c9bc2a15e61a7a744cccc26f7ae294b2a959df6a3c64133516bfee110fed7fe6` |
| `portable/guide/worktree.md` | `635ad2b0a4c91067bfc67bb297cf858dd651eaf752d9f5c9bcb4317293e5d14e` |
| `portable/roles/business-analyst.md` | `2cd2e3c8f05002b8bc711545d5bea4f049f7c7fd08da29e73cf971f71b39c64b` |
| `portable/roles/comtor.md` | `621d3bf7927f0f0c7262679e255dea30cd7604b4fd448d910144b57c9785efc2` |
| `portable/roles/developer.md` | `dfffc9fac4a4ce729b90059ce097839defec4e063e60c7d8712ba9e534356c43` |
| `portable/roles/project-manager.md` | `fe8c86ca28b1132603181f4a0db12ebc73ecfff38f21fc437dfe5586936f570c` |
| `portable/roles/qa.md` | `d03e1ea32dc61c879b957405f7dc1c33873667cb36cd8c638e5dbccff3e1eccb` |
| `portable/roles/security.md` | `c39ac0015e0b068c1cc4fe8bb247e4b51a5a1ac1aa434a3f0eb6a0d70df70079` |
| `portable/roles/tech-lead.md` | `6e27d9f0aa1434034efd4ba048c5a20348cd398ea8c41f67a1be272267f526ad` |
| `portable/rules/claude-md-standards.md` | `999758f6f48bd0304cc9375e266dc935188ace9bba886a161f19a80e902a7b9f` |
| `portable/rules/conversational-output.md` | `1755274d09e848c35470a70dc4669635a119adc0fd34b31ad2fddf679d72c6de` |
| `portable/rules/critical-thinking.md` | `7e89c74d20ff6392e4302e55d1b9d7ac997a23d81d7aec910b6ae9b1fea71472` |
| `portable/rules/doc-organization.md` | `0d6767c6934f6e7116c050c5fae6cd690e548a8e988d4aa7dee0714e6bb1428e` |
| `portable/rules/file-reading.md` | `f51a32fb014a76d6b4e5d4e2b4c725c5acb4898026a971628d45cd9b0731b843` |
| `portable/rules/rule-writing-standards.md` | `8c8ca9d8bba909a40df437d9059f7f8c7dc8d91c3c27975c2b59d0b7aa800b28` |
| `portable/rules/skill-md-standards.md` | `f2917dea9edca6012be54cf3af0eb92657f3ea57fb1b70023d6b8f6996c0d6e3` |
| `portable/rules/subagent-standards.md` | `a2c6e7b98d960f53ded6148ee7cf8443c038a4aaf51ff603ef41f52ce0eb82d8` |
| `portable/rules/wiki-tier.md` | `222d820e3a896af253ad9c2798ab4ad9fa9ecc1e0c15bca54034f476030e1ab2` |
| `portable/skills/document-writer/README.md` | `c94b38d659a64d4f06077ef40fd53cfb1beb7901f32b397527117f34e110c3a9` |
| `portable/skills/document-writer/SKILL.md` | `38bd23b5d98477cc85484f26f7591190ef4a8bf3680df90c1449149f66433354` |
| `portable/tooling/archive_decisions.py` | `c86b2a2696ec4eb8a5d15fe391dbd729488ba73083643033dccf9bca5d706d6a` |
| `portable/tooling/render_codex.py` | `e878faea9b12806cd3411948ab28a8c57ae0beb45b6f8d7aba9766033f667486` |
| `portable/tooling/scan_rule_health.py` | `6fd427dda5ffb38199b4b2420c4b13880fbc58f9f906fd2bbbd02775926d7ae0` |
| `portable/tooling/test_render_codex.py` | `705a61f98d276af4a04ddf484d049c77bb0edc7bd250b62ef727cd943fb4ea80` |
| `portable/tooling/test_scan_rule_health.py` | `852a8d494d94576315181068f5980a1a95356c2abf7a8f0bcefc3e1e9b06d10b` |
| `portable/tooling/test_trigger_kinds.py` | `da32394efea58bdeb4ce5107244f80e1be5125f74940a5a44061503c1a5f0856` |
| `portable/tooling/test_verify_decision_log.py` | `ff6936deb4a331e1c9b04c94d6f86caca44a9c175836b54d4e024065e78c4249` |
| `portable/tooling/test_verify_lesson_router.py` | `8967533b0b5e4fe6e32c41cae4c42b16ee727700432eed84de65a6e998e03f19` |
| `portable/tooling/test_verify_role_files.py` | `0a638b4ee0032705b193d2e3eb5229a72a610bba21ec5db7b4244c4c7e2e05e6` |
| `portable/tooling/test_verify_wiki.py` | `d975e95377e9a48127fb8818e6b573a58f1537eb9a013301782f64e497cd9976` |
| `portable/tooling/verify_decision_log.py` | `7cdc190341e2508c8d688f480935ffa1bd1283cf44c26013592797aed7869990` |
| `portable/tooling/verify_lesson_router.py` | `542a7e886686adceb8354aae74f7c757f66b79a298c4e54edad91703ee218384` |
| `portable/tooling/verify_role_files.py` | `08b035465ec6c266664873cbb7168c7822d2ffa7aee34ad870569cf8ecd3cbfb` |
| `portable/tooling/verify_wiki.py` | `4c5f127917807e1c2dc2c901dc34eea09e0acfc3ccf5b4173391927ed88d0782` |
| `SKILL.md` | `580d753748050baee08ec0d6722194edc2069f023dc085c63c56beed6ef6f6ae` |
| `templates/CLAUDE.md.tpl` | `2d04c07c94e50a8ba071f247fea5bac8e69dd15132333896c4f32441d90e2f65` |
| `templates/decisions/index.md.tpl` | `ab06c2f4c560db13b19c731b924b72e74936a0fb95941f40a55669f851044c2d` |
| `templates/docs/index.md.tpl` | `f7885576f44e8dc7f2787d4652ba6364745f0b9340cf9c44fcb573b5329ca9bb` |
| `templates/guide/index.md.tpl` | `4a7d3bc97f01f9838050b2327d8f587b8c436a1bb6960e0e8d7b716392a66ac9` |
| `templates/lessons/index.md.tpl` | `36721f0725f9c26b8430c5efac4ec5d38a972830253d24f6776d8f0170e45ca2` |
| `templates/roles/index.md.tpl` | `8dd908b8298e261fd5b22015c483e84e4e550ec1394c3bec1255f57c6188b979` |
| `templates/wiki/index.md.tpl` | `5f7e0cb2915576f97e2912c078dc571c56d76935d832f8e82f311b3bc0b0c490` |
| `VERSION` | `e1d49c569ae09b2ede16e2d83820a3809b35eb6c44c13ba9b5330598d6b8f43c` |
