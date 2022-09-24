r"""Utility to handle the big lists of options that become our constants."""

from typing import List, Callable, Optional


def multiline_text_to_list(
        multiline: str,
        mapping: Optional[Callable[[str], str]] = None) -> List[str]:
    """Convert a plain-text list to a python list.

    List entries should be:
     - Trimmed of whitespace
     - Unique
     - Non-empty

    Additionally a map can be applied by passing one as the second argument.
    """
    lines = multiline.split("\n")  # Break into lines
    lines = map(lambda s: s.strip().lower(), lines)# Trim whitespace
    lines = filter_unique_preserving_order(lines)  # Uniqueness
    lines = filter(lambda s: len(s) > 0, lines)  # Remove empty
    if mapping is not None:
        lines = map(mapping, lines)  # Apply mapping if provided
    lines = map(lambda s: s.lower(), lines) # To lowercase
    return list(lines)


def filter_unique_preserving_order(ordered_list: List[str]) -> List[str]:
    """Remove duplicates from a list, preserving order."""
    found = []
    for entry in ordered_list:
        if entry not in found:
            found.append(entry)
    return found


"""
The MIT License (MIT)

Copyright © 2022 Hex Miller-Bakewell

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
