---
scope: project
documentType: Evaluation Report
status: Completed
evaluatedAt: 2026-09-16
---

# So sánh đầu ra của Claude khi dùng genome cũ và mới

## §1 Kết luận

Phép thử đã chạy được sau khi tài khoản Claude được cấp lại lượt sử dụng. Kết quả xác nhận bộ chỉ dẫn mới không còn yêu cầu chung buộc câu trả lời so sánh phải dùng bảng. Tuy nhiên, **chưa đủ bằng chứng để kết luận rằng việc viết lại genome đã giải quyết được vấn đề văn phong**. Chất lượng các mẫu không đồng đều, và cả hai phiên bản đều có đầu ra cần biên tập.

Phép thử còn phát hiện một lỗi quy trình trong bản viết lại: Claude bỏ qua việc đọc hai mục tra cứu bắt buộc trước khi trả lời. Chỉ dẫn này đã được làm rõ bằng câu đầy đủ trong `CLAUDE.md` và template phân phối. Sáu lượt thử sau sửa đều thực hiện hai lần đọc. Đây là kết quả về việc tuân thủ quy trình, không phải bằng chứng rằng chất lượng văn phong đã tốt hơn.

Các mẫu sau sửa vẫn có phần giới thiệu việc chọn vai trò không phục vụ người đọc, kể cả khi đề bài chỉ yêu cầu lời kể. Báo cáo giữ nguyên lỗi này, không chỉnh câu trả lời thử nghiệm để làm đẹp kết quả và không bổ sung một bộ quy định văn phong chung để che nó đi.

## §2 Thiết kế phép thử

Ba đề bài tiếng Việt được dùng cho cả hai phiên bản: lời kể mở đầu về nhân vật hư cấu Minh; nội dung giải thích quy trình hỗ trợ gửi khách hàng; và câu trả lời tư vấn cách soạn bản đề xuất. Mỗi đề bài chạy hai lần ở mỗi phiên bản, tạo thành sáu cặp với tổng cộng 12 đầu ra ban đầu. Sáu lượt bổ sung kiểm tra bản mới sau khi sửa yêu cầu đọc tài liệu.

Bản cũ được lấy từ commit `13fc9fa26e9e7d54e0cc58c818d196d5b284cd52`, tương ứng bundle 4.0.0. Bản mới là bộ nguồn 5.0.0 đang chuẩn bị cục bộ. Hai project thử nghiệm nằm ngoài repo nguồn và ngoài Hi Tuấn C. Giá trị project và ngôn ngữ giống nhau; không thêm một yêu cầu “viết tự nhiên” vào riêng nhánh nào.

Mỗi lượt là một phiên Claude Code mới, phiên bản CLI 2.1.73. Tất cả 18 lượt viết báo cáo model `claude-opus-4-6`, hoàn thành thành công và không có yêu cầu công cụ bị từ chối. Cả hai nhánh được cấp cùng bốn công cụ đọc `Read`, `Glob`, `Grep`, `Skill`, chỉ dùng cấu hình project, không lưu phiên và không nạp MCP ngoài cấu hình chặt đã chọn. Các flag chính xác nằm trong [metadata thực thi](thu-nghiem-claude/run-metadata.json).

Hai phiên hiệu chuẩn riêng được chạy trước khi viết, yêu cầu Claude nêu các rule project đã có trong context mà không dùng công cụ. Bản cũ báo có bốn rule nền, gồm `conversational-output.md` và câu `comparison → table`. Bản mới báo ba rule, không có yêu cầu đó. Đây là lời tự báo của model, được đối chiếu với danh mục file; nó không chứng minh toàn bộ context ẩn của nhà cung cấp. Các đường dẫn tổ tiên và thư mục chỉ dẫn người dùng đã kiểm tra được ghi trong [danh mục đầu vào](thu-nghiem-claude/input-inventory.json).

