<!-- Tự động tải từ Google Drive "SRS-He thong quan ly.docx" — không sửa tay (bị ghi đè). Nguồn: https://drive.google.com/open?id=1UhUr3qFQHhhCGgbIHR1LXnahggKxWf_y · sửa lần cuối: 2026-08-19T14:14:11.321Z -->

# SRS-He-thong-quan-ly.docx

**Version 0.1**

**Prepared by: Class BA2204**

**Mục lục**

**[1. Introduction](#introduction) 1**

> **[1.1 Purpose](#purpose) 1**
>
> **[1.2 Document Conventions](#document-conventions) 1**
>
> **[1.3 Project Scope](#project-scope) 1**
>
> **[1.3.1 Nghiệp vụ tổng quan](#nghiệp-vụ-tổng-quan) 1**
>
> **[1.3.2 Khảo sát thị trường](#khảo-sát-thị-trường) 3**
>
> **[1.3.3 Xây dựng chương trình đào tạo](#xây-dựng-chương-trình-đào-tạo) 3**
>
> **[1.3.4 Quản lý thư viện tài liệu](#quản-lý-thư-viện-tài-liệu) 3**
>
> **[1.3.5 Marketing quảng bá khóa học](#marketing-quảng-bá-khóa-học) 3**
>
> **[1.3.6 Chăm sóc khách hàng](#chăm-sóc-khách-hàng) 3**
>
> **[1.3.7 Mở lớp học](#mở-lớp-học) 3**
>
> **[1.3.8 Quản lý lớp học](#quản-lý-lớp-học) 3**
>
> **[1.3.9 Quản lý chi phí lớp học](#quản-lý-chi-phí-lớp-học) 3**
>
> **[1.4 References](#references) 3**

**[2. Overall Description](#overall-description) 1**

> **[2.1 Product Perspective](#product-perspective) 1**
>
> **[2.2 Product Features](#product-features) 1**
>
> **[2.3 User Classes and Characteristics](#user-classes-and-characteristics) 1**
>
> **[2.4 Operating Environment](#operating-environment) 1**
>
> **[2.4.1 Mô hình triển khai](#mô-hình-triển-khai) 2**
>
> **[2.4.2 Mô hình đồng bộ dữ liệu từ AD sang Hệ thống Quản lý trung tâm đào tạo](#mô-hình-đồng-bộ-dữ-liệu-từ-ad-sang-hệ-thống-quản-lý-trung-tâm-đào-tạo) 3**
>
> **[+2.4.2.1 Service Đăng ký tài khoản](#service-đăng-ký-tài-khoản) 3**
>
> **[2.4.2.2 Service Cập nhập thông tin tài khoản](#service-cập-nhập-thông-tin-tài-khoản) 9**
>
> **[2.4.2.3 Service Đổi mật khẩu tài khoản](#service-đổi-mật-khẩu-tài-khoản) 10**
>
> **[2.4.2.4 Service xóa tài khoản](#service-xóa-tài-khoản) 12**
>
> **[2.4.2.5 Service tìm kiếm tài khoản (tìm kiếm nhanh)](#service-tìm-kiếm-tài-khoản-tìm-kiếm-nhanh) 16**
>
> **[2.4.2.6 Service tìm kiếm tài khoản theo các thông tin chi tiết](#service-tìm-kiếm-tài-khoản-theo-các-thông-tin-chi-tiết) 18**
>
> **[2.4.3 Mô hình đồng bộ dữ liệu từ hệ thống quản lý trung tâm đào tạo sang AD](#mô-hình-đồng-bộ-dữ-liệu-từ-hệ-thống-quản-lý-trung-tâm-đào-tạo-sang-ad) 21**
>
> **[2.4.3.1 Service Cập nhật thông tin tài khoản](#service-cập-nhật-thông-tin-tài-khoản) 21**
>
> **[2.4.3.2 Service Đổi mật khẩu tài khoản](#service-đổi-mật-khẩu-tài-khoản-1) 24**
>
> **[2.4.3.3 Service Xóa tài khoản](#service-xóa-tài-khoản-1) 26**
>
> **[2.4.3.4 Service tìm kiếm tài khoản (tìm kiếm nhanh)](#service-tìm-kiếm-tài-khoản-tìm-kiếm-nhanh-1) 28**
>
> **[2.4.3.5 Service tìm kiếm tài khoản theo thông tin chi tiết](#service-tìm-kiếm-tài-khoản-theo-thông-tin-chi-tiết) 31**
>
> **[2.5 Assumptions and Dependencies](#assumptions-and-dependencies) 33**

**[3. Functional Requirements](#functional-requirements) 1**

> **[3.1 Đăng nhập hệ thống](#đăng-nhập-hệ-thống) 1**
>
> **[3.2 Quản lý học viên ](#quản-lý-học-viên) 1**
>
> **[3.2.1 Xem danh sách học viên ](#xem-danh-sách-học-viên) 2**
>
> **[3.2.1.1 Mô tả chức năng](#mô-tả-chức-năng) 2**
>
> **[3.2.1.2 Mô tả Usecase](#mô-tả-usecase) 1**
>
> **[3.2.1.3 Biểu đồ tuần tự](#biểu-đồ-tuần-tự) 1**
>
> **[3.2.1.4 Biểu đồ hoạt động](#biểu-đồ-hoạt-động) 2**
>
> **[3.2.1.5 Biểu đồ thực thể quan hệ (ERD)/ Biểu đồ lớp](#biểu-đồ-thực-thể-quan-hệ-erd-biểu-đồ-lớp) 3**
>
> **[3.2.1.6 Giao diện minh họa](#giao-diện-minh-họa) 4**
>
> **[3.2.2 Xem thông tin chi tiết học viên](#xem-thông-tin-chi-tiết-học-viên) 6**
>
> **[3.2.2.1 Mô tả chức năng](#mô-tả-chức-năng-1) 6**
>
> **[3.2.2.2 Mô tả Use case](#mô-tả-use-case) 7**
>
> **[3.2.2.3 Biểu đồ tuần tự](#biểu-đồ-tuần-tự-1) 8**
>
> **[3.2.2.4 Biểu đồ hoạt động](#biểu-đồ-hoạt-động-1) 9**
>
> **[3.2.2.5 Biểu đồ thực thể quan hệ (ERD)/ Biểu đồ lớp](#biểu-đồ-thực-thể-quan-hệ-erd-biểu-đồ-lớp-1) 9**
>
> **[3.2.2.6 Giao diện minh họa](#giao-diện-minh-họa-1) 10**
>
> **[3.2.3 Chỉnh sửa thông tin học viên ](#chỉnh-sửa-thông-tin-học-viên) 11**
>
> **[3.2.4 Xóa thông tin học viên](#xóa-thông-tin-học-viên) 15**
>
> **[ ](#section-3) 16**
>
> **[3.2.5 Tạo thông tin học viên mới ](#tạo-thông-tin-học-viên-mới) 16**
>
> **[3.2.6 Bảo lưu học viên](#bảo-lưu-học-viên) 16**
>
> **[3.2.7 Chuyển đổi trạng thái học viên](#chuyển-đổi-trạng-thái-học-viên) 16**
>
> **[3.2.8 Xếp lớp cho học viên](#xếp-lớp-cho-học-viên) 16**
>
> **[3.2.9 Lịch sử / quá trình học](#lịch-sử-quá-trình-học) 16**
>
> **[3.2.10 Xem đánh giá của học viên](#xem-đánh-giá-của-học-viên) 16**
>
> **[3.3 \[Module 1\]](#module-1) 16**
>
> **[3.3.1 Description and Priority](#description-and-priority) 16**
>
> **[3.3.2 Functional Requirements](#functional-requirements-1) 16**
>
> **[3.4 \[Module 2\] (and so on)](#module-2-and-so-on) 17**
>
> **[3.5 .](#section-4) 17**
>
> **[3.6 Quản lý lớp học](#quản-lý-lớp-học-1) 18**
>
> **[3.6.1 Xem danh sách lớp học](#xem-danh-sách-lớp-học) 18**
>
> **[3.6.1.1 Miêu tả chức năng](#miêu-tả-chức-năng) 18**
>
> **[3.6.1.2 Mô tả Use case](#mô-tả-use-case-1) 18**
>
> **[3.6.1.3 Biểu đồ tuần tự](#biểu-đồ-tuần-tự-2) 20**
>
> **[3.6.1.4 Biểu đồ hoạt động](#biểu-đồ-hoạt-động-2) 21**
>
> **[3.6.1.5 Biểu đồ thực thể quan hệ (ERD)/ Biểu đồ lớp](#biểu-đồ-thực-thể-quan-hệ-erd-biểu-đồ-lớp-2) 22**
>
> **[3.6.1.6 Giao diện minh họa](#giao-diện-minh-họa-2) 23**
>
> **[Giao diện trang hiển thị danh sách lớp học](#giao-diện-trang-hiển-thị-danh-sách-lớp-học) 23**
>
> **[Giao diện phần tìm kiếm nâng cao](#giao-diện-phần-tìm-kiếm-nâng-cao) 24**
>
> **[Giao diện in](#giao-diện-in) 25**
>
> **[Giao diện thêm mới lớp học](#giao-diện-thêm-mới-lớp-học) 26**
>
> **[Chỉnh sửa thông tin lớp học](#chỉnh-sửa-thông-tin-lớp-học) 26**
>
> **[Xoá lớp học](#xoá-lớp-học) 26**
>
> **[Xem chi tiết lớp học](#xem-chi-tiết-lớp-học) 27**
>
> **[Để xem chi tiết lớp học, người dùng nhấn vào ID của từng lớp học, khi đó hiện lên các tab thông tin khác nhau liên quan đến lớp học.](#để-xem-chi-tiết-lớp-học-người-dùng-nhấn-vào-id-của-từng-lớp-học-khi-đó-hiện-lên-các-tab-thông-tin-khác-nhau-liên-quan-đến-lớp-học.) 27**

**[4. Nonfunctional Requirements](#nonfunctional-requirements) 1**

> **[4.1 Performance Requirements](#performance-requirements) 1**
>
> **[4.2 Safety Requirements](#safety-requirements) 1**
>
> **[4.3 Security Requirements](#security-requirements) 1**
>
> **[4.4 Software Quality Attributes](#software-quality-attributes) 1**

**[5. Other Requirements](#other-requirements) 1**

**Revision History**

|          |          |             |             |
|----------|----------|-------------|-------------|
| **Name** | **Date** | **Changes** | **Version** |
|          |          |             |             |
|          |          |             |             |

# Introduction

## Purpose 

*\<Identify the product whose software requirements are specified in this document, including the revision or release number. Describe the scope of the product that is covered by this SRS, particularly if this SRS describes only part of the system or a single subsystem.\>*

## Document Conventions

*\<Describe any standards or typographical conventions that were followed when writing this SRS, such as fonts or highlighting that have special significance. For example, state whether priorities for higher-level requirements are assumed to be inherited by detailed requirements, or whether every requirement statement is to have its own priority.\>*

## Project Scope

*\<Provide a short description of the software being specified and its purpose, including relevant benefits, objectives, and goals. Relate the software to corporate goals or business strategies. If a separate vision and scope document is available, refer to it rather than duplicating its contents here. An SRS that specifies the next release of an evolving product should contain its own scope statement as a subset of the long-term strategic product vision.\>*

### Nghiệp vụ tổng quan

…..

![](./media/image29.png),.,.

….

Các nhóm quy trình/ chức năng cần xây dựng như sau:

- Khảo sát thị trường

- Xây dựng chương trình đào tạo

- Quản lý thư viện tài liệu

- Marketing quảng bá khóa học

- Chăm sóc khách hàng

- Mở lớp học

- Quản lý lớp học

- Quản lý chi phí lớp học

Cụ thể nghiệp vụ của từng quy trình/ chức năng:

### Khảo sát thị trường 

### Xây dựng chương trình đào tạo 

### Quản lý thư viện tài liệu 

### Marketing quảng bá khóa học

### Chăm sóc khách hàng 

### Mở lớp học 

### Quản lý lớp học 

### Quản lý chi phí lớp học 

## References

*\<List any other documents (BRD) or Web addresses to which this SRS refers. These may include user interface style guides, contracts, standards, system requirements specifications, use case documents, or a vision and scope document. Provide enough information so that the reader could access a copy of each reference, including title, author, version number, date, and source or location.\>*

# Overall Description

## Product Perspective

*\<Describe the context and origin of the product being specified in this SRS. For example, state whether this product is a follow-on member of a product family, a replacement for certain existing systems, or a new, self-contained product. If the SRS defines a component of a larger system, relate the requirements of the larger system to the functionality of this software and identify interfaces between the two. A simple diagram that shows the major components of the overall system, subsystem interconnections, and external interfaces can be helpful.\>*

## Product Features

*\<Summarize the major features the product contains or the significant functions that it performs or lets the user perform. Details will be provided in Section 3, so only a high level summary is needed here. Organize the functions to make them understandable to any reader of the SRS. A picture of the major groups of related requirements and how they relate, such as a top level data flow diagram or a class diagram, is often effective.\>*

## User Classes and Characteristics

*\<Identify the various user classes that you anticipate will use this product. User classes may be differentiated based on frequency of use, subset of product functions used, technical expertise, security or privilege levels, educational level, or experience. Describe the pertinent characteristics of each user class. Certain requirements may pertain only to certain user classes. Distinguish the favored user classes from those who are less important to satisfy.\>*

## Operating Environment

*\<Describe the environment in which the software will operate, including the hardware platform, operating system and versions, and any other software components or applications with which it must peacefully coexist.\>*

## **Mô hình triển khai** 

![](./media/image34.png)

## **Mô hình đồng bộ dữ liệu** từ **AD** sang Hệ thống Quản lý trung tâm đào tạo

![](./media/image54.png)

Chức năng cho phép hệ thống AD đăng ký tài khoản mới, thay đổi thông tin tài khoản, xóa tài khoản, đổi mật khẩu tài khoản đồng thời cho phép AD yêu cầu tìm kiếm thông tin tài khoản chi tiết từ server hệ thống quản lý trung tâm anh văn.

### +2.4.2.1 Service Đăng ký tài khoản

**Mô tả chức năng**

Chức năng cho phép AD đăng ký tài khoản mới và gửi yêu cầu xác nhận thông tin tài khoản mới trên server hệ thống quản lý trung tâm.

**Mô tả Use case**

**Biểu đồ tuần tự**

![](./media/image36.jpg)

**Biểu đồ hoạt động**

![](./media/image30.jpg)

**Biểu đồ quan hệ thực thể/ ERD**

**Giao diện minh họa**

<table style="width:100%;">
<colgroup>
<col style="width: 11%" />
<col style="width: 3%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 6%" />
<col style="width: 14%" />
<col style="width: 18%" />
<col style="width: 18%" />
</colgroup>
<tbody>
<tr>
<td colspan="17"><strong>REQUEST PARAM</strong></td>
</tr>
<tr>
<td colspan="5">PATHNAME</td>
<td colspan="12">/quanlyhocvien/themmoihocvien</td>
</tr>
<tr>
<td colspan="5">Method</td>
<td colspan="12">POST</td>
</tr>
<tr>
<td><strong>No</strong></td>
<td colspan="10"><strong>Param</strong></td>
<td><strong>Type</strong></td>
<td style="text-align: center;"><strong>Duplicate</strong></td>
<td style="text-align: center;"><strong>Mandatory</strong></td>
<td style="text-align: center;"><strong>Sample value</strong></td>
<td><strong>Description</strong></td>
<td><strong>Remark</strong></td>
</tr>
<tr>
<td style="text-align: right;">1</td>
<td>tenhocvien</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td>string</td>
<td></td>
<td>O</td>
<td>"Nguyễn Văn An"</td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;">2</td>
<td>gioitinh</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td>"nam"</td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;">3</td>
<td>ngaysinh</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td>date</td>
<td></td>
<td>O</td>
<td>"2022/4/5"</td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;">4</td>
<td>diachi</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td>string</td>
<td></td>
<td></td>
<td>"Hoàng Mai, Hà Nội"</td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;">5</td>
<td>email</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td>string</td>
<td></td>
<td>O</td>
<td><u>annv@gmail.com</u></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;">6</td>
<td>sodienthoai</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td>number</td>
<td></td>
<td>O</td>
<td>"0967546877"</td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;">7</td>
<td>khoahoc</td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td>string</td>
<td></td>
<td>O</td>
<td>"TOEIC Beginner"</td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 35%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 0%" />
<col style="width: 49%" />
</colgroup>
<tbody>
<tr>
<td colspan="17"><strong>REQUEST SAMPLE</strong></td>
</tr>
<tr>
<td colspan="16"><p>{</p>
<p>"tenhocvien": ""Nguyễn Văn An",</p>
<p>"gioitinh::"nam",</p>
<p>"ngaysinh":"2022/4/5",</p>
<p>"diachi":"Hoàng Mai, Hà Nội",</p>
<p>"email": "annv@gmail.com",</p>
<p>"sodienthoai":"0967546877",</p>
<p>"khoahoc":"TOEIC Beginner"</p>
<p>}</p></td>
<td></td>
</tr>
</tbody>
</table>

<table style="width:100%;">
<colgroup>
<col style="width: 9%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 0%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 9%" />
<col style="width: 9%" />
<col style="width: 21%" />
<col style="width: 17%" />
<col style="width: 7%" />
</colgroup>
<tbody>
<tr>
<td colspan="25"><strong>RESPONSE FIELD</strong></td>
</tr>
<tr>
<td colspan="5"><strong>FORMAT</strong></td>
<td colspan="20"><strong>JSON</strong></td>
</tr>
<tr>
<td><strong>No</strong></td>
<td colspan="10"><strong>Item New</strong></td>
<td colspan="10"><strong>Item (older)</strong></td>
<td><strong>Type</strong></td>
<td style="text-align: center;"><strong>Duplicate</strong></td>
<td style="text-align: center;"><strong>Mandatory</strong></td>
<td style="text-align: center;"><strong>Sample value</strong></td>
</tr>
<tr>
<td style="text-align: right;"><strong>1</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"><strong>2</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"><strong>3</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"><strong>4</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"><strong>5</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"><strong>6</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"><strong>7</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"><strong>8</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"><strong>9</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"><strong>10</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td colspan="25"><strong>RESPONSE SAMPLE</strong></td>
</tr>
<tr>
<td colspan="25"><p><strong>status: fail</strong></p>
<p><strong>"học viên đã tồn tại và đã đăng kí khóa học trên "</strong></p></td>
</tr>
</tbody>
</table>

### 2.4.2.2 Service Cập nhập thông tin tài khoản

**Mô tả chức năng**

Chức năng cho phép AD cập nhập thông tin tài khoản trên Server Hệ thống quản lý và hệ thống quản lý sẽ trả lại kết quả tài khoản đã cập nhập tại AD.

**Mô tả Use case**

**Biểu đồ tuần tự**

![](./media/image48.png)

**Sơ đồ Use case**

![](./media/image60.png)

**Biểu đồ hoạt động**

**Biểu đồ quan hệ thực thể/ ERD**

**Giao diện minh họa**

### 2.4.2.3 Service Đổi mật khẩu tài khoản

**Mô tả chức năng**

Chức năng cho phép người dùng đổi mật khẩu tài khoản đăng nhập trên Server Hệ thống quản lý và hệ thống quản lý sẽ trả lại kết quả tài khoản đã cập nhập tại AD.

**Mô tả use case**

**Mô tả biểu đồ tuần tự**

![](./media/image43.jpg)

**Mô tả biểu đồ hoạt động**

![](./media/image56.jpg)

**Mô tả biểu đồ quan hệ thực thể**

**Giao diện minh họa**

### 2.4.2.4 Service xóa tài khoản

**Mô tả chức năng**

Chức năng cho phép AD xóa tài khoản trên Server Hệ thống quản lý

**Mô tả use case**

**Mô tả biểu đồ tuần tự**

![](./media/image46.jpg)

**Mô tả biểu đồ hoạt động**

![](./media/image44.jpg)

**Mô tả biểu đồ quan hệ thực thể**

**Giao diện minh họa**

<table>
<colgroup>
<col style="width: 9%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 1%" />
<col style="width: 4%" />
<col style="width: 4%" />
<col style="width: 4%" />
<col style="width: 10%" />
<col style="width: 14%" />
<col style="width: 23%" />
</colgroup>
<tbody>
<tr>
<td colspan="27"><strong>REQUEST PARAM</strong></td>
</tr>
<tr>
<td colspan="5"><strong>PATHNAME</strong></td>
<td colspan="22"><strong>/quanlyhocvien/xoahocvien</strong></td>
</tr>
<tr>
<td colspan="5"><strong>Method</strong></td>
<td colspan="22"><strong>DELETE</strong></td>
</tr>
<tr>
<td><strong>No</strong></td>
<td colspan="10"><strong>Param</strong></td>
<td colspan="10"><strong>Param (older)</strong></td>
<td><strong>Type</strong></td>
<td style="text-align: center;"><strong>Duplicate</strong></td>
<td style="text-align: center;"><strong>Mandatory</strong></td>
<td style="text-align: center;"><strong>Sample value</strong></td>
<td><strong>Description</strong></td>
<td><strong>Remark</strong></td>
</tr>
<tr>
<td style="text-align: right;"><strong>1</strong></td>
<td colspan="10"><strong>mahocvien</strong></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td><strong>"1"</strong></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td colspan="27"><strong>REQUEST SAMPLE</strong></td>
</tr>
<tr>
<td colspan="26"></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td colspan="27"><strong>RESPONSE FIELD</strong></td>
</tr>
<tr>
<td colspan="5"><strong>FORMAT</strong></td>
<td colspan="22"><strong>JSON</strong></td>
</tr>
<tr>
<td><strong>No</strong></td>
<td colspan="10"><strong>Item New</strong></td>
<td colspan="10"><strong>Item (older)</strong></td>
<td><strong>Type</strong></td>
<td style="text-align: center;"><strong>Duplicate</strong></td>
<td style="text-align: center;"><strong>Mandatory</strong></td>
<td style="text-align: center;"><strong>Sample value</strong></td>
<td><strong>Description</strong></td>
<td><strong>Remark</strong></td>
</tr>
<tr>
<td style="text-align: right;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: right;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td colspan="27"><strong>RESPONSE SAMPLE</strong></td>
</tr>
<tr>
<td colspan="27"><p><strong>status: pass</strong></p>
<p><strong>Xóa thành công</strong></p></td>
</tr>
</tbody>
</table>

### 2.4.2.5 Service tìm kiếm tài khoản (tìm kiếm nhanh)

**Mô tả chức năng**

Chức năng cho phép hệ thống AD tìm kiếm nhanh tài khoản qua Server Hệ thống quản lý trung tâm anh văn

**Mô tả use case**

**Mô tả biểu đồ tuần tự**

![](./media/image41.jpg)

**Mô tả biểu đồ hoạt động**

![](./media/image53.jpg)

**Giao diện minh họa**

### 2.4.2.6 Service tìm kiếm tài khoản theo các thông tin chi tiết

**Mô tả chức năng**

Chức năng cho phép hệ thống AD tìm kiếm tài khoản theo các thông tin chi tiết qua Sưe Quản lý trung tâm anh văn.

**Mô tả use case**

**Mô tả biểu đồ tuần tự**

![](./media/image52.jpg)

**Mô tả biểu đồ hoạt động**

![](./media/image49.jpg)

**Mô tả biểu đồ quan hệ thực thể**

**Giao diện minh họa**

## 2.4.3 Mô hình đồng bộ dữ liệu từ hệ thống quản lý trung tâm đào tạo sang AD 

![](./media/image58.png)

### 2.4.3.1 Service Cập nhật thông tin tài khoản

**Mô tả chức năng**

Chức năng cho phép hệ thống quản lý trung tâm tiếng anh cập nhật thông tin tài khoản qua hệ thống AD

**Mô tả use case**

**Mô tả biểu đồ tuần tự**

![](./media/image50.jpg)

**Mô tả biểu đồ hoạt động**

![](./media/image57.jpg)

**Mô tả biểu đồ quan hệ thực thể**

**Giao diện minh họa**

### 2.4.3.2 Service Đổi mật khẩu tài khoản

**Mô tả chức năng**

Chức năng cho phép hệ thống ECMS đổi mật khẩu tài khoản qua hệ thống AD

**Mô tả use case**

**Mô tả biểu đồ tuần tự**

![](./media/image55.jpg)

**Mô tả biểu đồ hoạt động**

![](./media/image59.jpg)

**Mô tả biểu đồ quan hệ thực thể**

**Giao diện minh họa**

### 2.4.3.3 Service Xóa tài khoản

**Mô tả chức năng**

Chức năng cho phép hệ thống quản lý trung tâm anh văn xóa tài khoản qua hệ thống AD

**Mô tả use case**

**Mô tả biểu đồ tuần tự**

![](./media/image25.jpg)

**Mô tả biểu đồ hoạt động**

![](./media/image26.jpg)

**Mô tả biểu đồ quan hệ thực thể**

**Giao diện minh họa**

### 2.4.3.4 Service tìm kiếm tài khoản (tìm kiếm nhanh)

**Mô tả chức năng**

Chức năng cho phép hệ thống ESMC tìm kiếm nhanh tài khoản qua Server AD

**Mô tả use case**

**Mô tả biểu đồ tuần tự**

![](./media/image39.jpg)

**Mô tả biểu đồ hoạt động**

![](./media/image23.jpg)

**Mô tả biểu đồ quan hệ thực thể**

**Giao diện minh họa**

### \

### 2.4.3.5 Service tìm kiếm tài khoản theo thông tin chi tiết

**Mô tả chức năng**

Chức năng cho phép hệ thống quản lý trung tâm tiếng anh tìm kiếm tài khoản theo thông tin chi tiết qua hệ thống AD

**Mô tả use case**

**Mô tả biểu đồ tuần tự**

![](./media/image61.jpg)

**Mô tả biểu đồ hoạt động**

![](./media/image31.jpg)

**Mô tả biểu đồ quan hệ thực thể**

**Giao diện minh họa**

## Assumptions and Dependencies

*\<List any assumed factors (as opposed to known facts) that could affect the requirements stated in the SRS. These could include third-party or commercial components that you plan to use, issues around the development or operating environment, or constraints. The project could be affected if these assumptions are incorrect, are not shared, or change. Also identify any dependencies the project has on external factors, such as software components that you intend to reuse from another project, unless they are already documented elsewhere (for example, in the vision and scope document or the project plan).\>*

# Functional Requirements

*\<This template illustrates organizing the functional requirements for the product by system features, the major services provided by the product. You may prefer to organize this section by use case, mode of operation, user class, object class, functional hierarchy, or combinations of these, whatever makes the most logical sense for your product.\>*

## Đăng nhập hệ thống

## Quản lý học viên 

Người dùng được phần quyền truy cập quản lý học viên bằng cách xem được danh sách học viên, thông tin chi tiết học viên đồng thời có thể chỉnh sửa, xóa thông tin học viên, tạo thông tin mới và xếp lớp cho học viên

Trong chức năng xem thông tin chi tiết học viên, ngoài những thông tin cá nhân cơ bản của học viên, người dùng còn có thể xem được danh sách khóa học, lớp học đã và đang học của học viên, trạng thái học tập và bảo lưu của học viên. Đối với những lớp học đang theo học, người dùng có thể xem được đánh giá của giảng viên/trợ giảng về học viên hoặc đánh giá của học viên về giảng viên/trợ giảng.

### Xem danh sách học viên 

#### Mô tả chức năng

Người dùng có thể xem danh sách học viên, tìm kiếm thông tin chi tiết học viên và chuyển trang hiển thị bản ghi

#### Mô tả Usecase

<table>
<colgroup>
<col style="width: 9%" />
<col style="width: 8%" />
<col style="width: 20%" />
<col style="width: 10%" />
<col style="width: 34%" />
<col style="width: 5%" />
<col style="width: 9%" />
<col style="width: 0%" />
</colgroup>
<tbody>
<tr>
<td rowspan="2" style="text-align: center;"><strong>STT</strong></td>
<td rowspan="2" style="text-align: center;"><strong>Chức năng</strong></td>
<td rowspan="2" style="text-align: center;"><strong>Mô tả</strong></td>
<td colspan="4" style="text-align: center;"><strong>Use-Case Description</strong></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;">Tác nhân chính (Main Actor)</td>
<td style="text-align: center;">Tác nhân phụ (Sub-Actors)</td>
<td style="text-align: center;">Thao tác/ giao dịch/ Transaction</td>
<td style="text-align: center;">Phân loại</td>
<td style="text-align: center;">Độ phức tạp</td>
</tr>
<tr>
<td style="text-align: center;">B.1</td>
<td style="text-align: center;">Xem danh sách học viên </td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><ol type="1">
<li><p>Nhân viên phòng Đào tạo,</p></li>
<li><p>Nhân viên Chăm sóc khách hàng,</p></li>
<li><p>Nhân viên Hỗ trợ đào tạo</p></li>
</ol></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">B</td>
<td style="text-align: center;">TB</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">Vào trang chủ, người dùng chọn mục quản lý học viên.<br />
Hệ thống gửi lệnh truy cập danh sách học viên và trả kết quả hiển thị </td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">Người dùng nhấn chọn tìm kiếm nhanh/ tìm kiếm nâng cao <br />
Hệ thống hiển thị form tìm kiếm tương đương với lựa chọn (tìm kiếm nhanh, tìm kiếm nâng cao)</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">Người dùng nhập thông tin cần tìm kiếm và nhấn "tìm kiếm" <br />
Hệ thống kiểm tra dữ liệu người dùng nhập vào <br />
Hệ thống truy vấn dữ liệu theo điều kiện tìm kiếm <br />
Hệ thống khởi tạo trang hiển thị kết quả tìm kiếm </td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">Người dùng thay đổi số bản ghi muốn hiển thị trên một trang <br />
Hệ thống kiểm tra dữ liệu nhập vào <br />
Hệ thống phân trang lại và hiển thị lại trang danh sách </td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">Người dùng nhấp chuyển trang (trang đầu tiên, trang cuối cùng, trang sau, trang trước đó hoặc chỉ định trang muốn hiển thị)<br />
Hệ thống kiểm tra dữ liệu nhập vào <br />
Hệ thống phân trang lại và hiển thị lại trang danh sách </td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
</tr>
</tbody>
</table>

#### Biểu đồ tuần tự

![](./media/image27.jpg)

#### Biểu đồ hoạt động

![](./media/image47.jpg)

#### Biểu đồ thực thể quan hệ (ERD)/ Biểu đồ lớp

![](./media/image28.png)

#### \

#### Giao diện minh họa

![](./media/image32.png)

- Tìm kiếm nhanh: người dùng nhập từ khóa tìm kiếm, sau đó nhấn nút ![](./media/image16.png)

- Download: ![](./media/image4.png) chức năng cho phép người dùng tải dữ liệu

- In ![](./media/image1.png)

- Phân trang hiển thị:

  - Chọn số dòng dữ liệu sẽ hiển thị trên mỗi trang: người dùng nhập số trong phần ![](./media/image15.png), danh sách sẽ hiển thị số dòng dữ liệu tương ứng trong một trang

  - Nhảy sang trang thứ n: người dùng nhập số trang muốn hiểu thị trong ![](./media/image5.png)để danh sách hiển thị tương ứng với số thứ tự trang được nhập

  - Về trang trước: người dùng ấn nút ![](./media/image13.png) để về danh sách hiển thị ở trang trước

  - Về trang đầu: người dùng ấn nút ![](./media/image2.png)để danh sách hiển thị ở trang đầu tiên

  - Sang trang tiếp theo: người dùng ấn nút ![](./media/image17.png) để sang danh sách hiển thị ở trang tiếp theo

  - Tới trang cuối cùng: người dùng ấn nút ![](./media/image19.png) để danh sách hiển thị theo thứ tự cuối cùng

- Nút “Add New", cho phép thêm dữ liệu. Chi tiết chức năng xem trong mục “[<u>Tạo thông tin học viên mới</u>](#tạo-thông-tin-học-viên-mới)”

- Nút “Delete", cho phép xóa một hoặc nhiều dòng dữ liệu. Chi tiết chức năng xem trong mục “[<u>Xoá thông tin học viên</u>](#xóa-thông-tin-học-viên)”, cụ thể, hệ thống cho phép xoá ở hai chế độ:

  - Xoá một dòng

  - Xoá nhiều dòng.

- Nút cập nhật/ hiệu chỉnh thông tin học viên ![](./media/image18.png): cho phép người dùng chỉnh sửa thông tin dữ liệu tương ứng. Chi tiết chức năng xem trong mục “[<u>Chỉnh sửa thông tin học viên</u>](#chỉnh-sửa-thông-tin-học-viên)”

- Khi người dùng nhấp chuột vào nút![](./media/image14.png) , hệ thống sẽ ẩn đi form Tìm kiếm nhanh, thay vào vùng của form tìm kiếm nhanh là form Tìm kiếm nâng cao. Với thiết kế của Form tìm kiếm nâng cao như sau:

![](./media/image7.png)

- Ràng buộc dữ liệu giữa các thông tin: Tỉnh/ Thành phố với Quận/ Huyện và Xã/ Phường: …

- Khi người dùng nhấp chuột vào nút ![](./media/image10.png), sẽ ẩn đi form tìm kiếm nâng cao và hiển thị lại form tìm kiếm nhanh.

### Xem thông tin chi tiết học viên

#### Mô tả chức năng

Người dùng xem thông tin chi tiết học viên, bao gồm: thông tin cá nhân, lịch sử khóa học/lớp học, điểm danh, đánh giá của giảng viên/trợ giảng, kết quả kiểm tra, học phí, bảo lưu.

#### Mô tả Use case

<table>
<colgroup>
<col style="width: 6%" />
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 33%" />
<col style="width: 6%" />
<col style="width: 6%" />
</colgroup>
<tbody>
<tr>
<td rowspan="2" style="text-align: center;"><strong>STT</strong></td>
<td rowspan="2" style="text-align: center;"><strong>Chức năng</strong></td>
<td rowspan="2" style="text-align: center;"><strong>Mô tả</strong></td>
<td colspan="4" style="text-align: center;"><strong>Use-Case Description</strong></td>
<td></td>
</tr>
<tr>
<td style="text-align: center;">Tác nhân chính (Main Actor)</td>
<td style="text-align: center;">Tác nhân phụ (Sub-Actors)</td>
<td style="text-align: center;">Thao tác/ giao dịch/ Transaction</td>
<td style="text-align: center;">Phân loại</td>
<td>Độ phức tạp</td>
</tr>
<tr>
<td style="text-align: center;">B.1.1</td>
<td style="text-align: center;">Xem thông tin chi tiết học viên</td>
<td style="text-align: center;"><p>Người dùng đang đứng ở trang danh sách học viên, đã thực hiện tìm kiếm.</p>
<p>Người dùng chỉ cẩn chọn học viên muốn thao tác</p></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">B</td>
<td>TB</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Người dùng nhấn và TAB Xem danh sách khoá học/ lớp học đã học</p>
<p>Hệ thống hiển thị danh sách các khoá học/ lớp học mà học viên đã học</p></td>
<td style="text-align: center;"></td>
<td></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Người dùng nhấn và TAB Xem lớp học hiện tại đang theo học</p>
<p>Hệ thống hiển thị thông tin lớp học hiện tại đang theo học : chi tiết các buổi học , có điểm danh hay không, đánh giá của giáo viên và trợ giảng về học viên trong buổi học đó , đánh giá của học viên về giáo viên/ trợ giảng trong buổi học đó</p></td>
<td style="text-align: center;"></td>
<td></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Người dùng nhấn và TAB Xem thông tin chăm sóc khách hàng, kết quả làm. bài kiểm tra</p>
<p>Hệ thống hiển thị danh sách thông tin chăm sóc khách hàng, kết quả làm. bài kiểm tra</p></td>
<td style="text-align: center;"></td>
<td></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Người dùng nhấn và TAB Xem thông tin đóng học phí của học viên</p>
<p>Hệ thống hiển thị danh sách các lần đóng học phí của học viên</p></td>
<td style="text-align: center;"></td>
<td></td>
</tr>
</tbody>
</table>

#### Biểu đồ tuần tự

![](./media/image9.jpg)

#### \

#### Biểu đồ hoạt động

#### Biểu đồ thực thể quan hệ (ERD)/ Biểu đồ lớp

![](./media/image22.png)

#### Giao diện minh họa

### Chỉnh sửa thông tin học viên 

**Mô tả chức năng**

Cho phép người dùng chỉnh sửa thông tin học viên

**Mô tả use case**

<table style="width:100%;">
<colgroup>
<col style="width: 5%" />
<col style="width: 18%" />
<col style="width: 15%" />
<col style="width: 6%" />
<col style="width: 12%" />
<col style="width: 25%" />
<col style="width: 6%" />
<col style="width: 9%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: center;">B.1.2</td>
<td>Chỉnh sửa thông tin học viên</td>
<td><p>Người dùng đang đứng ở trang danh sách học viên, đã thực hiện tìm kiếm.</p>
<p>Người dùng chỉ cẩn chọn học viên muốn thao tác</p></td>
<td></td>
<td></td>
<td></td>
<td>B</td>
<td>ĐG</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td><p>Người dùng nhấn nút "sửa" trên bản ghi/ dữ liệu cần chỉnh sửa thông tin</p>
<p>Hệ thống kiểm tra dữ liệu người dùng nhâp vào có hợp lệ hay không</p>
<p>Hệ thống truy vấn thông tin từ CSDL, tương úng với dữ liệu nhập vào</p>
<p>Hệ thống hiển thị trang hiệu chỉnh thông tin</p></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td><p>Người dùng nhập thông tin cần thay đổi, chọn lưu thông tin đã chỉnh sửa</p>
<p>Hệ thống yêu cầu người dùng xác nhận thao tác lưu</p></td>
<td></td>
<td></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td></td>
<td></td>
<td></td>
<td></td>
<td><p>Người dùng xác nhận thao tác lưu</p>
<p>Hệ thống cập nhâp thông tin vào CSDL</p>
<p>Hệ thống thông báo kết quả cập nhật và cập nhật lại trang hiển thị danh sách</p></td>
<td></td>
<td></td>
</tr>
</tbody>
</table>

**Biểu đồ tuần tự**

![](./media/image12.jpg)

**Biểu đồ hoạt động**

**Biểu đồ thực thể quan hệ**

![](./media/image22.png)

**Giao diện minh họa**

![](./media/image6.png)

### Xóa thông tin học viên

**Mô tả chức năng**

**Mô tả use case**

**Biểu đồ tuần tự**

**Biểu đồ hoạt động**

**Biểu đồ thực thể quan hệ**

![](./media/image22.png)

**Giao diện minh họa**

### ![](./media/image11.jpg) 

### Tạo thông tin học viên mới 

### Bảo lưu học viên

### Chuyển đổi trạng thái học viên

### Xếp lớp cho học viên

### Lịch sử / quá trình học

### Xem đánh giá của học viên

## \[Module 1\]

### Description and Priority

*\<Provide a short description of the feature and indicate whether it is of High, Medium, or Low priority. You could also include specific priority component ratings, such as benefit, penalty, cost, and risk (each rated on a relative scale from a low of 1 to a high of 9).\>*

### Functional Requirements

*\<Itemize the detailed functional requirements associated with this feature. These are the software capabilities that must be present in order for the user to carry out the services provided by the feature, or to execute the use case. Include how the product should respond to anticipated error conditions or invalid inputs. Requirements should be concise, complete, unambiguous, verifiable, and necessary. Use “TBD” as a placeholder to indicate when necessary information is not yet available.\>*

*\<Each requirement should be uniquely identified with a sequence number or a meaningful tag of some kind.\>*

FR-001:

FR-002:

## \[Module 2\] (and so on)

## **.**

## **Quản lý lớp học**

Người dùng được phần quyền truy cập quản lý lớp học bằng cách xem được danh sách lớp học, thông tin chi tiết lớp học đồng thời có thể chỉnh sửa, xóa thông tin, tạo thông tin mới và xem được đánh giá của lớp học.

## Xem danh sách lớp học

### Miêu tả chức năng

Trong chức năng xem danh sách lớp học, người dùng có thể xem, tìm kiếm cơ bản và tìm kiếm nâng cao lớp học, người dùng còn có thể xem chi tiết thông tin của lớp bao gồm mô tả, danh sách tiết học, tài liệu, danh sách học viên chi tiết cũng như chỉnh sửa được thông tin đó.

### Mô tả Use case

<table>
<colgroup>
<col style="width: 6%" />
<col style="width: 16%" />
<col style="width: 16%" />
<col style="width: 7%" />
<col style="width: 7%" />
<col style="width: 33%" />
<col style="width: 6%" />
<col style="width: 6%" />
</colgroup>
<tbody>
<tr>
<td rowspan="2" style="text-align: center;"><strong>STT</strong></td>
<td rowspan="2" style="text-align: center;"><strong>Chức năng</strong></td>
<td rowspan="2" style="text-align: center;"><strong>Mô tả</strong></td>
<td colspan="4" style="text-align: center;"><strong>Use-Case Description</strong></td>
<td></td>
</tr>
<tr>
<td style="text-align: center;">Tác nhân chính (Main Actor)</td>
<td style="text-align: center;">Tác nhân phụ (Sub-Actors)</td>
<td style="text-align: center;">Thao tác/ giao dịch/ Transaction</td>
<td style="text-align: center;">Phân loại</td>
<td>Độ phức tạp</td>
</tr>
<tr>
<td style="text-align: center;">G.1</td>
<td style="text-align: center;">Xem danh sách lớp học</td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;">B</td>
<td>TB</td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Vào trang chủ, người dùng chọn mục quản lý lớp học.</p>
<p>Hệ thống gửi lệnh truy cập danh sách lớp học và trả kết quả hiển thị</p></td>
<td style="text-align: center;"></td>
<td></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Người dùng nhấn chọn tìm kiếm nhanh/ tìm kiếm nâng cao</p>
<p>Hệ thống hiển thị form tìm kiếm tương đương với lựa chọn (tìm kiếm nhanh, tìm kiếm nâng cao)</p></td>
<td style="text-align: center;"></td>
<td></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Người dùng nhập thông tin cần tìm kiếm và nhấn "tìm kiếm"</p>
<p>Hệ thống kiểm tra dữ liệu người dùng nhập vào</p>
<p>Hệ thống truy vấn dữ liệu theo điều kiện tìm kiếm</p>
<p>Hệ thống khởi tạo trang hiển thị kế quả tìm kiếm</p></td>
<td style="text-align: center;"></td>
<td></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Người dùng thay đổi số bản ghi muốn hiển thị trên một trang</p>
<p>Hệ thống kiểm tra dữ liệu nhập vào</p>
<p>Hệ thống phân trang lại và hiển thị lại trang danh sách</p></td>
<td style="text-align: center;"></td>
<td></td>
</tr>
<tr>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"></td>
<td style="text-align: center;"><p>Người dùng nhấp chuyển trang (trang đầu tiên, trang cuối cùng, trang sau, trang trước đó hoặc chỉ định trang muốn hiển thị)</p>
<p>Hệ thống kiểm tra dữ liệu nhập vào</p>
<p>Hệ thống phân trang lại và hiển thị lại trang danh sách</p></td>
<td style="text-align: center;"></td>
<td></td>
</tr>
</tbody>
</table>

### \

### 

### Biểu đồ tuần tự

![](./media/image38.png)

### \

### Biểu đồ hoạt động

![](./media/image37.png)

### \

### Biểu đồ thực thể quan hệ (ERD)/ Biểu đồ lớp

![](./media/image45.png)

### \

### Giao diện minh họa 

### Giao diện trang hiển thị danh sách lớp học

![](./media/image42.png)

- Tìm kiếm nhanh: người dùng nhập từ khóa tìm kiếm, sau đó nhấn nút ![](./media/image16.png)

- Download: ![](./media/image4.png) chức năng cho phép người dùng tải dữ liệu

- In ![](./media/image1.png)

- Phân trang hiển thị:

  - Chọn số dòng dữ liệu sẽ hiển thị trên mỗi trang: người dùng nhập số trong phần ![](./media/image15.png), danh sách sẽ hiển thị số dòng dữ liệu tương ứng trong một trang

  - Nhảy sang trang thứ n: người dùng nhập số trang muốn hiểu thị trong ![](./media/image5.png)để danh sách hiển thị tương ứng với số thứ tự trang được nhập

  - Về trang trước: người dùng ấn nút ![](./media/image13.png) để về danh sách hiển thị ở trang trước

  - Về trang đầu: người dùng ấn nút ![](./media/image2.png)để danh sách hiển thị ở trang đầu tiên

  - Sang trang tiếp theo: người dùng ấn nút ![](./media/image17.png) để sang danh sách hiển thị ở trang tiếp theo

  - Tới trang cuối cùng: người dùng ấn nút ![](./media/image19.png) để danh sách hiển thị theo thứ tự cuối cùng

- Nút “Add New", cho phép thêm dữ liệu. Chi tiết chức năng xem trong mục “<u>Tạo thông tin lớp học mới</u>”

- Nút “Delete", cho phép xóa một hoặc nhiều dòng dữ liệu. Chi tiết chức năng xem trong mục “<u>Xoá thông tin lớp học</u>”, cụ thể, hệ thống cho phép xoá ở hai chế độ:

  - Xoá một dòng

  - Xoá nhiều dòng.

- Nút cập nhật/ hiệu chỉnh thông tin lớp học ![](./media/image18.png): cho phép người dùng chỉnh sửa thông tin dữ liệu tương ứng. Chi tiết chức năng xem trong mục “[<u>Chỉnh sửa thông tin học viên</u>](#chỉnh-sửa-thông-tin-học-viên)”

- Khi người dùng nhấp chuột vào nút![](./media/image14.png) , hệ thống sẽ ẩn đi form Tìm kiếm nhanh, thay vào vùng của form tìm kiếm nhanh là form Tìm kiếm nâng cao. Với thiết kế của Form tìm kiếm nâng cao như sau:

### 

### Giao diện phần tìm kiếm nâng cao

![](./media/image24.png)

### 

### \

### Giao diện in 

![](./media/image21.png)

### \

### Giao diện thêm mới **lớp học**

![](./media/image51.png)

### **Chỉnh sửa thông tin lớp học**

### Xoá lớp học

Để xoá lớp học cần nhấn các button xoá tại hàng danh sách hoặc đánh dấu tick vô cột đầu tiên để chọn lựa nhiều lớp cần xoá rồi nhấn nút delete góc phải màn hình.

![](./media/image35.png)

Khi đó hiện ra popup xác nhận người dùng có chắc chắn muốn xoá đi không, nếu có thì nhấn “đồng ý”, để trở lại nhấn “huỷ”.

![](./media/image40.png)

### Xem chi tiết lớp học

### Để xem chi tiết lớp học, người dùng nhấn vào ID của từng lớp học, khi đó hiện lên các tab thông tin khác nhau liên quan đến lớp học.

![](./media/image33.png)

![](./media/image20.png)![](./media/image8.png)

![](./media/image3.png)

# Nonfunctional Requirements

## Performance Requirements

*\<If there are performance requirements for the product under various circumstances, state them here and explain their rationale, to help the developers understand the intent and make suitable design choices. Specify the timing relationships for real time systems. Make such requirements as specific as possible. You may need to state performance requirements for individual functional requirements or features.\>*

## Safety Requirements

*\<Specify those requirements that are concerned with possible loss, damage, or harm that could result from the use of the product. Define any safeguards or actions that must be taken, as well as actions that must be prevented. Refer to any external policies or regulations that state safety issues that affect the product’s design or use. Define any safety certifications that must be satisfied.\>*

## Security Requirements

*\<Specify any requirements regarding security or privacy issues surrounding use of the product or protection of the data used or created by the product. Define any user identity authentication requirements. Refer to any external policies or regulations containing security issues that affect the product. Define any security or privacy certifications that must be satisfied.\>*

## Software Quality Attributes

*\<Specify any additional quality characteristics for the product that will be important to either the customers or the developers. Some to consider are: adaptability, availability, correctness, flexibility, interoperability, maintainability, portability, reliability, reusability, robustness, testability, and usability. Write these to be specific, quantitative, and verifiable when possible. At the least, clarify the relative preferences for various attributes, such as ease of use over ease of learning.\>*

# Other Requirements

*\<Define any other requirements not covered elsewhere in the SRS. This might include database requirements, internationalization requirements, legal requirements, reuse objectives for the project, and so on. Add any new sections that are pertinent to the project.\>*

**Appendix A: Glossary**

*\<Define all the terms necessary to properly interpret the SRS, including acronyms and abbreviations. You may wish to build a separate glossary that spans multiple projects or the entire organization, and just include terms specific to a single project in each SRS.\>*

**Appendix B: Analysis Models**

*\<Optionally, include any pertinent analysis models, such as data flow diagrams, class diagrams, state-transition diagrams, or entity-relationship diagrams*.\>

**Appendix C: Issues List**

*\< This is a dynamic list of the open requirements issues that remain to be resolved, including TBDs, pending decisions, information that is needed, conflicts awaiting resolution, and the like.\>*
