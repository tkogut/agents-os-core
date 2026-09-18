#!/usr/bin/env python3
"""
test_guard_coordinator_pretool.py — Unit tests for guard_coordinator_pretool.py
"""

import unittest
from scripts.guard_coordinator_pretool import evaluate_tool_call


class TestGuardCoordinatorPretool(unittest.TestCase):

    def test_block_direct_src_jsx(self):
        payload = {
            "toolCall": {
                "name": "write_to_file",
                "args": {"TargetFile": "/home/user/projects/sample_project/ui_dashboard/src/components/AggregatedPnLCard.jsx"}
            }
        }
        res = evaluate_tool_call(payload)
        self.assertEqual(res["decision"], "force_ask")
        self.assertIn("Swarm Governance Alert", res["reason"])

    def test_block_direct_python_file(self):
        payload = {
            "toolCall": {
                "name": "replace_file_content",
                "args": {"TargetFile": "/home/user/projects/sample_project/src/sample_project/__init__.py"}
            }
        }
        res = evaluate_tool_call(payload)
        self.assertEqual(res["decision"], "force_ask")
        self.assertIn("Swarm Governance Alert", res["reason"])

    def test_allow_worktree_edits(self):
        payload = {
            "toolCall": {
                "name": "write_to_file",
                "args": {"TargetFile": "/home/user/projects/sample_project/tmp/worktrees/feature/dashboard-pnl/src/App.jsx"}
            }
        }
        res = evaluate_tool_call(payload)
        self.assertEqual(res["decision"], "allow")

    def test_allow_memory_and_task(self):
        payload_mem = {
            "toolCall": {
                "name": "write_to_file",
                "args": {"TargetFile": "/home/user/projects/sample_project/.agents/MEMORY.md"}
            }
        }
        res_mem = evaluate_tool_call(payload_mem)
        self.assertEqual(res_mem["decision"], "allow")

        payload_task = {
            "toolCall": {
                "name": "replace_file_content",
                "args": {"TargetFile": "/home/user/projects/sample_project/.agents/task.md"}
            }
        }
        res_task = evaluate_tool_call(payload_task)
        self.assertEqual(res_task["decision"], "allow")

    def test_allow_brain_artifacts(self):
        payload = {
            "toolCall": {
                "name": "write_to_file",
                "args": {"TargetFile": "/home/user/.gemini/antigravity-cli/brain/9396bb06-1200-4c8d-9686-23acccdf4d5b/plan.md"}
            }
        }
        res = evaluate_tool_call(payload)
        self.assertEqual(res["decision"], "allow")

    def test_allow_markdown_and_config(self):
        payload_md = {
            "toolCall": {
                "name": "write_to_file",
                "args": {"TargetFile": "/home/user/projects/sample_project/docs/ARCHITECTURE.md"}
            }
        }
        self.assertEqual(evaluate_tool_call(payload_md)["decision"], "allow")

        payload_attr = {
            "toolCall": {
                "name": "write_to_file",
                "args": {"TargetFile": "/home/user/projects/sample_project/.gitattributes"}
            }
        }
        self.assertEqual(evaluate_tool_call(payload_attr)["decision"], "allow")


if __name__ == "__main__":
    unittest.main()
