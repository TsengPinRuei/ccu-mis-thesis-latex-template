#!/usr/bin/env python3
"""Measure this repository's supplied demonstration PDFs, not arbitrary theses.

Requires pdfplumber and pypdf. Coordinates and sizes are PDF points (bp = 1/72").
The assertions intentionally use identifiable placeholder text in the examples.
After replacing the example chapters, perform a fresh visual review and adapt the
sample landmarks; a passing report is not a general thesis compliance certificate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import pdfplumber
    from pypdf import PdfReader
except ImportError as exc:
    raise SystemExit("Install verification dependencies: python3 -m pip install pdfplumber pypdf") from exc

BP_PER_MM = 72 / 25.4
MARGIN = 20 * BP_PER_MM
TOL = 0.1
ROOT = Path(__file__).resolve().parents[1]


def close(value, target, tolerance=TOL):
    return abs(value - target) <= tolerance


def compact(text):
    return re.sub(r"\s+", "", text)


def roman(number):
    result = ""
    for value, letters in ((1000, "m"), (900, "cm"), (500, "d"), (400, "cd"),
                           (100, "c"), (90, "xc"), (50, "l"), (40, "xl"),
                           (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")):
        while number >= value:
            result += letters
            number -= value
    return result


def rows(chars):
    """Group on actual text baselines, independent of font ascent/descent."""
    grouped = {}
    for char in chars:
        if char["text"].strip():
            grouped.setdefault(round(char["matrix"][5], 2), []).append(char)
    result = []
    for baseline, group in sorted(grouped.items(), reverse=True):
        group.sort(key=lambda char: char["x0"])
        result.append({
            "text": "".join(char["text"] for char in group),
            "baseline": baseline,
            "x0": min(char["x0"] for char in group),
            "x1": max(char["x1"] for char in group),
            "top": min(char["top"] for char in group),
            "bottom": max(char["bottom"] for char in group),
            "sizes": sorted({round(char["size"], 3) for char in group}),
            "chars": group,
        })
    return result


def footer_chars(page):
    return [char for char in page.chars if char["top"] > page.height - MARGIN]


def content_chars(page):
    return [char for char in page.chars
            if char["text"].strip() and char["top"] <= page.height - MARGIN]


def row_with(page, phrase, exact=False):
    target = compact(phrase)
    for row in rows(content_chars(page)):
        text = compact(row["text"])
        if text == target if exact else target in text:
            return row
    return None


def simple_row(row):
    if row is None:
        return None
    return {key: (round(value, 3) if isinstance(value, float) else value)
            for key, value in row.items() if key != "chars"}


def fonts_in_pdf(path):
    found = {}
    reader = PdfReader(path)
    for page in reader.pages:
        resources = page.get("/Resources", {}).get_object()
        for reference in resources.get("/Font", {}).values():
            font = reference.get_object()
            name = str(font.get("/BaseFont", "unknown")).lstrip("/")
            descendants = font.get("/DescendantFonts", [font])
            embedded = []
            for descendant in descendants:
                descriptor = descendant.get_object().get("/FontDescriptor")
                descriptor = descriptor.get_object() if descriptor else {}
                embedded.append(any(key in descriptor for key in
                                    ("/FontFile", "/FontFile2", "/FontFile3")))
            found[name] = all(embedded)
    return [{"name": name, "embedded": embedded} for name, embedded in sorted(found.items())]


class Verification:
    def __init__(self, path):
        report_path = path.resolve()
        try:
            # Keep shared reports independent of the local checkout directory.
            report_path = report_path.relative_to(ROOT)
        except ValueError:
            pass
        self.result = {
            "path": str(report_path),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "checks": [],
        }

    def check(self, name, passed, measured, source):
        self.result["checks"].append({
            "name": name, "status": "pass" if passed else "fail",
            "format_pdf_pages": source, "measured": measured,
        })

    def manual(self, name, measured, source):
        self.result["checks"].append({
            "name": name, "status": "manual",
            "format_pdf_pages": source, "measured": measured,
        })


def check_fonts(report, path):
    fonts = fonts_in_pdf(path)
    prescribed = [font for font in fonts if
                  "DFKaiShu-SB" in font["name"] or "TimesNewRoman" in font["name"]]
    report.check("prescribed_fonts_embedded",
                 any("DFKaiShu-SB" in f["name"] for f in prescribed)
                 and any("TimesNewRoman" in f["name"] for f in prescribed)
                 and all(f["embedded"] for f in prescribed),
                 fonts, [1])


def verify_thesis(path):
    report = Verification(path)
    with pdfplumber.open(path) as pdf:
        pages = pdf.pages
        report.result["page_count"] = len(pages)
        report.check("a4_page_sizes",
                     all(close(p.width, 210 * BP_PER_MM) and close(p.height, 297 * BP_PER_MM)
                         for p in pages),
                     [[round(p.width, 3), round(p.height, 3)] for p in pages],
                     "A4 is a documented default based on the source PDF page size")
        check_fonts(report, path)
        font_violations = []
        chinese_count = latin_count = math_latin_count = 0
        math_fonts = set()
        for page_index, page in enumerate(pages, 1):
            for char in page.chars:
                if re.search(r"[\u3400-\u9fff]", char["text"]):
                    chinese_count += 1
                    if "DFKaiShu-SB" not in char["fontname"]:
                        font_violations.append({"physical_page": page_index, "text": char["text"],
                                                "font": char["fontname"]})
                elif re.search(r"[A-Za-z]", char["text"]):
                    bare_font = char["fontname"].split("+")[-1]
                    if bare_font.startswith(("CM", "MSAM", "MSBM")):
                        math_latin_count += 1
                        math_fonts.add(bare_font)
                    else:
                        latin_count += 1
                        if "TimesNewRoman" not in bare_font:
                            font_violations.append({"physical_page": page_index, "text": char["text"],
                                                    "font": char["fontname"]})
        report.check("actual_chinese_and_nonmath_latin_font_assignments",
                     chinese_count > 0 and latin_count > 0 and not font_violations,
                     {"chinese_characters": chinese_count, "nonmath_latin_characters": latin_count,
                      "excluded_math_latin_characters": math_latin_count,
                      "excluded_math_fonts": sorted(math_fonts), "violations": font_violations}, [1])
        texts = [compact(page.extract_text() or "") for page in pages]
        headings = []
        for index, page in enumerate(pages):
            page_rows = rows(content_chars(page))
            headings.append(compact(page_rows[0]["text"]) if page_rows else "")
        starts = [index for index, title in enumerate(headings) if title == "第一章、緒論"]
        report.check("sample_body_landmark", len(starts) == 1,
                     {"physical_pages": [i + 1 for i in starts]}, [1, 17])
        if not starts:
            return report.result
        body_start = starts[0]
        proposal = "論文提案書" in texts[0]
        expected_front = (["目錄", "圖目錄", "表目錄"] if proposal else
                          ["論文口試委員會審定書", "誌謝", "摘要", "Abstract", "目錄", "圖目錄", "表目錄"])
        report.check("frontmatter_order", headings[1:body_start] == expected_front,
                     {"actual_headings": headings[1:body_start], "mode": "proposal" if proposal else "thesis"},
                     [1, 3])
        expected_footers = ([roman(i + 1) for i in range(body_start)]
                            + [str(i + 1) for i in range(len(pages) - body_start - 1)] + [""])
        actual_footers = [compact("".join(c["text"] for c in sorted(footer_chars(p), key=lambda c: c["x0"])))
                          for p in pages]
        report.check("continuous_printed_page_numbers", actual_footers == expected_footers,
                     {"actual": actual_footers, "expected": expected_footers}, [1])
        footer_measurements = []
        footer_ok = True
        for index, page in enumerate(pages[:-1]):
            chars = footer_chars(page)
            if not chars:
                footer_ok = False
                continue
            baseline = sum(c["matrix"][5] for c in chars) / len(chars)
            center = (min(c["x0"] for c in chars) + max(c["x1"] for c in chars)) / 2
            footer_measurements.append({"physical_page": index + 1,
                                        "baseline_from_bottom_mm": round(baseline / BP_PER_MM, 4),
                                        "center_error_bp": round(center - page.width / 2, 4)})
            footer_ok &= close(baseline, 10 * BP_PER_MM) and close(center, page.width / 2)
        report.check("footer_baseline_10mm_and_centered", footer_ok, footer_measurements, [2])
        last = pages[-1]
        report.check("blank_back_cover",
                     not (last.chars or last.images or last.lines or last.rects or last.curves),
                     {"characters": len(last.chars), "images": len(last.images),
                      "drawing_objects": len(last.lines) + len(last.rects) + len(last.curves)},
                     "Blank back cover is a documented default; composition specified on p.1")

        intrusions = []
        advance_intrusions = []
        bounds = []
        for index, page in enumerate(pages[:-1]):
            chars = content_chars(page)
            if not chars:
                continue
            bounds.append({"physical_page": index + 1,
                           "left_mm": round(min(c["x0"] for c in chars) / BP_PER_MM, 4),
                           "right_mm": round((page.width - max(c["x1"] for c in chars)) / BP_PER_MM, 4),
                           "top_mm": round(min(c["top"] for c in chars) / BP_PER_MM, 4),
                           "bottom_mm": round((page.height - max(c["bottom"] for c in chars)) / BP_PER_MM, 4)})
            for char in chars:
                # A sheared font cell rectangle is wider than its typeset advance.
                # Neither rectangle is a contour measurement of the glyph's ink.
                advance_left = char["matrix"][4]
                advance_right = advance_left + char["adv"] * char["matrix"][0]
                advance_outside = (advance_left < MARGIN - TOL
                                   or advance_right > page.width - MARGIN + TOL
                                   or char["top"] < MARGIN - TOL
                                   or char["bottom"] > page.height - MARGIN + TOL)
                if advance_outside:
                    advance_intrusions.append({"physical_page": index + 1, "text": char["text"],
                                               "advance_x_bp": [round(advance_left, 4), round(advance_right, 4)]})
                if (char["x0"] < MARGIN - TOL or char["x1"] > page.width - MARGIN + TOL
                        or char["top"] < MARGIN - TOL or char["bottom"] > page.height - MARGIN + TOL):
                    intrusions.append({"physical_page": index + 1, "text": char["text"],
                                       "bbox_bp": [round(char[k], 4) for k in ("x0", "top", "x1", "bottom")],
                                       "advance_x_bp": [round(advance_left, 4), round(advance_right, 4)],
                                       "shear": round(char["matrix"][2], 4),
                                       "advance_outside": advance_outside})
        report.check("text_advance_extents_within_20mm",
                     not advance_intrusions,
                     {"tolerance_bp": TOL, "intrusions": advance_intrusions,
                      "note": "Uses text origins plus advances horizontally and font cells vertically."},
                     [2, 4])
        bbox_measurements = {"tolerance_bp": TOL, "page_bounds": bounds, "intrusions": intrusions,
                             "note": "Font cell rectangles are not glyph ink contours. "
                             "Synthetic italic shear may extend the rectangle beyond its text advance."}
        if intrusions and all(item["shear"] and not item["advance_outside"] for item in intrusions):
            report.manual("slanted_font_cell_bbox_overhang", bbox_measurements, [2, 4])
        else:
            report.check("text_bounding_boxes_within_20mm", not intrusions, bbox_measurements, [2, 4])

        expected_watermark = [False] * len(pages)
        watermark_start = 1 if proposal else 2
        for index in range(watermark_start, len(pages) - 1):
            expected_watermark[index] = True
        image_presence = [bool(page.images) for page in pages]
        report.check("sample_watermark_page_presence", image_presence == expected_watermark,
                     {"actual_image_presence": image_presence, "expected_watermark_presence": expected_watermark,
                      "note": "Valid for the supplied vector placeholder figure; inspect the actual watermark visually."},
                     [3, 7, 9, 10, 17, 18])

        toc_measurements = []
        toc_ok = True
        for title in ("目錄", "圖目錄", "表目錄"):
            indexes = [i for i, heading in enumerate(headings[:body_start]) if heading == title]
            if len(indexes) != 1:
                toc_ok = False
                toc_measurements.append({"title": title, "found_pages": indexes})
                continue
            page = pages[indexes[0]]
            listing_rows = rows(content_chars(page))
            entries = listing_rows[1:]
            right_edges = [round(row["x1"], 4) for row in entries]
            entry_checks = [bool(re.search(r"[0-9ivxlcdm]+$", compact(row["text"])))
                            and "." in row["text"] and close(row["x1"], page.width - MARGIN)
                            for row in entries]
            toc_ok &= listing_rows[0]["sizes"] == [18] and bool(entries) and all(entry_checks)
            toc_measurements.append({"title": title, "physical_page": indexes[0] + 1,
                                     "heading_sizes_bp": listing_rows[0]["sizes"],
                                     "entry_right_edges_bp": right_edges,
                                     "entries": [row["text"] for row in entries]})
        report.check("contents_lists_titles_leaders_right_aligned_pages", toc_ok, toc_measurements, [5, 6, 7, 13, 14, 15, 16])

        cover_rows = rows(content_chars(pages[0]))
        university = row_with(pages[0], "國立中正大學", exact=True)
        report.check("cover_font_sizes_36_and_24",
                     university is not None and university["sizes"] == [36]
                     and all(row["sizes"] == [24] for row in cover_rows if row is not university
                             and compact(row["text"]) != "國立中正大學"),
                     [simple_row(row) for row in cover_rows], [5, 9])

        chapter = pages[body_start]
        size_landmarks = [("第一章、緒論", 18), ("1.1研究背景", 14), ("1.2.1研究範圍", 12),
                          ("第二段示範", 12)]
        measured_sizes = []
        size_ok = True
        for phrase, size in size_landmarks:
            row = row_with(chapter, phrase)
            measured_sizes.append({"landmark": phrase, "expected_bp": size, "row": simple_row(row)})
            size_ok &= row is not None and row["sizes"] == [size]
        report.check("chapter_section_subsection_body_sizes", size_ok, measured_sizes, [1])
        title_row = row_with(chapter, "第一章、緒論", exact=True)
        section_row = row_with(chapter, "1.1研究背景", exact=True)
        first_row = row_with(chapter, "【佔位資料】本論文示例")
        report.manual("heading_gap_measurements",
                      {"chapter_to_section_baselines_bp":
                       round(title_row["baseline"] - section_row["baseline"], 3) if title_row and section_row else None,
                       "section_to_body_baselines_bp":
                       round(section_row["baseline"] - first_row["baseline"], 3) if section_row and first_row else None,
                       "note": "Baseline distances include font/strut metrics. Do not equate them directly to blank-line glue; "
                       "review with the source class and rendered page."}, [1, 3, 17])

        first_paragraph = row_with(chapter, "【佔位資料】本論文示例")
        second_paragraph = row_with(chapter, "第二段示範")
        if first_paragraph and second_paragraph:
            paragraph_rows = [row for row in rows(content_chars(chapter))
                              if second_paragraph["baseline"] <= row["baseline"] <= first_paragraph["baseline"]]
            deltas = [round(a["baseline"] - b["baseline"], 3)
                      for a, b in zip(paragraph_rows, paragraph_rows[1:])]
            indent = second_paragraph["x0"] - MARGIN
            report.check("body_baselines_18bp_and_no_extra_paragraph_skip",
                         bool(deltas) and all(close(delta, 18) for delta in deltas),
                         {"sample_baseline_gaps_bp": deltas}, [2, 3, 17])
            report.check("sample_paragraph_indent_24bp", close(indent, 24),
                         {"second_paragraph_indent_bp": round(indent, 4)},
                         "Two-character indentation is a documented default based on pp.3/17")
        else:
            report.check("body_baselines_and_indent_landmarks", False, "Example paragraphs not found", [2, 3, 17])

        figure_label = row_with(chapter, "圖1.1", exact=True)
        figure_title = row_with(chapter, "研究流程示意圖（佔位資料）", exact=True)
        figure_body = row_with(chapter, "佔位流程圖")
        figure_note = row_with(chapter, "註：方框")
        figure_source = row_with(chapter, "參考文獻：本研究自行繪製")
        figure_parts = [figure_body, figure_label, figure_title, figure_note, figure_source]
        report.check("figure_body_label_title_note_source_order",
                     all(figure_parts) and all(a["baseline"] > b["baseline"]
                                              for a, b in zip(figure_parts, figure_parts[1:])),
                     [simple_row(row) for row in figure_parts], [4])
        method_candidates = [i for i, title in enumerate(headings) if title == "第二章、研究方法與版型示例"]
        if method_candidates:
            method = pages[method_candidates[0]]
            table_parts = [row_with(method, "表2.1", exact=True),
                           row_with(method, "示意資料彙整(佔位資料)", exact=True),
                           row_with(method, "組別(group)"),
                           row_with(method, "註：數值僅供"),
                           row_with(method, "參考文獻：王範例")]
            report.check("table_label_title_body_note_source_order",
                         all(table_parts) and all(a["baseline"] > b["baseline"]
                                                  for a, b in zip(table_parts, table_parts[1:])),
                         [simple_row(row) for row in table_parts], [4])
            note_sources = [figure_note, figure_source, table_parts[3], table_parts[4]]
            report.check("figure_table_notes_sources_10bp",
                         all(note_sources) and all(row["sizes"] == [10] for row in note_sources),
                         [simple_row(row) for row in note_sources], [4])
            citation_text = compact(method.extract_text() or "")
            markers = ["Adams", "Brown", "王範例", "林示例"]
            positions = [citation_text.find(marker) for marker in markers]
            report.check("in_text_citation_english_then_chinese_sample",
                         all(pos >= 0 for pos in positions) and positions == sorted(positions),
                         {"markers": markers, "text_positions": positions}, [6])
        else:
            report.check("sample_method_landmark", False, "Second chapter not found", [1, 4, 6])
        bibliography_pages = [i for i, title in enumerate(headings) if title == "參考文獻"]
        markers = ["王範例", "林示例", "Adams", "Brown"]
        bibliography = texts[bibliography_pages[0]] if bibliography_pages else ""
        positions = [bibliography.find(marker) for marker in markers]
        report.check("bibliography_chinese_then_english_sample",
                     all(pos >= 0 for pos in positions) and positions == sorted(positions),
                     {"markers": markers, "text_positions": positions}, [6])

        formula_results = []
        formulas_ok = True
        for label in ("(2.1)", "(A-1)", "(A-2)", "(B-1)"):
            candidates = []
            for index, page in enumerate(pages[body_start:-1], body_start + 1):
                for match in page.search(re.escape(label), regex=True, return_chars=True):
                    candidates.append({"physical_page": index, "x0_bp": round(match["x0"], 4),
                                       "top_bp": round(match["top"], 4)})
            left_matches = [m for m in candidates if close(m["x0_bp"], MARGIN)]
            formula_results.append({"label": label, "left_aligned_matches": left_matches,
                                    "all_matches": candidates})
            formulas_ok &= len(left_matches) == 1
        report.check("equation_and_appendix_labels_at_left_20mm",
                     formulas_ok, formula_results, [5, 6])
        report.check("no_unresolved_reference_markers",
                     not any("??" in text or "尚未定義書籤" in text for text in texts),
                     {"checked_physical_pages": len(pages)}, [6, 13, 14])
        report.manual("visual_review_still_required",
                      "Inspect rendered pages for watermark appearance, bold/slanted glyph appearance, "
                      "heading/blank-line spacing, content alignment, clipping and complete TOC links. "
                      "Font metadata and character rectangles do not measure actual glyph ink.", [1, 3, 4, 5, 6, 7, 8, 17])
    return report.result


def verify_spine(path):
    report = Verification(path)
    with pdfplumber.open(path) as pdf:
        report.result["page_count"] = len(pdf.pages)
        report.check("spine_single_page", len(pdf.pages) == 1, len(pdf.pages), [8])
        dimensions = [[round(p.width / BP_PER_MM, 4), round(p.height / BP_PER_MM, 4)] for p in pdf.pages]
        report.check("spine_height_297mm",
                     all(close(p.height, 297 * BP_PER_MM) for p in pdf.pages),
                     {"page_dimensions_mm": dimensions, "width_is_binding_shop_setting": True},
                     "Spine size is a documented default; source p.8 has no numeric dimensions")
        check_fonts(report, path)
        page = pdf.pages[0]
        overflow = [c["text"] for c in page.chars if c["x0"] < -TOL or c["x1"] > page.width + TOL
                    or c["top"] < -TOL or c["bottom"] > page.height + TOL]
        report.check("spine_text_inside_page", not overflow, {"overflow_characters": overflow}, [8])
        spine_rows = rows(page.chars)
        cjk_rows = [row for row in spine_rows if re.search(r"[\u3400-\u9fff]", row["text"])]
        report.check("spine_chinese_characters_vertically_stacked",
                     bool(cjk_rows) and all(len(compact(row["text"])) == 1 for row in cjk_rows),
                     [simple_row(row) for row in cjk_rows], [8])
        actual = compact("".join(row["text"] for row in spine_rows))
        markers = ["級", "國立中正大學", "研究所", "論文", "論文格式驗證範例", "王小明", "撰"]
        cursor = 0
        positions = []
        for marker in markers:
            position = actual.find(marker, cursor)
            positions.append(position)
            if position >= 0:
                cursor = position + len(marker)
        report.check("spine_sample_vertical_content_order", all(p >= 0 for p in positions),
                     {"extracted_top_to_bottom": actual, "markers": markers, "positions": positions}, [8])
        report.manual("binding_review_required",
                      "Confirm physical spine width, cropping and type size with the binding shop.", [8])
    return report.result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdfs", nargs="*", type=Path,
                        help="Defaults to existing output/pdf/main.pdf, proposal.pdf and spine.pdf.")
    parser.add_argument("--report", type=Path, help="Write measured results as JSON.")
    args = parser.parse_args()
    paths = args.pdfs or [ROOT / "output/pdf" / name for name in
                         ("main.pdf", "proposal.pdf", "spine.pdf")
                         if (ROOT / "output/pdf" / name).exists()]
    if not paths:
        parser.error("No PDFs found. Run bash scripts/build.sh first.")
    results = []
    for path in paths:
        if not path.is_file():
            parser.error(f"PDF not found: {path}")
        results.append(verify_spine(path) if path.stem == "spine" else verify_thesis(path))
    report = {"generated_at_utc": datetime.now(timezone.utc).isoformat(),
              "scope": "Measured checks of supplied demonstration PDFs; manual items are not automated passes.",
              "units": "bp = PDF points = 1/72 inch; mm = millimeters",
              "documents": results}
    failed = 0
    for document in results:
        print(f"{Path(document['path']).name}: {document.get('page_count', '?')} pages")
        for check in document["checks"]:
            print(f"  {check['status'].upper():6} {check['name']}")
            failed += check["status"] == "fail"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Measurements: {args.report.resolve()}")
    print(f"Failed automated checks: {failed}. Manual checks require a separate visual/physical review.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
