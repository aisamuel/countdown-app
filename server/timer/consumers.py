import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import CountdownTimer

active_timers = {}  

class TimerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handles WebSocket connection"""
        self.event_id = self.scope['url_route']['kwargs']['event_id']
        self.group_name = f"timer_{self.event_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        if self.event_id not in active_timers:
            timer_obj = await self.get_timer_obj(int(self.event_id))
            active_timers[self.event_id] = {
                "remaining_time": timer_obj.total_seconds(),
                "is_running": False,
                "countdown_task": None,
            }

        # Send initial timer state
        await self.send_timer_update()

    async def disconnect(self, close_code):
        """Handles WebSocket disconnection"""
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        """Handles incoming WebSocket messages"""
        data = json.loads(text_data)
        command = data.get("command")

        if command == "set_time":
            await self.set_time(data)
        elif command == "start_pause":
            await self.toggle_start_pause()
        elif command == "reset":
            await self.reset_timer()
        elif command == "update_time":
            await self.update_time(data)

    async def set_time(self, data):
        """Sets a new timer duration"""
        h, m, s = data.get("hours", 0), data.get("minutes", 0), data.get("seconds", 0)
        new_time = h * 3600 + m * 60 + s

        if new_time <= 0:
            return

        await self.update_timer_in_db(h, m, s)
        active_timers[self.event_id]["remaining_time"] = new_time
        active_timers[self.event_id]["is_running"] = False
        await self.send_timer_update()

    async def toggle_start_pause(self):
        """Starts or pauses the countdown"""
        state = active_timers[self.event_id]

        if not state["is_running"]:
            state["is_running"] = True
            if not state["countdown_task"]:
                state["countdown_task"] = asyncio.create_task(self.run_countdown())
        else:
            state["is_running"] = False
            if state["countdown_task"]:
                state["countdown_task"].cancel()
                state["countdown_task"] = None

        await self.send_timer_update()

    async def reset_timer(self):
        """Resets the countdown timer"""
        timer_obj = await self.get_timer_obj(int(self.event_id))
        state = active_timers[self.event_id]

        if state["countdown_task"]:
            state["countdown_task"].cancel()
            state["countdown_task"] = None

        state["is_running"] = False
        state["remaining_time"] = timer_obj.total_seconds()
        await self.send_timer_update()

    async def update_time(self, data):
        """Syncs timer with frontend"""
        remaining_time = data.get("remaining_time")
        if remaining_time is not None:
            active_timers[self.event_id]["remaining_time"] = remaining_time
            await self.send_timer_update()

    async def run_countdown(self):
        """Runs the countdown process"""
        try:
            while active_timers[self.event_id]["remaining_time"] > 0 and active_timers[self.event_id]["is_running"]:
                active_timers[self.event_id]["remaining_time"] -= 1
                await self.send_timer_update()
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
        finally:
            active_timers[self.event_id]["countdown_task"] = None
            active_timers[self.event_id]["is_running"] = False
            await self.send_timer_update()

    async def send_timer_update(self):
        """Broadcasts the current timer state to all clients"""
        state = active_timers[self.event_id]
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "timer_update",
                "remaining_time": state["remaining_time"],
                "is_running": state["is_running"]
            }
        )

    async def timer_update(self, event):
        """Sends an update to the frontend"""
        await self.send(json.dumps({
            "type": "timer_update",
            "remaining_time": event["remaining_time"],
            "is_running": event["is_running"]
        }))

    @database_sync_to_async
    def get_timer_obj(self, event_id):
        """Fetches timer from the database"""
        try:
            return CountdownTimer.objects.get(pk=event_id)
        except CountdownTimer.DoesNotExist:
            return CountdownTimer.objects.create(event_name="Untitled Event")

    @database_sync_to_async
    def update_timer_in_db(self, h, m, s):
        """Updates the timer in the database"""
        timer_obj = CountdownTimer.objects.get(pk=self.event_id)
        timer_obj.hours = h
        timer_obj.minutes = m
        timer_obj.seconds = s
        timer_obj.save()
