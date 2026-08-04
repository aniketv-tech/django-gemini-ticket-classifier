from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import SupportTicket
from .agent import classify_and_draft_agent

@api_view(['GET', 'POST'])
def ticket_api(request):
    if request.method == 'GET':
        tickets = SupportTicket.objects.all().order_by('-created_at')
        return Response([{
            "id": t.id,
            "message": t.message,
            "category": t.category,
            "priority": t.priority,
            "auto_reply": t.auto_reply,
            "created_at": t.created_at
        } for t in tickets], status=status.HTTP_200_OK)

    if request.method == 'POST':
        message = request.data.get('message')
        if not message:
            return Response({"error": "Field 'message' is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Run Local Classifier Agent
        agent_output = classify_and_draft_agent(message)

        # Save to Database
        ticket = SupportTicket.objects.create(
            message=message,
            category=agent_output["category"],
            priority=agent_output["priority"],
            auto_reply=agent_output["auto_reply"]
        )

        return Response({
            "id": ticket.id,
            "message": ticket.message,
            "category": ticket.category,
            "priority": ticket.priority,
            "auto_reply": ticket.auto_reply,
            "created_at": ticket.created_at
        }, status=status.HTTP_201_CREATED)