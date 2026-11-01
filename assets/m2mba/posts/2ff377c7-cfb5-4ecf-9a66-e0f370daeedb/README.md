---
id: 335
title: "Sử dụng google Opal để phân tích API của 1 usecase"
author: "Đậu Thị Ngọc Ánh"
created_at: "2025-10-11T12:34:33.000Z"
source_url: "https://m2mba.com/blog/articles/2ff377c7-cfb5-4ecf-9a66-e0f370daeedb"
---

# Sử dụng google Opal để phân tích API của 1 usecase

*Tác giả: Đậu Thị Ngọc Ánh | Ngày đăng: 2025-10-11T12:34:33.000Z*

Flow mà Opal tạo ra theo yêu cầu của mình

Ds các API thể hiện trên ứng dụng do Opal tạo ra

 

**I. Phân biệt thông tin phía máy khách và yêu cầu API Backend**

 

Trong luồng chuyển khoản liên ngân hàng, việc tối ưu hóa xử lý dữ liệu phía máy khách (client-side) có thể giảm đáng kể số lượng cuộc gọi API tới backend, cải thiện hiệu suất và trải nghiệm người dùng.

 

**1. Màn hình "Chuyển tiền - Nhập thông tin"**

 

- **Thông tin có thể xử lý và hiển thị theo chương trình phía máy khách mà không cần gọi API backend mới:****Số tài khoản nguồn, Tên tài khoản nguồn, Số dư tài khoản nguồn:** Các thông tin này thường được lấy từ một API duy nhất khi người dùng đăng nhập hoặc chọn tài khoản (ví dụ: API Lấy danh sách tài khoản của người dùng). Sau khi nhận được từ backend, dữ liệu này có thể được lưu trữ tạm thời phía máy khách và hiển thị/cập nhật dựa trên lựa chọn của người dùng mà không cần gọi lại API cho mỗi lần hiển thị hoặc chuyển đổi tài khoản.
- **Ngân hàng thụ hưởng (Danh sách):** Danh sách các ngân hàng được hỗ trợ cho chuyển khoản liên ngân hàng có thể được tải về một lần (ví dụ: khi khởi động ứng dụng hoặc lần đầu truy cập chức năng chuyển tiền) thông qua API Lấy danh sách ngân hàng. Dữ liệu này sau đó được lưu trữ cục bộ và được sử dụng để populate trường chọn (Dropdown) "Ngân hàng thụ hưởng". Việc người dùng chọn một ngân hàng từ danh sách này là thao tác phía máy khách, không kích hoạt API backend mới.
- **Số tiền chuyển, Nội dung chuyển tiền:** Đây là dữ liệu do người dùng nhập trực tiếp và được xử lý hoàn toàn phía máy khách.
- **Số tiền bằng chữ:** Đây là một ví dụ điển hình về xử lý theo chương trình phía máy khách. Khi người dùng nhập "Số tiền chuyển", ứng dụng khách có thể tự động chuyển đổi số tiền số thành chữ (ví dụ: "Mười nghìn Việt Nam Đồng") và hiển thị ngay lập tức mà không cần gửi dữ liệu này lên backend.
- **Thông tin yêu cầu gọi API backend:****Tên tài khoản thụ hưởng:** Sau khi người dùng nhập "Số tài khoản thụ hưởng" và chọn "Ngân hàng thụ hưởng", một lệnh gọi API backend (API Xác thực tài khoản thụ hưởng) là cần thiết để xác minh tính hợp lệ của tài khoản và lấy tên chủ tài khoản tương ứng từ ngân hàng thụ hưởng.
 

**II. Phân tích dữ liệu yêu cầu và phản hồi cho từng API được xác định**

 

Dựa trên luồng nghiệp vụ và các phần tử động, các API sau đây được xác định:

 

