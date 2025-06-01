from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model"""
    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number']
        read_only_fields = ['user_id']

class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8,
        error_messages={
            'min_length': 'Password must be at least 8 characters long.'
        }
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['user_id', 'email', 'password', 'password_confirm', 
                 'first_name', 'last_name', 'phone_number']
        read_only_fields = ['user_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match.'
            })
        
        # Validate password strength
        try:
            validate_password(data['password'])
        except ValidationError as e:
            raise serializers.ValidationError({
                'password': list(e.messages)
            })
        
        return data

    def create(self, validated_data):
        # Remove password_confirm from the data
        validated_data.pop('password_confirm')
        
        # Create user with hashed password
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number', '')
        )
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user information"""
    current_password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'},
        min_length=8,
        error_messages={
            'min_length': 'Password must be at least 8 characters long.'
        }
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        required=False,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number',
                 'current_password', 'new_password', 'new_password_confirm']
        read_only_fields = ['email']

    def validate(self, data):
        # Check if user is trying to change password
        if 'new_password' in data:
            if 'current_password' not in data:
                raise serializers.ValidationError({
                    'current_password': 'Current password is required to set new password.'
                })
            
            if 'new_password_confirm' not in data:
                raise serializers.ValidationError({
                    'new_password_confirm': 'Please confirm your new password.'
                })
            
            # Check if new passwords match
            if data['new_password'] != data['new_password_confirm']:
                raise serializers.ValidationError({
                    'new_password_confirm': 'New passwords do not match.'
                })
            
            # Validate new password strength
            try:
                validate_password(data['new_password'])
            except ValidationError as e:
                raise serializers.ValidationError({
                    'new_password': list(e.messages)
                })
            
            # Verify current password
            if not self.instance.check_password(data['current_password']):
                raise serializers.ValidationError({
                    'current_password': 'Current password is incorrect.'
                })
        
        return data

    def update(self, instance, validated_data):
        # Handle password update
        if 'new_password' in validated_data:
            instance.set_password(validated_data.pop('new_password'))
            validated_data.pop('current_password', None)
            validated_data.pop('new_password_confirm', None)
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the Message model"""
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at', 'is_read']
        read_only_fields = ['message_id', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for the Conversation model"""
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at', 'updated_at']
        read_only_fields = ['conversation_id', 'created_at', 'updated_at']

class ConversationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new conversation"""
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=True
    )

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participant_ids']
        read_only_fields = ['conversation_id']

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids')
        conversation = Conversation.objects.create(**validated_data)
        
        # Add participants
        for user_id in participant_ids:
            try:
                user = User.objects.get(user_id=user_id)
                conversation.participants.add(user)
            except User.DoesNotExist:
                raise serializers.ValidationError(f"User with ID {user_id} does not exist")
        
        return conversation

class MessageCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new message"""
    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'message_body']
        read_only_fields = ['message_id']

    def validate(self, data):
        # Check if the sender is a participant in the conversation
        request = self.context.get('request')
        if request and request.user:
            if not data['conversation'].participants.filter(user_id=request.user.user_id).exists():
                raise serializers.ValidationError("You are not a participant in this conversation")
        return data
