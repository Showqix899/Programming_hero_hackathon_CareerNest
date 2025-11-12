
def is_admin(user):
    """Check if the user has admin privileges."""
    return user.is_authenticated and user.is_superuser or user.is_staff