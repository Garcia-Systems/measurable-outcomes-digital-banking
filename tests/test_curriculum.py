import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CurriculumStructureTest(unittest.TestCase):
    def test_all_chapters_exist_once_in_files_and_contents(self):
        files = sorted((ROOT / "chapters").glob("part-*/chapter-*.md"))
        file_numbers = [int(path.name.split("-")[1]) for path in files]
        self.assertEqual(sorted(file_numbers), list(range(40)))
        self.assertEqual(len(file_numbers), len(set(file_numbers)))

        contents = (ROOT / "CONTENTS.md").read_text(encoding="utf-8")
        content_numbers = [int(value) for value in re.findall(r"^\d+\. \[Chapter (\d+):", contents, re.MULTILINE)]
        self.assertEqual(content_numbers, list(range(40)))

    def test_eight_parts_and_required_stub_sections(self):
        parts = list((ROOT / "chapters").glob("part-*"))
        self.assertEqual(len(parts), 8)
        headings = ["## Learning objectives", "## Measurable-outcome concept", "## Planned Harbor FCU scenario", "## Metrics to measure", "## Planned executable exercise", "## Expected takeaway"]
        for path in (ROOT / "chapters").glob("part-*/chapter-*.md"):
            text = path.read_text(encoding="utf-8")
            for heading in headings:
                self.assertIn(heading, text, f"{path} lacks {heading}")

    def test_every_chapter_has_complete_navigation(self):
        files = sorted(
            (ROOT / "chapters").glob("part-*/chapter-*.md"),
            key=lambda path: int(path.name.split("-")[1]),
        )
        for index, path in enumerate(files):
            text = path.read_text(encoding="utf-8")
            self.assertIn("[Contents](../../CONTENTS.md)", text)
            self.assertEqual("[Previous chapter]" in text, index > 0)
            self.assertEqual("[Next chapter]" in text, index < 39)

    def test_part_transitions_connect_the_learning_progression(self):
        files = {int(path.name.split("-")[1]): path for path in (ROOT / "chapters").glob("part-*/chapter-*.md")}
        for number in (4, 9, 14, 19, 24, 29, 34):
            self.assertIn("## Part transition", files[number].read_text(encoding="utf-8"))
        self.assertIn("## Book transition", files[39].read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
