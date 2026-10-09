# Design Decisions - Engineer A (Felix)

1. Priority Engine Order
Decision: Check high AND >=10 (critical) BEFORE high OR >=10 (high)
Reason: Critical is subset of High. If High checked first, Critical unreachable.
Result: high+12 = critical, not high.

2. ID Generation
Decision: Parse max numeric ID, not len(tickets)+1
Reason: Ensures uniqueness after reload and deletions.
Test: test_id_unique_after_reload

3. Validation Strictness
Decision: Reject blank title, zero/negative users, float users, invalid category.
Reason: Prevent garbage data. Fail fast with ValueError.

4. Storage - Missing vs Corrupted
Decision: Missing file -> return [], Corrupted -> raise ValueError
Reason: Missing = expected first run, corrupted = data loss risk must not erase.

5. Ticket Structure
Decision: Dict with id, title, category, urgency, affected_users, priority, status=open, assigned_to=None
Reason: JSON-serializable, compatible with Engineer B workflow.

6. Package Structure
Decision: Use __init__.py to make package importable
Reason: Allows from campusflow.tickets import in CLI and tests.