---
scope: project
documentType: Implementation Report
status: Implemented
implementedAt: 2026-09-16
---

# Nguồn Codex độc lập, project genome dùng chung

## Cấu trúc nguồn

Toàn bộ nguồn phân phối Codex nằm trong [`skills/init-codex-genome/`](../../skills/init-codex-genome/SKILL.md). Copy nguyên thư mục này vào `.agents/skills/` của project mới rồi yêu cầu Codex khởi tạo genome. Skill chứa nguồn bootstrap, template, công cụ triển khai và VERSION; nó không phụ thuộc vào cây nguồn Claude Code khi chạy.

Thư mục `codex/` ở root đã được bỏ. Kiểm thử nằm trong `tests/codex/`, công cụ và metadata đóng gói nằm trong `scripts/codex/`, còn [tài liệu phát triển](../codex/index.md) nằm trong `docs/codex/`. Những phần hỗ trợ này không chứa một cây rule hoặc guide thứ hai.

Hai bộ phân phối vẫn được biên soạn độc lập: `skills/init-project/` cho Claude Code và `skills/init-codex-genome/` cho Codex. Sự độc lập này thuộc lớp nguồn và cấu hình harness, không tạo hai genome riêng trong project đích.

## Cấu trúc được triển khai

Project chỉ có một không gian genome tại `.agent-workspace/`. Cả `CLAUDE.md` và `AGENTS.md` đều dẫn agent tới cùng guide, role, lesson, decision, wiki và task state. Các file cấu hình và sổ sở hữu của từng harness vẫn tách riêng:

| Thành phần | Vị trí |
|---|---|
| Dữ liệu và quy trình chung | `.agent-workspace/` |
| Adapter Claude Code | `CLAUDE.md`, `.claude/` |
| Adapter Codex | `AGENTS.md`, `.codex/`, `.agent-workspace/rules/` |
| Manifest Codex | `.codex/genome-manifest.json` |
| Lock và journal Codex | `.codex/genome-update-lock.json`, `.codex/genome-update-journal.json` |

Khi project chưa có genome, một trong hai bộ cài có thể tạo nội dung chung từ bundle của mình. Khi project đã có một genome hoàn chỉnh, bộ cài còn lại giữ nguyên nội dung đó và chỉ thêm adapter của harness. Manifest ghi trạng thái tái sử dụng và không nhận ownership guide hoặc record chung.

## Bảo trì nguồn

Sửa trực tiếp trong skill: `bundle/portable/` là nguồn được biên soạn; `bundle/templates/` chứa nội dung khởi tạo. Sau khi review, chạy từ root repository:

```text
python skills/init-codex-genome/scripts/genome.py refresh
python skills/init-codex-genome/scripts/genome.py refresh --apply
python skills/init-codex-genome/scripts/genome.py check
```

`refresh` cập nhật inventory và hash trong bundle map. `check` dựng project tạm để kiểm tra nguồn và instruction network. Hai lệnh này không đồng bộ nội dung từ bộ Claude Code và không tạo thêm bản live trong repository.

VERSION chuẩn nằm trong skill. Công cụ phát triển ở `scripts/codex/` nhận `--skill-root` khi đồng bộ phiên bản hoặc đóng gói plugin. Cách copy skill trực tiếp không cần đóng gói plugin.

## Kiểm chứng cần giữ

Suite Codex đã chạy 47 ca: 46 ca đạt và một ca symlink bị bỏ qua do quyền Windows; ca junction thật đạt. Kiểm tra tích hợp đã chạy cả hai thứ tự cài đặt, chạy cả hai updater và xác nhận các file chung giữ nguyên byte. Adapter được cài sau ghi trạng thái tái sử dụng và không liệt kê các file chung trong manifest của mình. Trường hợp genome Claude chưa bật wiki cũng được kiểm tra: Codex chỉ bổ sung seed wiki còn thiếu và không nhận ownership các file chung đã có.

[Bằng chứng kiểm tra hiện tại](codex/shared-workspace-checks.json) cũng ghi kết quả source check, hồi quy Claude, validator skill, đồng bộ phiên bản và build package tạm. Các báo cáo thử nghiệm ban đầu dưới `docs/genome/codex/` là bằng chứng lịch sử của kiến trúc trước khi sửa namespace; chúng không còn là hướng dẫn đường dẫn hiện hành.

Chưa có commit, push, phát hành hay triển khai sang Hi Tuấn C trong thay đổi này.