Skill `document-writer` xuất hiện trong danh sách skill của nhánh cũ và không có trong nhánh mới; không lượt viết nào gọi skill này. Không có plugin được báo trong các phiên. Các skill mặc định của Claude Code vẫn có mặt. Vì vậy đây là so sánh hai bộ genome thực tế, không phải thí nghiệm chỉ thay duy nhất độ nén của câu.

## §3 Những gì xuất hiện trong 12 mẫu ban đầu

### Lời kể

Ở lần thứ nhất, cả hai phiên bản đều thêm lời dẫn và lời bình ngoài kịch bản, trái với yêu cầu chỉ viết phần có thể đọc thành tiếng. Bản cũ còn cho Minh “gập laptop lại”, rồi kể bản đề xuất vẫn ở trên màn hình mà không nối lại hành động mở máy. Bản mới giữ diễn biến liền hơn, nhưng phần lời bình về nhịp kể vẫn phải xóa trước khi sử dụng.

Ở lần thứ hai, bản cũ chỉ trả lời kể, nhưng câu “Minh vừa mất việc vừa thêm áy náy” làm sai nghĩa: “mất việc” thường được hiểu là bị sa thải, trong khi tình huống chỉ nói mất thời gian. Bản mới không có lỗi nghĩa này, song tiếp tục thêm đoạn nhận xét về chính lời kể. Một bản tuân thủ phạm vi đầu ra tốt hơn nhưng mắc lỗi ngôn ngữ; bản còn lại rõ nghĩa hơn nhưng trả thêm phần không được yêu cầu. Không nên gộp hai tiêu chí thành một kết luận thắng tuyệt đối.

### Nội dung gửi khách hàng

Cả bốn mẫu phân biệt được xác nhận tiếp nhận trong một ngày làm việc với kết quả giải quyết, và không đặt thời hạn hoàn tất mới. Cấu trúc đánh số bước giúp theo dõi quy trình trong trường hợp này; bản thân việc có cấu trúc không phải lỗi văn phong.

Bản cũ ở lần hai có bảng phân biệt hai email, phục vụ đúng mục tiêu đề bài. Tuy nhiên, nó còn thêm ba gạch đầu dòng giải thích cách đã viết, khiến người sử dụng phải tách phần gửi khách khỏi phần trao đổi nội bộ. Bản mới không có phần bình luận đó trong hai lượt ban đầu. Một số cách nói như “đưa vào hàng chờ” hoặc “bắt đầu được xem xét” cụ thể hơn dữ kiện đã cung cấp; với tài liệu khách hàng thật, cần kiểm tra trước khi biến chúng thành mô tả chính thức của dịch vụ.

### Giải thích trong hội thoại

Hai mẫu cũ dùng nhiều thuật ngữ pha tiếng Anh như “outline cứng”, “prose”, “skeleton”, “incremental” và “batch”, rồi kết bằng mục “Bước tiếp”. Hai mẫu mới ban đầu giải thích chủ yếu bằng tiếng Việt và dễ theo dõi hơn ở điểm này. Đây là nhận xét biên tập trên các mẫu cụ thể, không phải thước đo khách quan cho mọi người đọc.

Cả hai phía vẫn có khẳng định quá chắc. Bản cũ nói lỗi số liệu ở phần nội dung chỉ là lỗi cục bộ; điều này không luôn đúng nếu số liệu làm thay đổi đề xuất. Bản mới nói làm dàn ý “gần như không tốn thời gian” hoặc giúp tránh cả hai nhược điểm. Các câu đó cần được cân nhắc lại nếu sử dụng như lời khuyên thực tế.

Dù nhánh cũ báo có quy định so sánh phải dùng bảng, cả hai câu trả lời hội thoại của nó đều không dùng bảng. Đây cũng là bằng chứng rằng không thể suy trực tiếp từ một câu rule sang mọi hành vi đầu ra.

## §4 Lỗi đọc tài liệu và kết quả sau sửa

