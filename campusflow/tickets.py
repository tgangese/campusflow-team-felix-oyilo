"""
Engineer A: Gangese Terkula Felix
Responsibility: ticket creation, validation, priority engine
"""
ALLOWED_CATEGORIES = ["network", "hardware", "software", "other"]
ALLOWED_URGENCIES = ["low", "medium", "high"]
PRIORITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}

def calculate_priority(urgency: str, affected_users: int) -> str:
    """Calculate priority IN ORDER specified — first match wins."""
    u = urgency.lower().strip()
    # RULE 1: high AND >=10 -> critical
    if u == "high" and affected_users >= 10:
        return "critical"
    # RULE 2: high OR >=10 -> high
    if u == "high" or affected_users >= 10:
        return "high"
    # RULE 3: medium OR >=3 -> medium
    if u == "medium" or affected_users >= 3:
        return "medium"
    # RULE 4: rest -> low
    return "low"

def normalize_category(cat: str) -> str:
    if not cat or not cat.strip():
        raise ValueError("Category must not be blank")
    c = cat.strip().lower()
    if c not in ALLOWED_CATEGORIES:
        raise ValueError(f"Invalid category '{cat}'. Allowed: {', '.join(ALLOWED_CATEGORIES)}")
    return c

def normalize_urgency(urg: str) -> str:
    if not urg or not urg.strip():
        raise ValueError("Urgency must not be blank")
    u = urg.strip().lower()
    if u not in ALLOWED_URGENCIES:
        raise ValueError(f"Invalid urgency '{urg}'. Allowed: {', '.join(ALLOWED_URGENCIES)}")
    return u

def validate_title(title: str) -> str:
    if not title or not title.strip():
        raise ValueError("Title must not be blank")
    return title.strip()

def validate_affected_users(value) -> int:
    # Reject bool — bool is subclass of int in Python
    if isinstance(value, bool):
        raise ValueError("affected_users must be a positive integer")
    if isinstance(value, str):
        v = value.strip()
        if not v.isdigit():
            raise ValueError("affected_users must be a positive integer (not zero, negative, decimal, or text)")
        value = int(v)
    if not isinstance(value, int):
        raise ValueError("affected_users must be a positive integer")
    if value <= 0:
        raise ValueError("affected_users must be > 0 (zero not allowed)")
    return value

def get_next_id(tickets) -> str:
    max_num = 0
    for t in tickets:
        tid = t.get("id", "")
        if tid.startswith("T") and tid[1:].isdigit():
            num = int(tid[1:])
            if num > max_num:
                max_num = num
    return f"T{max_num + 1:03d}"

def create_ticket(tickets, title, category, urgency, affected_users) -> dict:
    """Validate, calculate priority, assign ID, store."""
    clean_title = validate_title(title)
    clean_cat = normalize_category(category)
    clean_urg = normalize_urgency(urgency)
    clean_users = validate_affected_users(affected_users)

    priority = calculate_priority(clean_urg, clean_users)
    new_id = get_next_id(tickets)

    ticket = {
        "id": new_id,
        "title": clean_title,
        "category": clean_cat,
        "urgency": clean_urg,
        "affected_users": clean_users,
        "priority": priority,
        "status": "open",
        "assigned_to": None
    }
    tickets.append(ticket)
    return ticket

def find_ticket(tickets, ticket_id: str):
    if not ticket_id or not ticket_id.strip():
        raise ValueError("Ticket ID must not be blank")
    tid = ticket_id.strip().upper()
    for t in tickets:
        if t["id"].upper() == tid:
            return t
    return None