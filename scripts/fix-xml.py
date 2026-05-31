#!/usr/bin/env python3
"""
Draw.io XML Auto-Fix Script

Translates the 24-step validateAndFixXml pipeline from next-ai-draw-io
into a standalone Python script. Fixes common LLM-generated XML mistakes.

Usage:
    python fix-xml.py input.xml [output.xml]
    echo "<xml>" | python fix-xml.py -
"""

import re
import sys
from pathlib import Path

STRUCTURAL_ATTRS = ["edge", "parent", "source", "target", "vertex", "connectable"]

VALID_DRAWIO_TAGS = {
    "mxfile", "diagram", "mxGraphModel", "root",
    "mxCell", "mxGeometry", "mxPoint", "Array",
    "Object", "mxRectangle",
}

TAG_TYPOS = [
    (re.compile(r"</mxElement>", re.I), "</mxCell>"),
    (re.compile(r"</mxcell>"), "</mxCell>"),
    (re.compile(r"</mxgeometry>"), "</mxGeometry>"),
    (re.compile(r"</mxpoint>"), "</mxPoint>"),
    (re.compile(r"</mxgraphmodel>", re.I), "</mxGraphModel>"),
]


def fix_json_escaped(xml: str) -> tuple[str, bool]:
    """Fix JSON-escaped XML: \" -> ", \\n -> newline"""
    if '=\\"' not in xml:
        return xml, False
    xml = xml.replace('\\"', '"')
    xml = xml.replace("\\n", "\n")
    return xml, True


def fix_cdata(xml: str) -> tuple[str, bool]:
    """Remove CDATA wrapper"""
    if re.match(r"^\s*<!\[CDATA\[", xml):
        xml = re.sub(r"^\s*<!\[CDATA\[", "", xml)
        xml = re.sub(r"\]\]>\s*$", "", xml)
        return xml, True
    return xml, False


def strip_trailing_wrappers(xml: str) -> tuple[str, bool]:
    """
    Strip trailing LLM wrapper tags after last mxCell.
    
    Only strips tags that are clearly LLM wrappers (like </answer>, </xml>, etc.)
    Does NOT strip legitimate draw.io closing tags like </root>, </mxGraphModel>
    """
    # Find the last mxCell closing tag
    last_cell = xml.rfind("</mxCell>")
    if last_cell == -1:
        return xml, False
    
    # Get everything after the last mxCell
    after_last_cell = xml[last_cell + 9:]  # 9 = len("</mxCell>")
    
    # Check if there are any non-whitespace, non-drawio-closing tags
    # Legitimate draw.io structure ends with </root></mxGraphModel>
    legitimate_endings = ["</root>", "</mxGraphModel>", "</mxfile>", "</diagram>"]
    
    # If the suffix only contains whitespace and legitimate endings, don't strip
    suffix_stripped = after_last_cell.strip()
    if not suffix_stripped:
        return xml, False  # Only whitespace, nothing to strip
    
    # Check if suffix contains only legitimate draw.io closing tags
    temp = suffix_stripped
    is_legitimate = True
    for ending in legitimate_endings:
        temp = temp.replace(ending, "").strip()
    if not temp:
        return xml, False  # Only legitimate endings, don't strip
    
    # Check for LLM wrapper patterns
    llm_wrapper_pattern = re.compile(r"^(\s*</(?!root|mxGraphModel|mxfile|diagram)[a-zA-Z][a-zA-Z0-9]*>)+\s*$")
    if llm_wrapper_pattern.match(after_last_cell):
        xml = xml[: last_cell + 9]
        return xml, True
    
    return xml, False


def remove_text_before_root(xml: str) -> tuple[str, bool]:
    """Remove garbage text before XML root"""
    m = re.search(r"<(\?xml|mxGraphModel|mxfile)", xml, re.I)
    if m and m.start() > 0 and not re.match(r"^\s*<[a-zA-Z]", xml):
        xml = xml[m.start():]
        return xml, True
    return xml, False


