#!/usr/bin/env python3
"""
tests/test_project_graph.py
Unit tests cho mô-đun Project Architecture Graph Engine.
"""

import unittest
import tempfile
import json
from pathlib import Path

from agent_core.knowledge.project_graph import (
    parse_java_controller,
    parse_java_entity,
    parse_feign_client,
    parse_gateway_routes,
    build_project_graph,
    query_project_graph,
    detect_project_context
)


class TestProjectGraph(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_parse_java_controller(self):
        java_content = """
        package com.example.demo.controller;

        import org.springframework.web.bind.annotation.*;

        // Quản lý người dùng
        @RestController
        @RequestMapping("/api/v1/users")
        public class UserController {

            // Lấy thông tin user
            @GetMapping("/{id}")
            public String getUserById(@PathVariable String id) {
                return id;
            }

            // Tạo mới user
            @PostMapping
            public String createUser(@RequestBody String body) {
                return body;
            }
        }
        """
        controller_file = self.root / "UserController.java"
        controller_file.write_text(java_content, encoding="utf-8")

        endpoints = parse_java_controller(controller_file, self.root, "user-service")
        self.assertEqual(len(endpoints), 2)

        ep1 = endpoints[0]
        self.assertEqual(ep1["http_method"], "GET")
        self.assertEqual(ep1["path"], "/api/v1/users/{id}")
        self.assertEqual(ep1["method_name"], "getUserById")
        self.assertIn("Lấy thông tin user", ep1["description"])

        ep2 = endpoints[1]
        self.assertEqual(ep2["http_method"], "POST")
        self.assertEqual(ep2["path"], "/api/v1/users")
        self.assertEqual(ep2["method_name"], "createUser")

    def test_parse_java_entity(self):
        java_content = """
        package com.example.demo.entity;

        import jakarta.persistence.*;

        @Entity
        @Table(name = "tbl_order")
        public class OrderEntity {
            @Id
            private Long id;

            @Column(name = "order_code")
            private String orderCode;

            @Column(name = "total_amount")
            private Double totalAmount;

            @ManyToOne
            @JoinColumn(name = "customer_id")
            private CustomerEntity customer;
        }
        """
        entity_file = self.root / "OrderEntity.java"
        entity_file.write_text(java_content, encoding="utf-8")

        entity = parse_java_entity(entity_file, self.root, "order-service")
        self.assertIsNotNone(entity)
        self.assertEqual(entity["class_name"], "OrderEntity")
        self.assertEqual(entity["table_name"], "tbl_order")
        self.assertIn("order_code", entity["columns"])
        self.assertIn("total_amount", entity["columns"])
        self.assertEqual(len(entity["relations"]), 1)
        self.assertEqual(entity["relations"][0]["type"], "ManyToOne")
        self.assertEqual(entity["relations"][0]["join_column"], "customer_id")

    def test_parse_gateway_routes(self):
        yml_content = """
        spring:
          cloud:
            gateway:
              routes:
                - id: order-service
                  uri: lb://ORDER-SERVICE
                  predicates:
                    - Path=/api/v1/orders/**,/api/v1/checkout/**
                - id: user-service
                  uri: lb://USER-SERVICE
                  predicates:
                    - Path=/api/v1/users/**
        """
        res_dir = self.root / "src" / "main" / "resources"
        res_dir.mkdir(parents=True, exist_ok=True)
        (res_dir / "application.yml").write_text(yml_content, encoding="utf-8")

        routes = parse_gateway_routes(self.root)
        self.assertEqual(len(routes), 2)
        self.assertEqual(routes[0]["id"], "order-service")
        self.assertIn("/api/v1/orders/**", routes[0]["paths"])
        self.assertIn("/api/v1/checkout/**", routes[0]["paths"])

    def test_build_and_query_project_graph(self):
        # Tạo mock project
        gw_dir = self.root / "platform-services" / "gateway" / "src" / "main" / "resources"
        gw_dir.mkdir(parents=True, exist_ok=True)
        (gw_dir / "application.yml").write_text("""
        spring:
          cloud:
            gateway:
              routes:
                - id: order-route
                  uri: lb://order-service
                  predicates:
                    - Path=/api/v1/orders/**
        """, encoding="utf-8")

        svc_dir = self.root / "business" / "order-service" / "src" / "main" / "java"
        svc_dir.mkdir(parents=True, exist_ok=True)
        (svc_dir / "OrderController.java").write_text("""
        package com.test;
        import org.springframework.web.bind.annotation.*;
        @RestController
        @RequestMapping("/api/v1/orders")
        public class OrderController {
            // Xem đơn hàng
            @GetMapping("/{id}")
            public String getOrder(@PathVariable String id) { return id; }
        }
        """, encoding="utf-8")

        (svc_dir / "OrderEntity.java").write_text("""
        package com.test;
        import jakarta.persistence.*;
        @Entity
        @Table(name = "orders")
        public class OrderEntity {
            @Id private Long id;
            @Column(name = "status") private String status;
        }
        """, encoding="utf-8")

        out_file = self.root / "doc" / "architecture" / "project-graph.json"
        graph = build_project_graph(self.root, out_file)

        self.assertTrue(out_file.exists())
        self.assertGreaterEqual(graph["stats"]["total_endpoints"], 1)
        self.assertGreaterEqual(graph["stats"]["total_tables"], 1)

        # Test query
        results = query_project_graph(graph, "orders")
        self.assertGreaterEqual(len(results), 1)

        results_api = query_project_graph(graph, "orders", kind="Endpoint")
        self.assertEqual(len(results_api), 1)
        self.assertEqual(results_api[0]["path"], "/api/v1/orders/{id}")


if __name__ == "__main__":
    unittest.main()
