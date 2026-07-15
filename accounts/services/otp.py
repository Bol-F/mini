import secrets
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.utils import timezone

from accounts.models import Account, EmailVerificationOTP


def send_otp(account):
    code = str(secrets.randbelow(900000) + 100000)

    EmailVerificationOTP.objects.update_or_create(
        account=account,
        defaults={
            "code_hash": make_password(code),
            "expires_at": timezone.now() + timedelta(minutes=10),
            "attempts": 0,
        },
    )

    send_mail(
        subject="Email verification",
        message=f"Your verification code is: {code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[account.email],
    )


def verify_otp(email, code):
    account = Account.objects.filter(
        email__iexact=email,
    ).first()

    if account is None:
        raise ValueError("Invalid email or code.")

    if account.is_email_verified:
        raise ValueError("Email is already verified.")

    otp = EmailVerificationOTP.objects.filter(
        account=account,
    ).first()

    if otp is None:
        raise ValueError("Invalid email or code.")

    if otp.expires_at < timezone.now():
        otp.delete()
        raise ValueError("Code has expired.")

    if not check_password(code, otp.code_hash):
        otp.attempts += 1
        otp.save(update_fields=["attempts"])

        raise ValueError("Invalid email or code.")

    account.is_email_verified = True
    account.save(update_fields=["is_email_verified"])

    otp.delete()

    return account