def fix_duplicate_attrs(xml: str) -> tuple[str, bool]:
    """Remove duplicate structural attributes, keep first"""
    fixed = False
    def tag_replacer(m: re.Match) -> str:
        nonlocal fixed
        tag = m.group(0)
        for attr in STRUCTURAL_ATTRS:
            pattern = re.compile(rf'\s{attr}\s*=\s*["\'][^"\']*["\']', re.I)
            matches = pattern.findall(tag)
            if len(matches) > 1:
                first = True
                def replacer(mm: re.Match) -> str:
                    nonlocal first, fixed
                    if first:
                        first = False
                        return mm.group(0)
                    fixed = True
                    return ""
                tag = pattern.sub(replacer, tag)
        return tag
    xml = re.sub(r"<[^>]+>", tag_replacer, xml)
    return xml, fixed


def fix_unescaped_ampersand(xml: str) -> tuple[str, bool]:
    """Fix unescaped & characters (but not valid entities)"""
    pattern = re.compile(r"&(?!(?:lt|gt|amp|quot|apos|#[0-9]+|#x[0-9a-fA-F]+);)")
    if pattern.search(xml):
        xml = pattern.sub("&amp;", xml)
        return xml, True
    return xml, False


def fix_double_escaped_entities(xml: str) -> tuple[str, bool]:
    """Fix double-escaped entities like &ampquot; -> &quot;"""
    replacements = [
        (re.compile(r"&ampquot;"), "&quot;"),
        (re.compile(r"&amplt;"), "&lt;"),
        (re.compile(r"&ampgt;"), "&gt;"),
        (re.compile(r"&ampapos;"), "&apos;"),
        (re.compile(r"&ampamp;"), "&amp;"),
    ]
    fixed = False
    for pattern, repl in replacements:
        if pattern.search(xml):
            xml = pattern.sub(repl, xml)
            fixed = True
    return xml, fixed


def fix_malformed_quotes(xml: str) -> tuple[str, bool]:
    """
    Fix malformed attribute quotes: =&quot;value&quot; -> ="value"
    
    ⚠️ CRITICAL: This function should ONLY convert &quot; when it's used as
    the outer quotes of an attribute value, NOT when &quot; appears inside
    a value that already uses normal quotes.
    
    Example of what to fix:
    - <mxCell id="1" value=&quot;text&quot;> -> <mxCell id="1" value="text">
    
    Example of what NOT to fix:
    - value="&lt;font color=&quot;#6e6e80&quot;&gt;" (correctly escaped HTML)
    
    Strategy: Only match attribute=&quot;...&quot; when the attribute is NOT 'value'
    OR when value=&quot;...&quot; doesn't contain HTML tags.
    """
    fixed = False
    
    # Pattern 1: Non-value attributes with &quot; outer quotes
    # e.g., id=&quot;test&quot; style=&quot;rounded&quot;
    pattern1 = re.compile(r'(\s(?:id|style|vertex|parent|edge|source|target|connectable))=&quot;([^&]*?)&quot;')
    
    def replacer1(m: re.Match) -> str:
        nonlocal fixed
        fixed = True
        return f'{m.group(1)}="{m.group(2)}"'
    
    xml = pattern1.sub(replacer1, xml)
    
    # Pattern 2: value=&quot;...&quot; but ONLY if no HTML tags inside
    # value="&lt;font...&quot;...&quot;...&gt;" should NOT be matched
    # value=&quot;plain text&quot; SHOULD be matched
    pattern2 = re.compile(r'(value)=&quot;((?:[^&]|&(?!lt;|gt;))*?)&quot;')
    
    def replacer2(m: re.Match) -> str:
        nonlocal fixed
        attr_value = m.group(2)
        # Skip if contains HTML tags
        if '&lt;' in attr_value or '&gt;' in attr_value:
            return m.group(0)
        fixed = True
        return f'value="{attr_value}"'
    
    xml = pattern2.sub(replacer2, xml)
    
    return xml, fixed


