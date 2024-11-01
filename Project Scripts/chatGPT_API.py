from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, BotFrameworkAdapter
from aiohttp import web
import os

class MyBot(ActivityHandler):
    async def on_message(self, turn_context: TurnContext):
        user_message = turn_context.activity.text
        response = f"You said: {user_message}"
        await turn_context.send_activity(MessageFactory.text(response))

async def handle_messages(req):
    body = await req.json()
    activity = TurnContext.deserialize_activity(body)
    await bot_adapter.process_activity(activity, bot)
    return web.Response(status=200)

# Set up the bot and adapter
bot = MyBot()
bot_adapter = BotFrameworkAdapter(app_id=os.getenv("MicrosoftAppId"), app_password=os.getenv("MicrosoftAppPassword"))

app = web.Application()
app.router.add_post("/api/messages", handle_messages)

if __name__ == "__main__":
    web.run_app(app, host='127.0.0.1', port=3978)  # Ensure you are using 127.0.0.1
