# Self-Healing Tests

This folder contains advanced test scripts and machine learning models for self-healing UI automation, designed to work with the fintech application in this repository.

## Contents
- `multimodal_locator.py`: Multi-Modal Fusion Engine that combines DOM, visual, and text context for robust locator prediction using ViT and BERT.
- `predictive_healing.py`: Predictive Healing Framework that analyzes code changes and predicts which tests are at risk of breaking.
- `heal_element.py`: Strategy-based healing engine that attempts multiple approaches (visual, semantic, XAI) to recover from locator breakages.
- `certify_healing.py`: Cross-browser certification utility to ensure healing works in Chrome, Firefox, and Safari.

## Usage
- Integrate these modules with your Playwright test suite to:
  - Predict and recover from locator breakages using ML and multi-strategy healing.
  - Analyze upcoming UI changes and proactively identify at-risk tests.
  - Certify that healing works across multiple browsers.

## Advanced Healing and Certification
- All tests use `heal_element` as a fallback for critical UI actions (e.g., clicking buttons). If a selector fails, healing strategies are attempted in order:
  1. Visual context matching
  2. Semantic graph analysis
  3. XAI-based verification
  4. Human-in-the-loop fallback (alert)
- After a successful test, `certify_healing` is called to verify that the healing logic works in Chrome, Firefox, and Safari (using Playwright's async API).

## Example Playwright+ML Workflow
1. **Extract DOM, screenshot, and context for each UI element.**
2. **Use `MultiModalLocator` to predict the best locator for each element.**
3. **Run Playwright tests using these predicted locators.**
4. **If a locator fails, call `heal_element` to attempt recovery using multiple strategies.**
5. **After a successful test, call `await certify_healing(["chrome", "firefox"])` to ensure healing is robust across browsers.**
6. **Use `ChangePredictor` to analyze repo diffs and flag tests that may break.**

---

This folder is a starting point for research and experimentation in robust, self-healing UI automation. 