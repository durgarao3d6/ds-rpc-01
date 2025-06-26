# Fake in-memory users
USERS = {
    "alice": "finance",
    "bob": "hr",
    "carol": "executive",
    "dave": "employee"
}

# Roles and what folders they can access
ROLES_PERMISSIONS = {
    "finance": ["finance", "general"],
    "hr": ["hr", "general"],
    "marketing": ["marketing", "general"],
    "engineering": ["engineering", "general"],
    "executive": ["finance", "hr", "marketing", "engineering", "general"],
    "employee": ["general"]
}

def get_user_role(username: str) -> str:
    return USERS.get(username)

def get_allowed_departments(role: str) -> list[str]:
    return ROLES_PERMISSIONS.get(role, [])
