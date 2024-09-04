import pytest
from main import bot

@pytest.mark.asyncio
async def test_hello_response():
    message = type('Message', (), {'text': '安安', 'chat': type('Chat', (), {'id': 123})})()
    
    async def mock_send_message(chat_id, text):
        assert chat_id == 123
        assert text == "安安!"
    
    bot.send_message = mock_send_message
    
    await handle_hello(message)