**1. API Lấy chi tiết tài khoản nguồn**

    *   **Mục đích:** Cung cấp thông tin về tài khoản nguồn được chọn.

    *   **Yêu cầu (Request):** { "accountId": "string" } (Mã định danh tài khoản nguồn của người dùng)

    *   **Phản hồi (Response):** { "accountNumber": "0050109502003", "accountName": "DAU THI NGOC ANH", "currentBalance": 19756974, "currency": "VND" }

 

**2. API Lấy danh sách ngân hàng**

    *   **Mục đích:** Cung cấp danh sách các ngân hàng để chọn làm ngân hàng thụ hưởng.

    *   **Yêu cầu (Request):** { "type": "INTERBANK" } (Có thể thêm bộ lọc loại ngân hàng nếu cần)

    *   **Phản hồi (Response):** [ { "bankId": "VIETINBANK_ID", "bankName": "Công Thương Việt Nam (VIETINBANK)", "shortName": "VIETINBANK" }, ... ]

 

**3. API Xác thực tài khoản thụ hưởng**

    *   **Mục đích:** Kiểm tra tính hợp lệ của số tài khoản thụ hưởng và lấy tên chủ tài khoản.

    *   **Yêu cầu (Request):** { "beneficiaryAccountNumber": "103003178522", "beneficiaryBankId": "VIETINBANK_ID" }

    *   **Phản hồi (Response):** { "beneficiaryAccountName": "NGUYEN THI GIANG", "verificationStatus": "SUCCESS" } (Hoặc "ACCOUNT_NOT_FOUND", "BANK_ERROR")

 

**4. API Tiền kiểm tra giao dịch / Tính phí**

    *   **Mục đích:** Tổng hợp các thông tin đã nhập, tính toán phí giao dịch, xác định hình thức chuyển và trả về tổng quan giao dịch cho màn hình xác nhận.

    *   **Yêu cầu (Request):** { "sourceAccountId": "string", "beneficiaryBankId": "string", "beneficiaryAccountNumber": "string", "beneficiaryAccountName": "string", "amount": 10000, "transferContent": "DAU THI NGOC ANH chuyen khoan" }

    *   **Phản hồi (Response):** { "temporaryTransactionId": "GD1325515_TEMP", "amount": 10000, "sourceAccountName": "DAU THI NGOC ANH", "sourceAccountNumber": "0050109502003", "beneficiaryAccountName": "NGUYEN THI GIANG", "beneficiaryAccountNumber": "103003178522", "beneficiaryBankName": "Công Thương Việt Nam (VIETINBANK)", "feeAmount": "Miễn phí", "transferMethod": "Chuyển nhanh Napas 247", "amountInWords": "Mười nghìn Việt Nam Đồng" }

 

**5. API Khởi tạo/Yêu cầu OTP (cho Digital OTP)**

    *   **Mục đích:** Chuẩn bị backend cho bước xác thực PIN Digital OTP và cung cấp mã giao dịch.

    *   **Yêu cầu (Request):** { "temporaryTransactionId": "GD1325515_TEMP", "otpType": "DIGITAL_OTP" }

    *   **Phản hồi (Response):** { "transactionCode": "GD1325515", "status": "OTP_REQUIRED_DIGITAL_PIN" }

 

**6. API Xác thực PIN Digital OTP**

    *   **Mục đích:** Xác minh PIN Digital OTP do người dùng nhập.

    *   **Yêu cầu (Request):** { "transactionCode": "GD1325515", "digitalPin": "123456" }

    *   **Phản hồi (Response):** { "validationStatus": "SUCCESS", "message": "PIN Digital OTP hợp lệ" } (Hoặc "FAILED", "BLOCKED")

 

**7. API Khởi tạo/Yêu cầu OTP (cho SMS/Soft OTP)**

    *   **Mục đích:** Gửi mã OTP đến người dùng và cung cấp mã OTP hiển thị (nếu là Soft OTP) cùng thời gian hiệu lực.

    *   **Yêu cầu (Request):** { "temporaryTransactionId": "GD1325515_TEMP", "otpType": "SMS_OTP" }

    *   **Phản hồi (Response):** { "otpCode": "38805538", "otpExpiryTimestamp": "2025-10-11T19:30:00Z", "resendAttemptsRemaining": 2, "message": "Mã OTP đã được gửi đến số điện thoại đăng ký." }

 

