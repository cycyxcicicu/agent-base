import unittest
from agent_core.design.tokens import DesignTokens, TokenCompiler
from agent_core.design.linter import TokenLinter
from agent_core.design.svg_diagram import DiagramRenderer, Box, Connection


class TestDesignModules(unittest.TestCase):
    def test_design_token_resolution_and_css_compilation(self):
        raw_tokens = {
            "primitive": {
                "color": {
                    "blue": {"600": "#2563eb"}
                }
            },
            "semantic": {
                "color": {
                    "primary": "{primitive.color.blue.600}"
                }
            },
            "component": {
                "button": {
                    "bg": "{semantic.color.primary}"
                }
            }
        }
        tokens = DesignTokens(raw_tokens)
        self.assertEqual(tokens.resolved["primitive.color.blue.600"], "#2563eb")
        self.assertEqual(tokens.resolved["semantic.color.primary"], "#2563eb")
        self.assertEqual(tokens.resolved["component.button.bg"], "#2563eb")

        css = TokenCompiler.to_css_variables(tokens)
        self.assertIn("--primitive-color-blue-600: #2563eb;", css)
        self.assertIn("--semantic-color-primary: #2563eb;", css)

    def test_token_linter_and_contrast(self):
        sample_code = "const style = { color: '#ff0000', width: '250px' };"
        issues = TokenLinter.lint_file_content(sample_code, "Button.tsx")
        self.assertTrue(any(i.rule == "no_hardcoded_hex" for i in issues))
        self.assertTrue(any(i.rule == "no_large_hardcoded_px" for i in issues))

        # Tương phản trắng trên đen
        contrast = TokenLinter.calculate_contrast("#ffffff", "#000000")
        self.assertEqual(contrast, 21.0)
        self.assertTrue(TokenLinter.is_wcag_aa_compliant("#ffffff", "#000000"))
        self.assertTrue(TokenLinter.is_wcag_aaa_compliant("#ffffff", "#000000"))

        # Tương phản thấp xám nhạt trên trắng (#cccccc trên #ffffff)
        self.assertFalse(TokenLinter.is_wcag_aa_compliant("#cccccc", "#ffffff"))

    def test_svg_diagram_renderer(self):
        boxes = [
            Box("b1", "Frontend UI", "Next.js / Tailwind", 50, 100, color_tier="primary"),
            Box("b2", "API Gateway", "FastAPI / Node", 350, 100, color_tier="secondary")
        ]
        connections = [Connection("b1", "b2", label="HTTP JSON")]
        svg = DiagramRenderer.render_svg("Kiến trúc Mẫu", boxes, connections)
        self.assertIn("<svg", svg)
        self.assertIn("Frontend UI", svg)
        self.assertIn("API Gateway", svg)
        self.assertIn("HTTP JSON", svg)

    def test_multi_lane_pipeline_svg(self):
        stages = [
            {"id": "s1", "label": "Client App", "subtext": "Mobile/Web", "color_tier": "primary"},
            {"id": "s2", "label": "API Gateway", "subtext": "Envoy/Kong", "color_tier": "secondary", "conn_label": "mTLS"},
            {"id": "s3", "label": "Database", "subtext": "PostgreSQL", "color_tier": "accent", "conn_label": "SQL"}
        ]
        svg = DiagramRenderer.render_multi_lane_pipeline("Luồng Hệ Thống", stages)
        self.assertIn("Client App", svg)
        self.assertIn("API Gateway", svg)
        self.assertIn("Database", svg)
        self.assertIn("mTLS", svg)
        self.assertIn('filter="url(#paper-mask)"' if 'filter="url(#paper-mask)"' in svg else 'id="paper-mask"', svg)


if __name__ == "__main__":
    unittest.main()