Log của sáu lượt cũ ghi nhận việc đọc cả `.agent-workspace/lessons/index.md` và `.agent-workspace/guide/roles/index.md`. Hai lượt viết tài liệu khách hàng còn đọc vai trò developer và tiêu chí business-analyst, qa, dù đề bài là dịch vụ hư cấu, không phải mô tả phần mềm. Sáu lượt dùng bản mới ban đầu không gọi công cụ nào, nên việc không đọc các vai trò phần mềm chưa thể được tính là chọn vai trò đúng: nó đã bỏ qua cả bước định tuyến.

Template mới khi đó dùng câu “At the start of a task, consult …”. Việc viết lại đã giữ ý định yêu cầu đọc, nhưng không giữ hiệu lực hành vi trong các lượt thử này. Chưa thể xác định cơ chế bên trong model. Giả thuyết có thể kiểm tra là hành động và phạm vi cần được nêu rõ hơn.

Bản sửa yêu cầu dùng công cụ đọc hai mục tra cứu trước khi trả lời một nhiệm vụ mới, nêu rõ áp dụng cho cả câu hỏi hội thoại và yêu cầu viết. Câu vẫn đầy đủ về ngữ pháp; không khôi phục ký hiệu mệnh lệnh nén. Hai lượt hội thoại thử trước đều đọc đủ; bốn lượt lời kể và tài liệu khách hàng tiếp theo cũng đọc đủ. Không lượt nào ép vai trò phần mềm vào những công việc này.

Sau sửa, cả sáu câu trả lời mở đầu bằng lời giải thích rằng không có lesson store hoặc role phù hợp. Hai mẫu lời kể vì vậy vẫn vi phạm yêu cầu chỉ trả lời kể. Mẫu hội thoại thứ nhất còn quay lại dùng “incremental editing”, “draft-then-revise” và nói lượt sửa cuối “chỉ sửa diễn đạt, không phải sửa logic”, một khẳng định quá mạnh. Những kết quả này không ủng hộ kết luận đơn giản rằng bỏ rule văn phong sẽ tự động tạo ra văn tự nhiên.

Chỉ phần yêu cầu đọc tài liệu đã được áp dụng vào bộ nguồn. Các vấn đề trong văn bản thử được ghi nhận như giới hạn của đầu ra hiện tại. Chưa có sửa đổi nào về văn phong chung phát sinh từ phép thử; một bộ tiêu chí cho kịch bản hoặc nội dung gửi khách hàng cần thuộc phạm vi của chính loại đầu ra đó.

## §5 Đọc độc lập với nhãn đã ẩn

Một phiên Claude riêng, không dùng genome của hai project thử và không có công cụ, đọc sáu cặp ban đầu dưới nhãn A/B được đổi vị trí giữa các cặp. Phiên này không được cung cấp giả thuyết cần chứng minh hay ánh xạ cũ–mới. [Đầu vào đánh giá](thu-nghiem-claude/blind-packet.md), [kết quả nguyên văn](thu-nghiem-claude/blind-review.output.md) và [ánh xạ nhãn](thu-nghiem-claude/blind-mapping.json) được giữ lại.

Đánh giá độc lập cũng ghi nhận lỗi “mất việc” và việc thêm phần bình luận vào lời kể. Nó không luôn ưu tiên bản mới: ở cặp tài liệu thứ hai, nó thích bảng của bản cũ hơn. Tuy nhiên, đánh giá này có chỗ đọc thiếu: ở cặp hội thoại thứ nhất, nó nói chỉ bản mới có cách viết theo cụm, trong khi bản cũ cũng nêu “2–3 phần gộp”. Nó còn khen một số nhận định mà người tổng hợp cho là quá chắc. Vì vậy báo cáo không dùng số lần A/B được chọn làm điểm chất lượng.

Đây là kiểm tra chéo bằng AI cùng dòng model, không thay thế phản hồi của người đọc hoặc khách hàng. Phiên đánh giá chỉ xem các mẫu trước sửa yêu cầu đọc tài liệu; không dùng nhận xét đó để chấm các mẫu sau sửa.

## §6 Mẫu và khả năng đối chiếu

