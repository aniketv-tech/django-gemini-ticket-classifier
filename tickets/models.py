from django.db import models

class SupportTicket(models.Model):
    message = models.TextField()
    category = models.CharField(max_length=50)
    priority = models.CharField(max_length=20)
    auto_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.priority}] {self.category} - Ticket #{self.id}"