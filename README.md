# Mini account API

Each account has one of three roles:

- `admin` - for administrative endpoints
- `moderator` - for moderation endpoints
- `user` - the default role for every new registration

The role is stored directly on `Account` to keep the code simple:

```python
account.role = Account.Role.MODERATOR
account.save(update_fields=["role"])
```

The login and `/me/` responses include the account's role. Public registration
always creates a regular `user`, so a visitor cannot make themselves an admin.

For role-protected API views, use `IsAdmin` or `IsAdminOrModerator` from
`accounts.permissions`. Regular signed-in users can continue to use DRF's
standard `IsAuthenticated` permission.

A Django superuser is always stored with the `admin` role. The opposite is not
automatic: an application `admin` does not become a Django superuser.
