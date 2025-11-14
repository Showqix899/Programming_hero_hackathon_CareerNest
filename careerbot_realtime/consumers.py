import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import  Conversation, Message
from profiles.models import UserProfile
from .prompts import build_career_prompt
from .services import ask_gemini


class CareerBotConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        user = self.scope.get('user')
        if user and user.is_authenticated:
            await self.accept()
            await self.send_json({
                'type': 'connection.accepted',
                'message': 'Connected to CareerBot'
            })
        else:
            await self.close(code=4001)

    async def receive_json(self, content):
        """
        Expected input:
        {"type": "ask", "question": "...", "conversation_id": "..."}
        """
        msg_type = content.get('type')

        if msg_type == 'ask':
            question = content.get('question', '').strip()

            if not question:
                await self.send_json({
                    'type': 'error',
                    'message': 'Question is empty'
                })
                return

            # Fetch user
            user = self.scope['user']

            # Fetch profile
            try:
                profile = await database_sync_to_async(
                    lambda: UserProfile.objects.get(user=user)
                )()
            except UserProfile.DoesNotExist:
                await self.send_json({
                    'type': 'error',
                    'message': 'User profile not found'
                })
                return

            # Create new conversation
            conv = await database_sync_to_async(
                lambda: Conversation.objects.create(user=user)
            )()

            # Save user message
            await database_sync_to_async(
                lambda: Message.objects.create(
                    conversation=conv,
                    sender='user',
                    content=question
                )
            )()

            # Prepare prompt
            prompt = build_career_prompt(profile, question)

            # Call Gemini in sync thread
            answer = await database_sync_to_async(lambda: ask_gemini(prompt))()

            # Save bot answer
            await database_sync_to_async(
                lambda: Message.objects.create(
                    conversation=conv,
                    sender='bot',
                    content=answer
                )
            )()

            # Send answer to frontend
            await self.send_json({
                'type': 'answer',
                'conversation_id': str(conv.id),
                'answer': answer
            })

        else:
            await self.send_json({
                'type': 'error',
                'message': 'Unknown message type'
            })

    async def disconnect(self, close_code):
        # optional cleanup
        pass