**8. API Xác thực mã OTP**

    *   **Mục đích:** Xác minh mã OTP (SMS/Soft OTP) do người dùng nhập.

    *   **Yêu cầu (Request):** { "transactionCode": "GD1325515", "otpCode": "38805538" }

    *   **Phản hồi (Response):** { "validationStatus": "SUCCESS", "message": "Xác thực OTP thành công" } (Hoặc "FAILED", "EXPIRED", "BLOCKED")

 

**9. API Thực hiện giao dịch**

    *   **Mục đích:** Hoàn tất việc chuyển tiền sau khi xác thực thành công.

    *   **Yêu cầu (Request):** { "transactionCode": "GD1325515", "otpValidationResult": "SUCCESS" } (Hoặc token xác thực)

    *   **Phản hồi (Response):** { "transactionStatus": "SUCCESS", "finalTransactionId": "FT22361714185045", "transactionTimestamp": "15:54:36, 27/12/2022", "amount": 10000, "sourceAccountNumber": "0050109502003", "sourceAccountName": "DAU THI NGOC ANH", "beneficiaryAccountNumber": "103003178522", "beneficiaryAccountName": "NGUYEN THI GIANG", "beneficiaryBankName": "Công Thương Việt Nam (VIETINBANK)", "transferContent": "DAU THI NGOC ANH chuyen khoan", "transferMethod": "Chuyển nhanh Napas 247" }

 

**III. Phương pháp thu thập dữ liệu cho các chuyển đổi màn hình**

 

- **Chuyển từ "Chuyển tiền - Nhập thông tin" sang "Xác nhận thông tin":****a) Đầu vào trực tiếp của người dùng:** "Số tiền chuyển", "Nội dung chuyển tiền", "Ngân hàng thụ hưởng" (lựa chọn từ danh sách), "Số tài khoản thụ hưởng".
- **b) Dữ liệu được chuyển từ lệnh gọi API trước đó:** "Số tài khoản nguồn", "Tên tài khoản nguồn", "Số dư tài khoản nguồn" (từ API Lấy chi tiết tài khoản nguồn), "Tên tài khoản thụ hưởng" (từ API Xác thực tài khoản thụ hưởng).
- **c) Dữ liệu yêu cầu một lệnh gọi API mới cụ thể cho màn hình tiếp theo:** "Phí giao dịch", "Hình thức chuyển" (từ API Tiền kiểm tra giao dịch / Tính phí). API này cũng sẽ trả về các thông tin tổng hợp khác để đảm bảo tính nhất quán trên màn hình xác nhận.
- **Chuyển từ "Xác nhận thông tin" sang "Lấy mã OTP - Nhập PIN Digital OTP":****b) Dữ liệu được chuyển từ lệnh gọi API trước đó:** Tất cả thông tin giao dịch đã hiển thị trên màn hình xác nhận (được lưu trữ tạm thời phía máy khách hoặc lấy từ phản hồi của API Tiền kiểm tra giao dịch / Tính phí).
- **c) Dữ liệu yêu cầu một lệnh gọi API mới cụ thể cho màn hình tiếp theo:** "Mã giao dịch" (từ API Khởi tạo/Yêu cầu OTP (cho Digital OTP)).
- **Chuyển từ "Lấy mã OTP - Nhập PIN Digital OTP" sang "Chuyển tiền thành công" (hoặc "Lấy mã OTP - Hiển thị và nhập mã OTP"):****a) Đầu vào trực tiếp của người dùng:** "Trường nhập PIN Digital OTP".
- **b) Dữ liệu được chuyển từ lệnh gọi API trước đó:** "Mã giao dịch" (từ API Khởi tạo/Yêu cầu OTP).
- **c) Dữ liệu yêu cầu một lệnh gọi API mới cụ thể cho màn hình tiếp theo:** API Xác thực PIN Digital OTP. Nếu xác thực thành công, sẽ kích hoạt API Thực hiện giao dịch và chuyển đến màn hình "Chuyển tiền thành công". Nếu không thành công hoặc chuyển sang phương thức OTP khác, có thể dẫn đến API Khởi tạo/Yêu cầu OTP (cho SMS/Soft OTP) và chuyển đến màn hình "Lấy mã OTP - Hiển thị và nhập mã OTP".
- **Chuyển từ "Lấy mã OTP - Hiển thị và nhập mã OTP" sang "Chuyển tiền thành công":****a) Đầu vào trực tiếp của người dùng:** "Trường nhập OTP".
- **b) Dữ liệu được chuyển từ lệnh gọi API trước đó:** "Mã OTP hiển thị", "Thời gian hiệu lực OTP" (từ API Khởi tạo/Yêu cầu OTP (cho SMS/Soft OTP)), "Mã giao dịch" (từ API khởi tạo OTP).
- **c) Dữ liệu yêu cầu một lệnh gọi API mới cụ thể cho màn hình tiếp theo:** API Xác thực mã OTP. Sau khi xác thực thành công, API này sẽ kích hoạt API Thực hiện giao dịch để lấy dữ liệu cuối cùng và hiển thị màn hình "Chuyển tiền thành công".
 

