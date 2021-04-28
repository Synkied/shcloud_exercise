"""
Admins permissions
"""


class AdminBackend():
    """
    Handles the permissions for admin users
    """

    def has_perm(self, user, perm, obj=None):
        """
        Perform the permission check for admins.
        Grant all privileges if user.is_admin.
        """
        if not user.is_admin:
            return False

        return True
