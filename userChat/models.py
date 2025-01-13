from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now
import uuid

# Extend AbstractUser for custom fields
class UserEx(User):
    ROLES = (
        ('guest', 'Guest'),
        ('registered', 'Registered User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='guest')
    tokens = models.PositiveIntegerField(default=0)  # User's token balance
    def __str__(self):
        return self.username
    def deduct_tokens(self, amount):
        if self.tokens >= amount:
            self.tokens -= amount
            self.save()
            return True
        return False
# Token packages for purchase
class TokenPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    tokens = models.PositiveIntegerField()  # Number of tokens in the package
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Package price
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.tokens} Tokens"
# Payment and transaction tracking
class Payment(models.Model):
    user = models.ForeignKey(UserEx, on_delete=models.CASCADE, related_name='payments')
    token_package = models.ForeignKey(TokenPackage, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='pending')  # e.g., pending, completed, failed
    payment_date = models.DateTimeField(default=now)
    def __str__(self):
        return f"Payment {self.id} - {self.status}"
#========== GuestSession Data =================
class GuestSession(models.Model):
    guest_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tokens = models.PositiveIntegerField(default=5)  # Default tokens for guests
    created_at = models.DateTimeField(auto_now_add=True)
    def deduct_tokens(self, amount):
        if self.tokens >= amount:
            self.tokens -= amount
            self.save()
            return True
        return False
    def __str__(self):
        if self.user:
            return f"Chat Session for User {self.user.username}"
        return f"Chat Session for Guest {self.guest_session.guest_id}"
#========== Chat session to log interactions =============
class ChatSession(models.Model):
    user = models.ForeignKey(UserEx, on_delete=models.CASCADE,null=True, blank=True,related_name='chat_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    token_spent = models.PositiveIntegerField(default=0)  # Tokens spent in this session
    def __str__(self):
        return f"Session {self.id} for {self.user.username}"
#========= Chat message log ===============
class ChatMessage(models.Model):
    ROLES = (
    ('user', 'User'),
    ('bot', 'Bot'),
)
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Message {self.id} - {self.role}"
#========= service redirections ===========
class ServiceRedirect(models.Model):
    keywords = models.CharField(max_length=255)  # Comma-separated keywords
    service_url = models.URLField()  # Link to the service page

    def __str__(self):
        return f"Redirect: {self.keywords}"
#======== Fine-tuning datasets for OpenAI ========
class FineTuningData(models.Model):
    prompt = models.TextField()
    completion = models.TextField()
    def __str__(self):
        return f"Fine-Tuning Entry {self.id}"