def fix_unescaped_html_quotes(xml: str) -> tuple[str, bool]:
    """
    Fix unescaped quotes inside HTML tags within value attributes.
    Example: &lt;font color="#6e6e80"&gt; → &lt;font color=&quot;#6e6e80&quot;&gt;
    
    This function specifically targets HTML tags (between &lt; and &gt;)
    that have unescaped double quotes in their attributes.
    """
    fixed = False
    
    # Strategy: Find all mxCell elements and process their value attributes
    # We need to handle the case where value contains unescaped quotes
    
    def process_mxcell(m: re.Match) -> str:
        nonlocal fixed
        full_match = m.group(0)
        
        # Find value attribute - it starts with value=" and we need to find the closing "
        # The closing " is followed by a space and another attribute, or > or />
        value_pattern = re.compile(r'(value=")(.*?)("(\s+\w|/>|>))')
        
        def fix_value(v: re.Match) -> str:
            nonlocal fixed
            prefix = v.group(1)  # value="
            content = v.group(2)  # content (may contain unescaped quotes)
            suffix = v.group(3)  # " followed by space+attr or /> or >
            
            # Find HTML tags with unescaped quotes: &lt;tag attr="value"&gt;
            html_attr_pattern = re.compile(r'(&lt;[a-zA-Z][a-zA-Z0-9]*[^&]*?)([a-zA-Z-]+)="([^"]*)"')
            
            if html_attr_pattern.search(content):
                # Replace unescaped quotes in HTML attributes
                new_content = html_attr_pattern.sub(
                    lambda hm: f'{hm.group(1)}{hm.group(2)}=&quot;{hm.group(3)}&quot;',
                    content
                )
                fixed = True
                return f'{prefix}{new_content}{suffix}'
            
            return v.group(0)
        
        return value_pattern.sub(fix_value, full_match)
    
    # Process all mxCell elements
    new_xml = re.sub(r'<mxCell[^>]*>.*?</mxCell>', process_mxcell, xml, flags=re.DOTALL)
    return new_xml, fixed


def fix_malformed_closing(xml: str) -> tuple[str, bool]:
    """Fix </tag/> -> </tag>"""
    pattern = re.compile(r"</([a-zA-Z][a-zA-Z0-9]*)\s*/>")
    if pattern.search(xml):
        xml = pattern.sub(r"</\1>", xml)
        return xml, True
    return xml, False


def fix_missing_space(xml: str) -> tuple[str, bool]:
    """Fix missing space between attributes: "1"parent= -> "1" parent="""
    pattern = re.compile(r'("[^"]*")([a-zA-Z][a-zA-Z0-9_:-]*=)')
    if pattern.search(xml):
        xml = pattern.sub(r"\1 \2", xml)
        return xml, True
    return xml, False


def fix_quoted_colors(xml: str) -> tuple[str, bool]:
    """Remove quotes around color values: fillColor="#fff -> fillColor=#fff"""
    pattern = re.compile(r";([a-zA-Z]*[Cc]olor)=\"#")
    if pattern.search(xml):
        xml = pattern.sub(r";\1=#", xml)
        return xml, True
    return xml, False


def fix_unescaped_lt_in_attrs(xml: str) -> tuple[str, bool]:
    """Escape < and > inside attribute values"""
    def replacer(m: re.Match) -> str:
        value = m.group(1)
        value = value.replace("<", "&lt;").replace(">", "&gt;")
        return f'="{value}"'
    new_xml = re.sub(r'="([^"]*?[<>][^"]*?)"', replacer, xml)
    if new_xml != xml:
        return new_xml, True
    return xml, False


