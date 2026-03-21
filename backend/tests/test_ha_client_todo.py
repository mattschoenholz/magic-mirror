"""Unit tests for HA todo response normalization."""

from __future__ import annotations

import pytest

from mirror_backend.ha_client import _extract_todo_items


@pytest.mark.parametrize(
    ("payload", "expected_titles"),
    [
        ([{"title": "A", "status": "needs_action"}], ["A"]),
        ([{"summary": "S", "completed": True}], ["S"]),
        (
            {"todo.elliot": {"items": [{"title": "E", "status": "completed"}]}},
            ["E"],
        ),
        (
            {"items": [{"name": "N", "status": "needs_action"}]},
            ["N"],
        ),
        (
            {"response": {"items": [{"subject": "Sub"}]}},
            ["Sub"],
        ),
        (
            {
                "service_response": {
                    "todo.elliot": {
                        "items": [{"summary": "From wrapper", "status": "needs_action"}]
                    }
                }
            },
            ["From wrapper"],
        ),
        (
            {
                "other_list": {
                    "items": [{"title": "Fallback", "status": "needs_action"}]
                }
            },
            ["Fallback"],
        ),
        ({}, []),
        (None, []),
    ],
)
def test_extract_todo_items_shapes(
    payload: object, expected_titles: list[str]
) -> None:
    items = _extract_todo_items(payload, "todo.elliot")
    titles = [
        i.get("title") or i.get("summary") or i.get("name") or i.get("subject")
        for i in items
    ]
    assert titles == expected_titles
