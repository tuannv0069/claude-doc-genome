---
scope: project
documentType: Implementation Plan
status: Implemented with client verification limits
plannedAt: 2026-09-16
baselineCommit: 156a886
---

# Kế hoạch hỗ trợ Claude Code và Codex trên cùng một project genome

## §1 Mô hình cần đạt

Mỗi project chỉ có một genome đang hoạt động tại `.agent-workspace/`. Claude Code và Codex cùng đọc và cập nhật các guide, role, lesson, decision, wiki và dữ liệu task trong không gian này. Nhờ đó, một bài học được ghi khi làm việc bằng Claude Code vẫn có tác dụng khi chuyển sang Codex, và ngược lại.

Hai harness có bề mặt cấu hình riêng. Claude Code dùng `CLAUDE.md`, `.claude/` và manifest của Claude. Codex dùng `AGENTS.md`, `.codex/`, skill Codex và manifest của Codex. Các bề mặt này chỉ có nhiệm vụ kết nối agent vào genome chung và xử lý những khả năng đặc thù của harness.

Nguồn phân phối của hai harness được duy trì độc lập. `skills/init-project/` sở hữu bộ cài Claude Code; `skills/init-codex-genome/` sở hữu bộ cài Codex. Một cải tiến chung được biên soạn và kiểm tra ở cả hai nơi. Không có generator hoặc nguồn rule trung gian buộc hai bộ phải giống từng byte.

## §2 Bố cục trong project đích

| Trách nhiệm | Đường dẫn |
|---|---|
| Genome chung | `.agent-workspace/` |
| Guide và role | `.agent-workspace/guide/` |
| Lesson, decision và wiki | `.agent-workspace/lessons/`, `.agent-workspace/decisions/`, `.agent-workspace/wiki/` |
| Dữ liệu task và worktree | `.agent-workspace/tasks/`, `.agent-workspace/worktrees/` |
| Chỉ dẫn Claude Code | `CLAUDE.md`, `.claude/` |
| Chỉ dẫn Codex | `AGENTS.md`, `.agent-workspace/rules/`, `.codex/` |
| Công cụ cục bộ | `.agent-workspace/tooling/`; mỗi công cụ có tên riêng và manifest chỉ nhận ownership file của mình |
| Manifest Claude Code | `.claude/init-manifest.json` |
| Manifest Codex | `.codex/genome-manifest.json` |

Không tạo namespace con theo tên agent bên trong `.agent-workspace/`. Việc chia dữ liệu thành vùng Claude và Codex sẽ làm mất chính mục tiêu buộc hai agent làm việc theo cùng cơ chế và cùng lịch sử project.

## §3 Hành vi của bộ cài Codex

`init-codex-genome` phải hoạt động trong hai trường hợp:

1. Project chưa có genome: skill tạo các guide, role và router ban đầu trong `.agent-workspace/`, sau đó cài vùng được quản lý trong `AGENTS.md`, các chuẩn Codex và công cụ triển khai.
2. Project đã có genome hoàn chỉnh: skill giữ nguyên guide và các kho dữ liệu đang có, rồi chỉ cài adapter Codex. Manifest ghi `shared_workspace: reused` và không nhận ownership các file chung.

Nếu `.agent-workspace/` chỉ có một phần của genome, bộ cài dừng và báo các thành phần còn thiếu. Nó không ghép âm thầm hai phiên bản hướng dẫn khác nhau. Khi cập nhật, manifest quyết định file nào thuộc Codex; dữ liệu chung được tái sử dụng phải được giữ nguyên.

Manifest, lock và journal của bộ cài Codex nằm dưới `.codex/`. Đây là trạng thái của adapter, không phải tri thức hay dữ liệu làm việc chung của genome.

Bộ cài Claude Code áp dụng quy tắc đối xứng. Khi Codex đã bootstrap một genome hoàn chỉnh, Claude bỏ qua các file chung, cài bề mặt `.claude/` và ghi `sharedWorkspace: reused` trong manifest của mình. Hai updater chỉ quản lý các file đã được manifest tương ứng nhận ownership.

## §4 Nguồn Codex

Toàn bộ nguồn Codex nằm trong `skills/init-codex-genome/`:

- `bundle/portable/` chứa bản Codex có thể bootstrap một project mới.
- `bundle/templates/` chứa vùng AGENTS và các router khởi tạo.
- `bundle/bundle-map.json` ghi đích triển khai và hash.
- `scripts/genome.py` là wrapper chạy công cụ trong bundle.
- `SKILL.md` và `references/` mô tả quy trình cài, cập nhật và adoption.

Các kiểm thử, công cụ đóng gói và tài liệu phát triển nằm lần lượt trong `tests/codex/`, `scripts/codex/` và `docs/codex/`. Repository không giữ thêm một cây genome Codex ở root.

## §5 Quyền sở hữu và an toàn cập nhật

`AGENTS.md` chỉ được quản lý trong vùng marker của Codex. Nội dung project nằm ngoài vùng này được giữ nguyên. Bộ cài không thay model, trust, sandbox, approval, hook hoặc MCP của người dùng.

Mỗi lần ghi phải bắt đầu bằng dry run và chỉ apply khi hash của plan vẫn đúng. File đã sửa cục bộ, đường dẫn không an toàn, symlink, hard link hoặc ownership không rõ phải tạo conflict trước khi ghi. Journal hỗ trợ phục hồi khi cập nhật bị gián đoạn.

Các guide và record đã được một bộ cài khác tạo trong genome chung được dùng tại chỗ. Adapter Codex không sao chép chúng sang vùng riêng, không nhập lại lịch sử và không ghi chúng vào manifest Codex như file do Codex sở hữu.

## §6 Kiểm chứng

Các kiểm tra bắt buộc gồm:

- Skill Codex được copy độc lập vẫn bootstrap được project mới, chạy update và verify.
- Project đã được một trong hai harness khởi tạo có thể thêm harness còn lại mà toàn bộ guide, lesson, decision và wiki giữ nguyên byte.
- Cập nhật Claude không đổi adapter Codex; cập nhật Codex không đổi workspace chung mà nó đang tái sử dụng.
- `CLAUDE.md` và `AGENTS.md` cùng trỏ tới `.agent-workspace/`.
- Bundle map, package, version, link và instruction network đều vượt qua kiểm tra tương ứng.
- Không có luật văn phong chung về độ dài câu, heading, bảng, giọng viết hoặc cách diễn đạt trong genome.

Kiểm tra cấu trúc và CLI không thay cho xác minh hành vi trên mọi client. Kết quả desktop, IDE, remote và cloud chỉ được công bố khi đã quan sát trực tiếp trên client đó.

## §7 Trạng thái triển khai

Thiết kế namespace riêng cho Codex đã bị loại bỏ. Nguồn Codex vẫn độc lập trong skill, còn project đích dùng trực tiếp `.agent-workspace/` làm genome chung. Bộ cài Codex bootstrap workspace khi chưa có và tái sử dụng workspace hoàn chỉnh khi đã tồn tại.

Việc commit, push, phát hành plugin hoặc triển khai sang project khác không nằm trong thay đổi này trừ khi người dùng yêu cầu riêng.