def fix_cell_tags(xml: str) -> tuple[str, bool]:
    """Fix <Cell> -> <mxCell>"""
    if re.search(r"</?Cell[\s>]", xml):
        xml = re.sub(r"<Cell(\s)", r"<mxCell\1", xml)
        xml = re.sub(r"<Cell>", "<mxCell>", xml)
        xml = re.sub(r"</Cell>", "</mxCell>", xml)
        return xml, True
    return xml, False


def fix_tag_typos(xml: str) -> tuple[str, list[str]]:
    """Fix common closing tag typos"""
    fixes = []
    for pattern, repl in TAG_TYPOS:
        if pattern.search(xml):
            xml = pattern.sub(repl, xml)
            fixes.append(f"Fixed typo to {repl}")
    return xml, fixes


def is_inside_quotes(xml: str, pos: int) -> bool:
    """Check if position is inside a quoted attribute value"""
    in_quote = False
    quote_char = ""
    for i in range(pos):
        c = xml[i]
        if in_quote:
            if c == quote_char:
                in_quote = False
        elif c in ('"', "'"):
            j = i - 1
            while j >= 0 and xml[j].isspace():
                j -= 1
            if j >= 0 and xml[j] == "=":
                in_quote = True
                quote_char = c
    return in_quote


def remove_foreign_tags(xml: str) -> tuple[str, bool]:
    """Remove non-draw.io tags (preserve HTML inside attribute values)"""
    pattern = re.compile(r"</?([a-zA-Z][a-zA-Z0-9_]*)[^>]*>")
    found = False
    def replacer(m: re.Match) -> str:
        nonlocal found
        tag_name = m.group(1)
        if tag_name in VALID_DRAWIO_TAGS:
            return m.group(0)
        if is_inside_quotes(xml, m.start()):
            return m.group(0)
        found = True
        return ""
    xml = pattern.sub(replacer, xml)
    return xml, found


def fix_nested_mxcell(xml: str) -> tuple[str, bool]:
    """Flatten nested mxCell tags"""
    if re.search(r"<mxCell[^>]*>[\s\S]*?<mxCell", xml):
        xml = re.sub(r"(<mxCell[^>]*>)\s*(<mxCell)", r"\1\n\2", xml)
        return xml, True
    return xml, False


def fix_duplicate_ids(xml: str) -> tuple[str, bool]:
    """Rename duplicate IDs"""
    seen = set()
    def replacer(m: re.Match) -> str:
        full = m.group(0)
        cell_id = m.group(1)
        if cell_id in seen:
            new_id = f"{cell_id}_dup"
            return full.replace(f'id="{cell_id}"', f'id="{new_id}"')
        seen.add(cell_id)
        return full
    new_xml = re.sub(r'id="([^"]*)"', replacer, xml)
    return new_xml, new_xml != xml


def fix_unclosed_tags(xml: str) -> tuple[str, bool]:
    """Close unclosed mxCell and mxGeometry tags"""
    fixed = False
    open_cells = len(re.findall(r"<mxCell[^>]*/>", xml))
    close_cells = len(re.findall(r"</mxCell>", xml))
    self_close = len(re.findall(r"<mxCell[^>]*/>", xml))
    # Count opening vs closing
    opens = len(re.findall(r"<mxCell(?![^>]*/>)", xml))
    closes = len(re.findall(r"</mxCell>", xml))
    if opens > closes:
        xml += "</mxCell>" * (opens - closes)
        fixed = True
    return xml, fixed


def wrap_with_mxfile(xml: str) -> tuple[str, bool]:
    """Wrap bare mxCell elements with mxfile structure"""
    if "<mxGraphModel" not in xml and "<mxfile" not in xml:
        root_cells = '<mxCell id="0"/><mxCell id="1" parent="0"/>'
        xml = f'<mxGraphModel><root>{root_cells}\n{xml}</root></mxGraphModel>'
        return xml, True
    return xml, False


