import git
import networkx as nx
import re
import os
from collections import defaultdict

class DiffParser:
    def extract_element_changes(self, commits):
        # Parse diffs to extract changed selectors (ids/classes) from HTML/JS/CSS files
        changed_elements = set()
        selector_regex = re.compile(r'(id|class)\s*=\s*["\\\']([\w\-]+)["\\\']')
        for commit in commits:
            for diff in commit.diff(commit.parents[0] if commit.parents else None, create_patch=True):
                if diff.a_path and (diff.a_path.endswith('.html') or diff.a_path.endswith('.js') or diff.a_path.endswith('.css')):
                    diff_text = diff.diff.decode(errors='ignore')
                    for line in diff_text.splitlines():
                        if line.startswith('+') or line.startswith('-'):
                            for match in selector_regex.finditer(line):
                                changed_elements.add(match.group(2))
        return [{'element': el} for el in changed_elements]

class ChangePredictor:
    def __init__(self, repo_path):
        self.repo = git.Repo(repo_path)
        self.diff_analyzer = DiffParser()
        self.element_graph = nx.DiGraph()  # Directed for dependency propagation
        self.element_to_tests = defaultdict(set)
        self._build_element_test_graph(repo_path)

    def _build_element_test_graph(self, repo_path):
        # Scan test files for selectors and map them to test functions
        test_dir = os.path.join(repo_path, 'selfhealingtests')
        selector_regex = re.compile(r'["\\\']([#\.]?[\w\-]+)["\\\']')
        for root, _, files in os.walk(test_dir):
            for fname in files:
                if fname.startswith('test_') and fname.endswith('.py'):
                    fpath = os.path.join(root, fname)
                    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                    current_test = None
                    for line in lines:
                        if line.strip().startswith('async def') or line.strip().startswith('def'):
                            current_test = line.strip().split()[2].split('(')[0]
                        for match in selector_regex.finditer(line):
                            selector = match.group(1)
                            if selector and current_test:
                                self.element_to_tests[selector].add(f"{fname}::{current_test}")
                                self.element_graph.add_node(selector)
                                self.element_graph.nodes[selector].setdefault('tests', set()).add(f"{fname}::{current_test}")
        # Optionally, add edges for known dependencies (e.g., parent-child in DOM)
        # For demo, we skip this, but it can be extended.

    def predict_breakages(self):
        # Analyze upcoming UI changes
        unmerged_commits = self.repo.iter_commits('origin/main..HEAD')
        ui_changes = self.diff_analyzer.extract_element_changes(unmerged_commits)
        # Propagate impact through element dependency graph
        affected_tests = set()
        suggestions = []
        for change in ui_changes:
            element = change['element']
            # Find all tests that use this element or are downstream in the graph
            if element in self.element_graph:
                for node in nx.dfs_preorder_nodes(self.element_graph, element):
                    affected_tests.update(self.element_graph.nodes[node].get('tests', []))
                suggestions.append(f"Element '{element}' changed. Check tests using selector '{element}'.")
            else:
                suggestions.append(f"Element '{element}' changed, but not mapped to any test.")
        return {
            "version": self.repo.head.commit.hexsha,
            "affected_elements": ui_changes,
            "tests_at_risk": list(affected_tests),
            "suggestions": suggestions
        } 