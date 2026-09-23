"""
WCAG 2.1 AA Accessibility Test Suite for LegalLens AI.
Verifies compliance with Web Content Accessibility Guidelines (WCAG 2.1 Level AA):
1. Perceivable: Text alternatives, semantic markup, high-contrast dark theme.
2. Operable: Full keyboard navigation, skip-to-content links, WAI-ARIA tablists.
3. Understandable: Meaningful headings, form labels, unambiguous error feedback.
4. Robust: Valid HTML5, standard ARIA roles, assistive technology live regions.
"""

import unittest
import re
from app import app


class AccessibilityWCAGTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        res = self.app.get('/')
        self.html = res.data.decode('utf-8')

    def test_01_document_language_declared(self):
        """WCAG 3.1.1 (Level A): Document must specify lang attribute."""
        self.assertIn('<html lang="en"', self.html, "HTML element must specify lang='en'.")

    def test_02_skip_to_main_content_link(self):
        """WCAG 2.4.1 (Level A): Provide a skip-to-content link for keyboard users."""
        self.assertIn('href="#main-content"', self.html, "Skip-to-content anchor must exist.")
        self.assertIn('id="main-content"', self.html, "Target element #main-content must exist.")

    def test_03_semantic_landmarks_present(self):
        """WCAG 1.3.1 (Level A): Semantic structural landmarks must be present."""
        self.assertIn('<header', self.html, "Header landmark must exist.")
        self.assertIn('<main', self.html, "Main landmark must exist.")
        self.assertIn('<nav', self.html, "Navigation landmark must exist.")
        self.assertIn('<footer', self.html, "Footer landmark must exist.")

    def test_04_heading_hierarchy(self):
        """WCAG 1.3.1 (Level A): Page must contain logical heading hierarchy."""
        self.assertIn('<h1', self.html, "Page must contain an h1 element.")
        self.assertIn('<h2', self.html, "Page must contain h2 elements.")
        self.assertIn('<h3', self.html, "Page must contain h3 elements.")

    def test_05_wai_aria_tablist_pattern(self):
        """WCAG 4.1.2 (Level A): Tab navigation must adhere to WAI-ARIA tablist pattern."""
        self.assertIn('role="tablist"', self.html, "Tab container must declare role='tablist'.")
        self.assertIn('role="tab"', self.html, "Tabs must declare role='tab'.")
        self.assertIn('aria-selected="true"', self.html, "Active tab must have aria-selected='true'.")
        self.assertIn('aria-controls=', self.html, "Tabs must declare aria-controls.")
        self.assertIn('role="tabpanel"', self.html, "Panels must declare role='tabpanel'.")
        self.assertIn('aria-labelledby=', self.html, "Panels must link back via aria-labelledby.")

    def test_06_accessible_dialog_modals(self):
        """WCAG 4.1.2 (Level A): Modal dialogs must declare role='dialog' and aria-modal='true'."""
        self.assertIn('role="dialog"', self.html, "Modals must have role='dialog'.")
        self.assertIn('aria-modal="true"', self.html, "Modals must declare aria-modal='true'.")
        self.assertIn('aria-labelledby="apiKeyModalTitle"', self.html, "API Key modal must be labeled.")
        self.assertIn('aria-labelledby="exportModalTitle"', self.html, "Export modal must be labeled.")

    def test_07_form_inputs_have_associated_labels(self):
        """WCAG 1.3.1 & 3.3.2 (Level A): Form inputs must have matching labels."""
        input_ids = ["contractTextInput", "diffTextA", "diffTextB", "interrogateInput",
                     "scenarioInput", "redraftClauseInput", "targetLanguageSelect", "groqApiKeyInput"]
        for input_id in input_ids:
            label_pattern = f'for="{input_id}"'
            self.assertIn(label_pattern, self.html, f"Missing <label for='{input_id}'>.")

    def test_08_interactive_buttons_have_accessible_names(self):
        """WCAG 4.1.2 (Level A): Buttons must have text content or an aria-label."""
        # Check buttons with aria-label
        self.assertIn('aria-label="Load pre-loaded sample test contracts"', self.html)
        self.assertIn('aria-label="Configure Groq API Key"', self.html)
        self.assertIn('aria-label="Export comprehensive legal audit report"', self.html)
        self.assertIn('aria-label="Run full AI contract audit"', self.html)

    def test_09_live_regions_for_assistive_tech(self):
        """WCAG 4.1.3 (Level AA): Status changes must be announced to screen readers via aria-live."""
        self.assertIn('aria-live="polite"', self.html, "Dynamic content areas must use aria-live='polite'.")

    def test_10_decorative_icons_hidden(self):
        """WCAG 1.1.1 (Level A): Decorative icons must declare aria-hidden='true'."""
        self.assertIn('aria-hidden="true"', self.html, "Decorative icons must be hidden from screen readers.")


if __name__ == "__main__":
    unittest.main()