Các file bên dưới giữ nguyên nội dung Claude trả về, kể cả phần thừa và lỗi. `new` là bản viết lại trước sửa yêu cầu đọc; `new-routing` là bản sau sửa. Đề bài không đổi giữa các lượt tương ứng.

| Đề bài và lượt | Bản cũ | Bản mới ban đầu | Bản mới sau sửa yêu cầu đọc |
|---|---|---|---|
| Lời kể, lượt 1 | [Cũ](thu-nghiem-claude/narration-1-old.output.md) | [Mới](thu-nghiem-claude/narration-1-new.output.md) | [Sau sửa](thu-nghiem-claude/narration-1-new-routing.output.md) |
| Lời kể, lượt 2 | [Cũ](thu-nghiem-claude/narration-2-old.output.md) | [Mới](thu-nghiem-claude/narration-2-new.output.md) | [Sau sửa](thu-nghiem-claude/narration-2-new-routing.output.md) |
| Tài liệu khách hàng, lượt 1 | [Cũ](thu-nghiem-claude/client_document-1-old.output.md) | [Mới](thu-nghiem-claude/client_document-1-new.output.md) | [Sau sửa](thu-nghiem-claude/client_document-1-new-routing.output.md) |
| Tài liệu khách hàng, lượt 2 | [Cũ](thu-nghiem-claude/client_document-2-old.output.md) | [Mới](thu-nghiem-claude/client_document-2-new.output.md) | [Sau sửa](thu-nghiem-claude/client_document-2-new-routing.output.md) |
| Hội thoại, lượt 1 | [Cũ](thu-nghiem-claude/conversation-1-old.output.md) | [Mới](thu-nghiem-claude/conversation-1-new.output.md) | [Sau sửa](thu-nghiem-claude/conversation-1-new-routing.output.md) |
| Hội thoại, lượt 2 | [Cũ](thu-nghiem-claude/conversation-2-old.output.md) | [Mới](thu-nghiem-claude/conversation-2-new.output.md) | [Sau sửa](thu-nghiem-claude/conversation-2-new-routing.output.md) |

Đề bài nguyên văn: [lời kể](thu-nghiem-claude/narration.prompt.txt), [tài liệu khách hàng](thu-nghiem-claude/client_document.prompt.txt), [hội thoại](thu-nghiem-claude/conversation.prompt.txt). Hai kết quả hiệu chuẩn: [cũ](thu-nghiem-claude/calibration-1-old.output.md) và [mới](thu-nghiem-claude/calibration-1-new.output.md).

Hash đầu vào ban đầu không thay đổi sau các lượt chạy. Phần bắt đầu công việc của fixture sau sửa khớp với template hiện tại. Metadata lưu model, công cụ đã gọi và hash đầu ra để có thể đối chiếu; không đưa dữ liệu xác thực hoặc transcript hệ thống thô vào hồ sơ này.

## §7 Giới hạn

Mỗi đề bài chỉ có hai lần lặp cho mỗi cấu hình. Cách sinh văn bản có biến động, không đặt seed và không kiểm soát mọi yếu tố dịch vụ. Sáu lượt sau sửa được thực hiện muộn hơn; nhánh cũ không được chạy lại đồng thời với chúng. Kết quả không phải một ước lượng có ý nghĩa thống kê.

Không có nhánh Claude không dùng genome, nên chưa thể so sánh với trải nghiệm hội thoại thông thường mà người dùng mô tả. Toàn bộ bộ chỉ dẫn, cách định tuyến và danh mục skill đều thay đổi giữa hai phiên bản; phép thử không tách riêng tác động của câu nén khỏi việc gỡ quy định văn phong. Bộ mẫu cũng chưa gồm tài liệu dài hoặc phản hồi của khách hàng thật.

Điều đã xác minh là các ràng buộc văn phong chung được gỡ khỏi bộ nguồn và một lỗi tuân thủ quy trình được phát hiện, sửa, rồi thử lại. Điều chưa xác minh là đầu ra của bản mới đạt chuẩn văn phong con người trên các project thực tế. Hai kết luận này cần được giữ tách biệt.
