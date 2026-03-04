"""Unit tests for interaction filtering logic - edge cases and boundary values."""

from app.models.interaction import InteractionLog
from app.routers.interactions import _filter_by_item_id


def _make_log(id: int, learner_id: int, item_id: int, kind: str = "attempt") -> InteractionLog:
    return InteractionLog(id=id, learner_id=learner_id, item_id=item_id, kind=kind)


# KEPT: tests boundary value item_id=0, not covered elsewhere
def test_filter_with_zero_item_id() -> None:
    """Test filtering with item_id=0 (boundary value)."""
    interactions = [_make_log(1, 1, 0), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, 0)
    assert len(result) == 1
    assert result[0].id == 1


# KEPT: tests negative item_id, important boundary case
def test_filter_with_negative_item_id() -> None:
    """Test filtering with negative item_id (boundary value)."""
    interactions = [_make_log(1, 1, -1), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, -1)
    assert len(result) == 1
    assert result[0].id == 1


# KEPT: tests large item_id value, good for integer overflow scenarios
def test_filter_with_large_item_id() -> None:
    """Test filtering with large item_id value."""
    large_id = 999999
    interactions = [_make_log(1, 1, large_id), _make_log(2, 2, 1)]
    result = _filter_by_item_id(interactions, large_id)
    assert len(result) == 1
    assert result[0].id == 1


# KEPT: tests multiple matches with same item_id, good coverage
def test_filter_multiple_matches_same_item_id() -> None:
    """Test filtering returns all interactions with matching item_id."""
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 1),
        _make_log(3, 3, 1),
        _make_log(4, 1, 2),
    ]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 3
    assert all(i.item_id == 1 for i in result)


# KEPT: tests no matches scenario, important for empty results
def test_filter_no_matches_returns_empty() -> None:
    """Test filtering with item_id that has no matches."""
    interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2)]
    result = _filter_by_item_id(interactions, 999)
    assert result == []


# KEPT: tests single interaction matching
def test_filter_single_interaction_matching() -> None:
    """Test filtering single interaction list with matching item_id."""
    interactions = [_make_log(1, 1, 5)]
    result = _filter_by_item_id(interactions, 5)
    assert len(result) == 1
    assert result[0].id == 1


# KEPT: tests single interaction not matching
def test_filter_single_interaction_not_matching() -> None:
    """Test filtering single interaction list with non-matching item_id."""
    interactions = [_make_log(1, 1, 5)]
    result = _filter_by_item_id(interactions, 10)
    assert result == []


# KEPT: tests order preservation, important for consistent behavior
def test_filter_preserves_original_order() -> None:
    """Test that filtering preserves the order of interactions."""
    interactions = [
        _make_log(1, 1, 1),
        _make_log(2, 2, 2),
        _make_log(3, 3, 1),
        _make_log(4, 4, 1),
        _make_log(5, 5, 2),
    ]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 3
    assert [i.id for i in result] == [1, 3, 4]


# DISCARDED: duplicates existing test_filter_returns_all_when_item_id_is_none in original test_interactions.py
# def test_filter_with_none_item_id_preserves_all_interactions() -> None:
#     """Test that None item_id returns all interactions unchanged."""
#     interactions = [_make_log(1, 1, 1), _make_log(2, 2, 2), _make_log(3, 3, 3)]
#     result = _filter_by_item_id(interactions, None)
#     assert result == interactions
#     assert len(result) == 3


# KEPT: tests different kinds with same item_id, good for kind filtering scenarios
def test_filter_with_different_kinds_same_item_id() -> None:
    """Test filtering interactions with different kinds but same item_id."""
    interactions = [
        _make_log(1, 1, 1, kind="view"),
        _make_log(2, 1, 1, kind="attempt"),
        _make_log(3, 1, 1, kind="complete"),
        _make_log(4, 1, 2, kind="view"),
    ]
    result = _filter_by_item_id(interactions, 1)
    assert len(result) == 3
    assert all(i.item_id == 1 for i in result)
    assert [i.kind for i in result] == ["view", "attempt", "complete"]