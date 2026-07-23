from django.db import migrations, models


def copy_existing_roles(apps, schema_editor):
    Account = apps.get_model("accounts", "Account")
    UserRole = apps.get_model("accounts", "UserRole")

    # Higher roles are copied later so they win if an account had many roles.
    for role_name in ("user", "moderator", "admin"):
        account_ids = UserRole.objects.filter(
            role__name__iexact=role_name,
        ).values_list("account_id", flat=True)
        Account.objects.filter(id__in=account_ids).update(role=role_name)

    Account.objects.filter(is_superuser=True).update(role="admin")


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_action_resource_role_account_deleted_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="role",
            field=models.CharField(
                choices=[
                    ("admin", "Admin"),
                    ("moderator", "Moderator"),
                    ("user", "User"),
                ],
                default="user",
                max_length=20,
            ),
        ),
        migrations.RunPython(
            copy_existing_roles,
            migrations.RunPython.noop,
        ),
        migrations.DeleteModel(name="RolePermission"),
        migrations.DeleteModel(name="UserRole"),
        migrations.DeleteModel(name="AccessPermission"),
        migrations.DeleteModel(name="Action"),
        migrations.DeleteModel(name="Resource"),
        migrations.DeleteModel(name="Role"),
    ]