**IV. API mới với tiềm năng trả về nhiều phần thông tin**

 

Để tối ưu hóa luồng dữ liệu và cung cấp trải nghiệm phong phú hơn, các API sau đây có tiềm năng được thiết kế để trả về nhiều phần thông tin liên quan, giảm số lượng cuộc gọi và cho phép xử lý linh hoạt hơn phía máy khách:

 

- **API Lấy danh sách tài khoản và số dư (Get User Accounts & Balances API):****Tiềm năng:** Cung cấp thông tin của tất cả các tài khoản thuộc về người dùng, không chỉ tài khoản được chọn.
- **Thông tin trả về mở rộng:** Danh sách các tài khoản, mỗi tài khoản bao gồm accountId, accountNumber, accountName, currentBalance, currency, accountType (tài khoản thanh toán, tiết kiệm, tín dụng...), branchInfo (thông tin chi nhánh), isDefault (có phải tài khoản mặc định không).
- **Lợi ích:** Máy khách có thể hiển thị tổng quan số dư tất cả tài khoản, cho phép người dùng dễ dàng chuyển đổi tài khoản nguồn mà không cần gọi API riêng biệt, hoặc hiển thị thông tin chi tiết tài khoản khác trên các màn hình liên quan.
- **API Lấy danh sách ngân hàng và thông tin bổ sung (Get Banks & Supplemental Info API):****Tiềm năng:** Cung cấp thông tin chi tiết hơn về các ngân hàng thụ hưởng.
- **Thông tin trả về mở rộng:** bankId, bankName, shortName, napasCode, swiftCode, bankLogoUrl (URL logo ngân hàng), transferTypesSupported (vd: NAPAS 247, chuyển thường), cutOffTime (thời gian giới hạn giao dịch trong ngày), transferLimits (giới hạn chuyển tiền theo ngân hàng/hình thức).
- **Lợi ích:** Máy khách có thể hiển thị logo ngân hàng, đưa ra cảnh báo về giới hạn chuyển tiền hoặc thời gian cắt giao dịch ngay trên màn hình nhập liệu hoặc xác nhận, cải thiện trải nghiệm người dùng và giúp đưa ra quyết định tốt hơn.
- **API Xác thực tài khoản thụ hưởng nâng cao (Enhanced Beneficiary Account Verification API):****Tiềm năng:** Cung cấp thông tin sâu hơn về tài khoản thụ hưởng.
- **Thông tin trả về mở rộng:** beneficiaryAccountName, verificationStatus, beneficiaryBankName (tên đầy đủ), accountType (cá nhân/tổ chức), isActiveStatus (trạng thái hoạt động của tài khoản), suggestedTransferMethod (hình thức chuyển tiền tối ưu được đề xuất).
- **Lợi ích:** Giúp ứng dụng xác định và gợi ý hình thức chuyển tiền phù hợp, cảnh báo nếu tài khoản thụ hưởng có vấn đề về trạng thái, hoặc hiển thị thông tin tài khoản đầy đủ trên màn hình xác nhận.
- **API Tiền kiểm tra giao dịch toàn diện (Comprehensive Transaction Pre-check API):****Tiềm năng:** Trả về tất cả dữ liệu cần thiết để populate màn hình xác nhận và cung cấp ngữ cảnh cho các bước tiếp theo.
- **Thông tin trả về mở rộng:** temporaryTransactionId, feeAmount, transferMethod, exchangeRate, totalAmountToDebit (tổng tiền trừ từ tài khoản nguồn), sourceAccountName, sourceAccountNumber, beneficiaryAccountName, beneficiaryAccountNumber, beneficiaryBankName, amountInWords (từ backend, đảm bảo tính chính xác), transactionWarnings (vd: số dư không đủ, vượt hạn mức, phí cao), estimatedCompletionTime (thời gian dự kiến hoàn tất giao dịch), otpMethodOptions (các phương thức OTP khả dụng cho giao dịch này).
- **Lợi ích:** Đảm bảo màn hình xác nhận hiển thị đầy đủ và chính xác tất cả thông tin chỉ với một lệnh gọi API. Máy khách có thể sử dụng transactionWarnings để hiển thị thông báo ngay lập tức, và otpMethodOptions để cho phép người dùng chọn phương thức xác thực OTP.
- **API Kết quả giao dịch chi tiết (Detailed Transaction Result API):****Tiềm năng:** Cung cấp bản tóm tắt đầy đủ về giao dịch đã hoàn thành.
- **Thông tin trả về mở rộng:** transactionStatus, finalTransactionId, transactionTimestamp, amount, feeApplied, sourceAccountNumber, sourceAccountName, beneficiaryAccountNumber, beneficiaryAccountName, beneficiaryBankName, transferContent, transferMethod, referenceNumber (số tham chiếu của ngân hàng/Napas), balanceAfterTransaction (số dư tài khoản nguồn sau giao dịch), receiptLink (link tải biên lai giao dịch).
- **Lợi ích:** Cung cấp tất cả thông tin cần thiết cho màn hình "Chuyển tiền thành công" và cho phép người dùng xem lại chi tiết, tải biên lai, hoặc chia sẻ thông tin mà không cần thực hiện thêm lệnh gọi API. balanceAfterTransaction cung cấp thông tin hữu ích cho người dùng ngay lập tức.
 

**V. Tổng kết**

 

Báo cáo này đã cung cấp một phân tích luồng dữ liệu chi tiết cho trường hợp sử dụng chuyển khoản liên ngân hàng. Chúng ta đã phân biệt rõ ràng các phần tử có thể được xử lý theo chương trình phía máy khách (như chuyển đổi số tiền bằng chữ, hiển thị dữ liệu đã có) và các phần tử yêu cầu tương tác với API backend.

 

Việc xác định và phân tích dữ liệu yêu cầu/phản hồi cho từng API tiềm năng là cơ sở để phát triển hệ thống mạnh mẽ. Đặc biệt, việc đề xuất các API mới với khả năng trả về nhiều phần thông tin (như API Tiền kiểm tra giao dịch toàn diện và API Kết quả giao dịch chi tiết) sẽ góp phần tối ưu hóa hiệu quả truyền tải dữ liệu, giảm thiểu số lượng cuộc gọi API và cung cấp cho ứng dụng khách một bộ dữ liệu phong phú để xử lý và hiển thị linh hoạt hơn. Điều này không chỉ cải thiện hiệu suất của ứng dụng mà còn nâng cao trải nghiệm tổng thể cho người dùng trong quá trình thực hiện chuyển khoản.