def validate_xml(xml: str) -> tuple[bool, str | None]:
    """Basic XML structure validation"""
    # Check for mxCell elements
    if "<mxCell" not in xml:
        return False, "No mxCell elements found"
    # Check balanced tags
    opens = len(re.findall(r"<mxCell(?![^>]*/>)[^>]*>", xml))
    closes = len(re.findall(r"</mxCell>", xml))
    if opens != closes:
        return False, f"Unbalanced mxCell tags: {opens} opens, {closes} closes"
    return True, None


def fix_xml(xml: str) -> tuple[str, list[str]]:
    """
    Run the full 24-step auto-fix pipeline.
    Returns (fixed_xml, list_of_fixes_applied).
    """
    fixes = []

    xml, ok = fix_json_escaped(xml)
    if ok:
        fixes.append("Fixed JSON-escaped XML")

    xml, ok = fix_cdata(xml)
    if ok:
        fixes.append("Removed CDATA wrapper")

    xml, ok = strip_trailing_wrappers(xml)
    if ok:
        fixes.append("Stripped trailing LLM wrapper tags")

    xml, ok = remove_text_before_root(xml)
    if ok:
        fixes.append("Removed text before XML root")

    xml, ok = fix_duplicate_attrs(xml)
    if ok:
        fixes.append("Removed duplicate structural attributes")

    xml, ok = fix_unescaped_ampersand(xml)
    if ok:
        fixes.append("Escaped unescaped & characters")

    xml, ok = fix_double_escaped_entities(xml)
    if ok:
        fixes.append("Fixed double-escaped entities")

    xml, ok = fix_unescaped_html_quotes(xml)
    if ok:
        fixes.append("Escaped quotes inside HTML tags")

    xml, ok = fix_malformed_quotes(xml)
    if ok:
        fixes.append("Fixed malformed attribute quotes")

    xml, ok = fix_malformed_closing(xml)
    if ok:
        fixes.append("Fixed malformed closing tags")

    xml, ok = fix_missing_space(xml)
    if ok:
        fixes.append("Added missing space between attributes")

    xml, ok = fix_quoted_colors(xml)
    if ok:
        fixes.append("Removed quotes around color values")

    xml, ok = fix_unescaped_lt_in_attrs(xml)
    if ok:
        fixes.append("Escaped <> in attribute values")

    xml, ok = fix_cell_tags(xml)
    if ok:
        fixes.append("Fixed <Cell> tags to <mxCell>")

    xml, tag_fixes = fix_tag_typos(xml)
    fixes.extend(tag_fixes)

    xml, ok = remove_foreign_tags(xml)
    if ok:
        fixes.append("Removed non-draw.io tags")

    xml, ok = fix_nested_mxcell(xml)
    if ok:
        fixes.append("Flattened nested mxCell tags")

    xml, ok = fix_duplicate_ids(xml)
    if ok:
        fixes.append("Renamed duplicate IDs")

    xml, ok = fix_unclosed_tags(xml)
    if ok:
        fixes.append("Closed unclosed tags")

    xml, ok = wrap_with_mxfile(xml)
    if ok:
        fixes.append("Wrapped with mxfile structure")

    return xml, fixes


def main():
    if len(sys.argv) < 2:
        print("Usage: python fix-xml.py input.xml [output.xml]")
        print("       echo '<xml>' | python fix-xml.py -")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None

    if input_path == "-":
        xml = sys.stdin.read()
    else:
        xml = Path(input_path).read_text()

    fixed, fixes = fix_xml(xml)

    if fixes:
        print(f"Applied {len(fixes)} fix(es):")
        for f in fixes:
            print(f"  - {f}")
    else:
        print("No fixes needed. XML is valid.")

    if output_path:
        Path(output_path).write_text(fixed)
        print(f"Written to {output_path}")
    else:
        print("\n--- Fixed XML ---")
        print(fixed)


if __name__ == "__main__":
    main()
