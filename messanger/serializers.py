from rest_framework import serializers

from .models import Message, Conversation
from django.db.models import Q


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'

    messages = serializers.SerializerMethodField(method_name='get_messages')

    def get_messages(self, obj):
        conversation_recieved = Conversation.objects.get(owner=obj.with_user)
        messages_sent = Message.objects.filter(
            owner=obj.owner, conversation=obj.conversation)
        messages_recieved = Message.objects.filter(
            owner=obj.with_user, conversation=conversation_recieved)

        # //////TODO concatinate the two querysets in a list.
        # and sort the list by timestamp NOTE!important
        # then serialize the result and return it.
