# Self-Healing Tests

This folder contains advanced test scripts and machine learning models for self-healing UI automation, designed to work with the fintech application in this repository.

## Contents
- `multimodal_locator.py`: Multi-Modal Fusion Engine that combines DOM, visual, and text context for robust locator prediction using ViT and BERT.
- `predictive_healing.py`: Predictive Healing Framework that analyzes code changes and predicts which tests are at risk of breaking.

## Usage
- Integrate these modules with your Playwright test suite to:
  - Predict and recover from locator breakages using ML.
  - Analyze upcoming UI changes and proactively identify at-risk tests.

## Example Playwright+ML Workflow
1. **Extract DOM, screenshot, and context for each UI element.**
2. **Use `MultiModalLocator` to predict the best locator for each element.**
3. **Run Playwright tests using these predicted locators.**
4. **Use `ChangePredictor` to analyze repo diffs and flag tests that may break.**

---

This folder is a starting point for research and experimentation in robust, self-healing UI automation. 