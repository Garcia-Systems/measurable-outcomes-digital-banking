import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class MarkdownLinksTest(unittest.TestCase):
    def test_relative_markdown_links_exist(self):
        for source in ROOT.rglob('*.md'):
            if '.git' in source.parts: continue
            for target in re.findall(r'\[[^]]+\]\(([^)]+)\)',source.read_text(encoding='utf-8')):
                if '://' in target or target.startswith('#'): continue
                path=(source.parent/target.split('#')[0]).resolve()
                self.assertTrue(path.exists(),f'{source.relative_to(ROOT)} -> {target}')
