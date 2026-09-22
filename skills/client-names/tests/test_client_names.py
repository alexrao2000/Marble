"""End-to-end tests: real git repositories, real pushes, the real hook."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / "scripts"))
import client_names as cn  # noqa: E402

LIST = {
    "version": 1,
    "allowed_everywhere": ["github.com/me/memory-and-skills"],
    "clients": [
        {
            "client": "Acme",
            "allowed_remotes": ["github.com/acme-corp/*"],
            "names": [
                {"text": "Acme", "kind": "company"},
                {"text": "Wile Coyote", "kind": "person"},
                {"text": "C0ABC12345", "kind": "identifier"},
            ],
        }
    ],
}


class Normalize(unittest.TestCase):
    def test_forms(self):
        for url in (
            "git@github.com:acme-corp/app.git",
            "https://github.com/acme-corp/app",
            "https://github.com/acme-corp/app.git",
            "ssh://git@github.com/acme-corp/app.git",
            "git@github.com-work_alias:acme-corp/app.git",
        ):
            self.assertEqual(cn.normalize_remote(url), "github.com/acme-corp/app", url)

    def test_allowed_remote_gets_no_terms(self):
        self.assertEqual(cn.terms_for(LIST, "git@github.com:acme-corp/app.git"), [])
        self.assertEqual(cn.terms_for(LIST, "https://github.com/me/memory-and-skills"), [])
        self.assertEqual(len(cn.terms_for(LIST, "https://github.com/public/repo")), 3)

    def test_whole_word_case_insensitive(self):
        terms = cn.terms_for(LIST, "github.com/public/repo")
        self.assertTrue(cn.scan_lines("x", ["we built this for ACME last week"], terms))
        self.assertTrue(cn.scan_lines("x", ["#ext-acme-channel"], terms))
        self.assertFalse(cn.scan_lines("x", ["acmeish and pacme are fine"], terms))


class Push(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.list_path = self.tmp / "names.json"
        self.list_path.write_text(json.dumps(LIST))
        # the hook reads names.json beside the script, so run a copy of the skill
        self.skill = self.tmp / "skill"
        shutil.copytree(SKILL / "scripts", self.skill / "scripts")
        shutil.copytree(SKILL / "hooks", self.skill / "hooks", symlinks=True)
        shutil.copy(self.list_path, self.skill / "names.json")
        self.remote = self.tmp / "remote.git"
        subprocess.run(["git", "init", "-q", "--bare", str(self.remote)], check=True)
        self.work = self.tmp / "work"
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.work)], check=True)
        self.env = {
            **os.environ,
            "GIT_CONFIG_GLOBAL": str(self.tmp / "gitconfig"),
            "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
            "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
        }
        self.git("config", "core.hooksPath", str(self.skill / "hooks"))
        # the hook decides by URL; a file:// remote normalises to its path, which no rule allows
        self.git("remote", "add", "origin", self.remote.as_uri())
        self.commit("README.md", "hello\n", "Initial commit")
        self.assertEqual(self.push().returncode, 0)

    def git(self, *args, check=True):
        return subprocess.run(["git", "-C", str(self.work), *args], env=self.env,
                              capture_output=True, text=True, check=check)

    def commit(self, name, text, message):
        (self.work / name).write_text(text)
        self.git("add", name)
        self.git("commit", "-q", "-m", message)

    def push(self, *extra):
        return self.git("push", "-q", "origin", "HEAD:main", *extra, check=False)

    def test_blocks_name_in_added_line(self):
        self.commit("notes.md", "the Acme rollout\n", "Add notes")
        r = self.push()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Acme", r.stderr)

    def test_blocks_name_in_commit_message(self):
        self.commit("notes.md", "neutral\n", "Fix the thing Wile Coyote asked for")
        self.assertNotEqual(self.push().returncode, 0)

    def test_blocks_name_in_file_path(self):
        self.commit("acme-plan.md", "neutral\n", "Add plan")
        self.assertNotEqual(self.push().returncode, 0)

    def test_blocks_identifier(self):
        self.commit("cfg.yaml", "channel: C0ABC12345\n", "Add config")
        self.assertNotEqual(self.push().returncode, 0)

    def test_clean_push_passes(self):
        self.commit("notes.md", "nothing to see\n", "Add notes")
        self.assertEqual(self.push().returncode, 0)

    def test_new_branch_is_scanned(self):
        self.git("checkout", "-q", "-b", "feature")
        self.commit("notes.md", "for acme\n", "Add notes")
        r = self.git("push", "-q", "origin", "feature", check=False)
        self.assertNotEqual(r.returncode, 0)

    def test_repo_own_pre_push_still_runs(self):
        own = self.work / ".git" / "hooks" / "pre-push"
        own.write_text("#!/usr/bin/env bash\necho OWN-HOOK-RAN >&2\nexit 1\n")
        own.chmod(0o755)
        self.commit("notes.md", "clean\n", "Add notes")
        r = self.push()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("OWN-HOOK-RAN", r.stderr)

    def test_scan_text(self):
        body = self.tmp / "body.md"
        body.write_text("A proposal. Tested with Acme.\n")
        r = subprocess.run([sys.executable, str(self.skill / "scripts" / "client_names.py"),
                            "scan-text", str(body), "--remote", "github.com/public/repo"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        r = subprocess.run([sys.executable, str(self.skill / "scripts" / "client_names.py"),
                            "scan-text", str(body), "--remote", "github.com/acme-corp/app"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
