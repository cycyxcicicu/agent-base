# Danh Mục Tên Định Danh Icon Chuẩn Của Draw.io (Stencils & Shapes Index)

> **Loại: tham khảo.** Hướng dẫn công cụ vẽ sơ đồ, không phải nguồn luật. Khi khác `AGENTS.md`, vai trò hoặc `agents/protocols/` thì theo các nơi đó (`agents/protocols/source-precedence.md`).
> **Khác với chuẩn:** Chỉ là bảng tra tên shape khi viết `style`; không quy định loại sơ đồ nào dùng icon nào. Chuẩn nội dung sơ đồ: `../srs/chuan-ve-so-do.md`; công cụ nguồn của dự án: `quy-uoc-draw-io-va-archify.md`; phần chữ đi kèm sơ đồ: `mo-ta-hoat-dong-so-do.md`.

> **Mã định danh:** `drawio-icons-index`  
> **Chuyên mục:** Kiến trúc, Trực quan hóa & Vẽ sơ đồ tự động  
> **Trạng thái:** `draft` (Chờ nghiệm thu con người)  

Trong Draw.io, các biểu tượng và hình dáng được gọi thông qua thuộc tính `shape=mxgraph.<thư_viện>.<tên_icon>` hoặc đường dẫn file vector nội bộ `image=img/lib/...`. Dưới đây là bảng tra cứu các icon thông dụng nhất cho kiến trúc phần mềm và hạ tầng điện toán đám mây.

---

## 1. Amazon Web Services (AWS 2024 / AWS4)
> **Cú pháp:** `shape=mxgraph.aws4.<tên_icon>`

| Tên định danh Shape | Dịch vụ tương ứng | Nhóm dịch vụ |
|---|---|---|
| `mxgraph.aws4.api_gateway` | API Gateway | Network & Routing |
| `mxgraph.aws4.application_load_balancer` | Application Load Balancer (ALB) | Network |
| `mxgraph.aws4.cloudfront` | CloudFront (CDN) | Network |
| `mxgraph.aws4.route_53` | Route 53 (DNS) | Network |
| `mxgraph.aws4.vpc` | Virtual Private Cloud | Network |
| `mxgraph.aws4.ecs` | Elastic Container Service (Microservices) | Compute |
| `mxgraph.aws4.eks` | Elastic Kubernetes Service | Compute |
| `mxgraph.aws4.ec2` | Elastic Compute Cloud (VM) | Compute |
| `mxgraph.aws4.lambda_function` | AWS Lambda (Serverless) | Compute |
| `mxgraph.aws4.rds_postgresql` | RDS PostgreSQL Database | Database |
| `mxgraph.aws4.rds_mysql` | RDS MySQL Database | Database |
| `mxgraph.aws4.dynamodb` | DynamoDB (NoSQL) | Database |
| `mxgraph.aws4.elasticache_redis` | ElastiCache Redis | Database / Cache |
| `mxgraph.aws4.s3` | Simple Storage Service (S3) | Storage |
| `mxgraph.aws4.sqs` | Simple Queue Service (Message Queue) | Integration |
| `mxgraph.aws4.sns` | Simple Notification Service | Integration |
| `mxgraph.aws4.mq` | Amazon MQ (RabbitMQ / ActiveMQ) | Integration |
| `mxgraph.aws4.cognito` | Amazon Cognito (Xác thực / Auth) | Security |
| `mxgraph.aws4.cloudwatch` | CloudWatch (Giám sát / Logging) | Management |
| `mxgraph.aws4.mobile` | Client Mobile / Smartphone | Client |
| `mxgraph.aws4.user` | Người dùng (End-User) | General |

---

## 2. Google Cloud Platform (GCP2)
> **Cú pháp:** `shape=mxgraph.gcp2.<tên_icon>`

| Tên định danh Shape | Dịch vụ tương ứng | Nhóm dịch vụ |
|---|---|---|
| `mxgraph.gcp2.compute_engine` | Google Compute Engine (VM) | Compute |
| `mxgraph.gcp2.kubernetes_engine` | Google Kubernetes Engine (GKE) | Compute |
| `mxgraph.gcp2.cloud_run` | Cloud Run (Serverless Container) | Compute |
| `mxgraph.gcp2.cloud_functions` | Cloud Functions | Compute |
| `mxgraph.gcp2.cloud_sql` | Cloud SQL (PostgreSQL/MySQL) | Database |
| `mxgraph.gcp2.cloud_spanner` | Cloud Spanner (Global Relational) | Database |
| `mxgraph.gcp2.bigquery` | BigQuery (Data Warehouse) | Analytics |
| `mxgraph.gcp2.cloud_storage` | Cloud Storage (Buckets) | Storage |
| `mxgraph.gcp2.pub_sub` | Cloud Pub/Sub (Event Streaming) | Integration |
| `mxgraph.gcp2.cloud_load_balancing` | Cloud Load Balancing | Network |
| `mxgraph.gcp2.cloud_armor` | Cloud Armor (WAF / DDoS) | Security |

---

## 3. Kubernetes (K8s)
> **Cú pháp:** `shape=mxgraph.kubernetes.<tên_icon>`

| Tên định danh Shape | Khái niệm Kubernetes |
|---|---|
| `mxgraph.kubernetes.pod` | Pod đơn lẻ |
| `mxgraph.kubernetes.deployment` | Deployment |
| `mxgraph.kubernetes.service` | K8s Service (ClusterIP/NodePort) |
| `mxgraph.kubernetes.ingress` | Ingress Controller |
| `mxgraph.kubernetes.node` | Worker Node |
| `mxgraph.kubernetes.control_plane` | K8s Master / Control Plane |
| `mxgraph.kubernetes.configmap` | ConfigMap |
| `mxgraph.kubernetes.secret` | Secret |
| `mxgraph.kubernetes.persistent_volume` | Persistent Volume (PV/PVC) |

---

## 4. Mạng & Hạ Tầng On-Premise (Cisco & General Network)
> **Cú pháp:** `shape=mxgraph.cisco.<nhóm>.<tên_icon>` hoặc `shape=mxgraph.networks.<tên_icon>`

| Tên định danh Shape | Thiết bị mạng |
|---|---|
| `mxgraph.cisco.routers.router` | Bộ định tuyến Router |
| `mxgraph.cisco.switches.switch` | Bộ chuyển mạch Switch L2/L3 |
| `mxgraph.cisco.firewalls.firewall` | Tường lửa Firewall phần cứng |
| `mxgraph.networks.server` | Máy chủ vật lý (Bare-metal Server) |
| `mxgraph.networks.storage` | Hệ thống lưu trữ SAN/NAS |
| `mxgraph.networks.laptop` | Máy tính xách tay Client |

---

## 5. Logo Phần Mềm & Thư Viện Độc Lập
> **Cú pháp:** `image=img/lib/mscae/<tên_file>.svg` hoặc `image=img/lib/atlassian/<tên_file>.svg`

- Docker Container: `image=img/lib/mscae/Docker.svg;`
- Git / GitHub / GitLab: `image=img/lib/mscae/Git.svg;`
- PostgreSQL: Sử dụng `shape=mxgraph.aws4.rds_postgresql;`
- Redis: Sử dụng `shape=mxgraph.aws4.elasticache_redis;`
- RabbitMQ: Sử dụng `shape=mxgraph.aws4.mq;`
- Spring Boot / Java: Thường dùng icon Service Box kèm viền màu `#6DB33F`.
