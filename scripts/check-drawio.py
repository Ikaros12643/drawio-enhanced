#!/usr/bin/env python3
"""Structural checks for draw.io .drawio files.

This script intentionally avoids visual validation. It checks whether the file is
well-formed enough to open and whether common mxCell references are consistent.
"""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def local_name(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[1]
    return tag


def find_children_by_name(node: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in list(node) if local_name(child.tag) == name]


def find_descendants_by_name(node: ET.Element, name: str) -> list[ET.Element]:
    return [child for child in node.iter() if local_name(child.tag) == name]


def has_geometry(cell: ET.Element, require_relative: bool = False) -> bool:
    for child in find_children_by_name(cell, "mxGeometry"):
        if child.attrib.get("as") != "geometry":
            continue
        if require_relative and child.attrib.get("relative") != "1":
            continue
        return True
    return False


def check_file(path: Path) -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []
    stats = {
        "diagrams": 0,
        "cells": 0,
        "vertices": 0,
        "edges": 0,
    }

    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        return [f"XML parse error: {exc}"], warnings, stats
    except OSError as exc:
        return [f"Cannot read file: {exc}"], warnings, stats

    root = tree.getroot()
    models_by_diagram: list[tuple[int, ET.Element]] = []
    if local_name(root.tag) == "mxfile":
        diagrams = find_children_by_name(root, "diagram")
        stats["diagrams"] = len(diagrams)
        if not diagrams:
            errors.append("No diagram element found")
        for diagram_index, diagram in enumerate(diagrams, start=1):
            models = find_children_by_name(diagram, "mxGraphModel")
            if not models:
                errors.append(f"Diagram {diagram_index} has no mxGraphModel")
                continue
            for model in models:
                models_by_diagram.append((diagram_index, model))
    elif local_name(root.tag) == "mxGraphModel":
        stats["diagrams"] = 1
        models_by_diagram.append((1, root))
        warnings.append("Standalone mxGraphModel root detected; full mxfile wrapper is preferred for .drawio delivery")
    else:
        errors.append(
            f"Root element should be mxfile or mxGraphModel, found {local_name(root.tag)!r}"
        )

    all_ids: dict[str, str] = {}
    duplicate_ids: set[str] = set()
    missing_ids = 0

    for diagram_index, model in models_by_diagram:
        roots = find_children_by_name(model, "root")
        if not roots:
            errors.append(f"Diagram {diagram_index} has no root")
            continue

        for graph_root in roots:
            cells = find_descendants_by_name(graph_root, "mxCell")
            for cell in cells:
                stats["cells"] += 1
                cell_id = cell.attrib.get("id")
                if not cell_id:
                    missing_ids += 1
                    continue
                if cell_id in all_ids:
                    duplicate_ids.add(cell_id)
                all_ids[cell_id] = f"diagram {diagram_index}"

    if missing_ids:
        errors.append(f"{missing_ids} mxCell element(s) missing id")
    for cell_id in sorted(duplicate_ids):
        errors.append(f"Duplicate mxCell id: {cell_id}")

    known_ids = set(all_ids)

    for diagram_index, model in models_by_diagram:
        for cell in find_descendants_by_name(model, "mxCell"):
            cell_id = cell.attrib.get("id", "<missing id>")
            is_vertex = cell.attrib.get("vertex") == "1"
            is_edge = cell.attrib.get("edge") == "1"

            if is_vertex:
                stats["vertices"] += 1
                if not has_geometry(cell):
                    errors.append(f"Vertex {cell_id} in diagram {diagram_index} missing mxGeometry")

            if is_edge:
                stats["edges"] += 1
                source = cell.attrib.get("source")
                target = cell.attrib.get("target")
                if not source:
                    errors.append(f"Edge {cell_id} in diagram {diagram_index} missing source")
                elif source not in known_ids:
                    errors.append(f"Edge {cell_id} source not found: {source}")
                if not target:
                    errors.append(f"Edge {cell_id} in diagram {diagram_index} missing target")
                elif target not in known_ids:
                    errors.append(f"Edge {cell_id} target not found: {target}")
                if not has_geometry(cell, require_relative=True):
                    errors.append(
                        f"Edge {cell_id} in diagram {diagram_index} missing relative mxGeometry"
                    )

    if stats["vertices"] and stats["edges"] > int(stats["vertices"] * 1.5) + 2:
        warnings.append(
            f"High edge count: {stats['edges']} edges for {stats['vertices']} vertices; consider simplifying relationships"
        )

    return errors, warnings, stats


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Check draw.io .drawio XML structure")
    parser.add_argument("files", nargs="+", help=".drawio files to check")
    args = parser.parse_args(argv)

    exit_code = 0
    for file_name in args.files:
        path = Path(file_name)
        if not path.exists():
            print(f"ERROR {path}: file does not exist")
            exit_code = 2
            continue
        if not path.is_file():
            print(f"ERROR {path}: not a file")
            exit_code = 2
            continue

        errors, warnings, stats = check_file(path)
        status = "OK" if not errors else "FAIL"
        print(f"{status} {path}")
        print(
            f"- diagrams: {stats['diagrams']}\n"
            f"- cells: {stats['cells']}\n"
            f"- vertices: {stats['vertices']}\n"
            f"- edges: {stats['edges']}"
        )
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
        if errors:
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
