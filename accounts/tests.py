from types import SimpleNamespace

from django.contrib.auth.models import AnonymousUser
from django.test import SimpleTestCase, TestCase

from accounts.models import Account
from accounts.permissions import IsAdmin, IsAdminOrModerator
from accounts.serializers.account import AccountSerializer
from accounts.serializers.register import RegisterSerializer


class AccountRoleTests(SimpleTestCase):
    def test_project_has_three_roles(self):
        self.assertEqual(
            [value for value, _ in Account.Role.choices],
            ["admin", "moderator", "user"],
        )

    def test_user_is_the_default_role(self):
        role_field = Account._meta.get_field("role")

        self.assertEqual(role_field.get_default(), Account.Role.USER)

    def test_role_cannot_be_selected_during_registration(self):
        self.assertNotIn("role", RegisterSerializer().fields)

    def test_role_is_returned_by_account_serializer(self):
        account = Account(
            email="user@example.com",
            username="user_1",
            role=Account.Role.MODERATOR,
        )

        self.assertEqual(
            AccountSerializer(account).data["role"],
            Account.Role.MODERATOR,
        )


class RolePermissionTests(SimpleTestCase):
    def test_admin_permission_only_allows_admin(self):
        admin_request = self._request_for(Account.Role.ADMIN)
        moderator_request = self._request_for(Account.Role.MODERATOR)

        self.assertTrue(IsAdmin().has_permission(admin_request, None))
        self.assertFalse(IsAdmin().has_permission(moderator_request, None))

    def test_moderator_permission_also_allows_admin(self):
        admin_request = self._request_for(Account.Role.ADMIN)
        moderator_request = self._request_for(Account.Role.MODERATOR)
        user_request = self._request_for(Account.Role.USER)

        permission = IsAdminOrModerator()

        self.assertTrue(permission.has_permission(admin_request, None))
        self.assertTrue(permission.has_permission(moderator_request, None))
        self.assertFalse(permission.has_permission(user_request, None))

    def test_role_permissions_require_authentication(self):
        request = SimpleNamespace(user=AnonymousUser())

        self.assertFalse(IsAdmin().has_permission(request, None))
        self.assertFalse(
            IsAdminOrModerator().has_permission(request, None)
        )

    @staticmethod
    def _request_for(role):
        account = Account(
            email=f"{role}@example.com",
            username=f"{role}_1",
            role=role,
        )

        return SimpleNamespace(user=account)


class RegistrationRoleTests(TestCase):
    def test_registration_always_creates_a_user(self):
        serializer = RegisterSerializer(
            data={
                "email": "new-user@example.com",
                "first_name": "New",
                "last_name": "User",
                "password": "A-very-strong-password-2026!",
                "password2": "A-very-strong-password-2026!",
                "role": Account.Role.ADMIN,
            }
        )
        serializer.is_valid(raise_exception=True)

        account = serializer.save()

        self.assertEqual(account.role, Account.Role.USER)

    def test_superuser_is_also_an_admin(self):
        account = Account.objects.create_superuser(
            username="site_admin",
            email="admin@example.com",
            password="A-very-strong-password-2026!",
        )

        self.assertEqual(account.role, Account.Role.ADMIN)
