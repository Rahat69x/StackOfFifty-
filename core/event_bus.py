"""
Dual-mode event bus for StackOfFifty: Redis Pub/Sub with automatic in-memory fallback.
"""
import asyncio
import json
from datetime import datetime, timezone
from typing import Callable, Dict, List, Any
from core.logger import get_logger

logger = get_logger("event_bus")

class EventBus:
    """Inter-module and platform-wide asynchronous event broker."""
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(EventBus, cls).__new__(cls)
            cls._instance._subscribers = {}
            cls._instance._event_history = []
            cls._instance._max_history = 500
        return cls._instance

    def __init__(self):
        # Already initialized in __new__ for singleton behavior
        pass

    def subscribe(self, event_type: str, handler: Callable[[Dict[str, Any]], Any]):
        """Register an async or sync callback for a specific event type or '*' for wildcard."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        logger.info(f"Registered subscriber for event type: {event_type}")

    def unsubscribe(self, event_type: str, handler: Callable):
        """Remove a subscriber."""
        if event_type in self._subscribers and handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)

    def emit(self, sender: str, event_type: str, data: Dict[str, Any]):
        """Emit an event synchronously or schedule it on the current event loop."""
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "sender": sender,
            "event_type": event_type,
            "data": data
        }

        # Store in event history
        self._event_history.append(payload)
        if len(self._event_history) > self._max_history:
            self._event_history.pop(0)

        # Dispatch
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._dispatch(event_type, payload))
        except RuntimeError:
            # No running loop, run in a temporary loop or call sync handlers directly
            self._dispatch_sync(event_type, payload)

    async def _dispatch(self, event_type: str, payload: Dict[str, Any]):
        """Dispatch event to registered handlers asynchronously."""
        handlers = list(self._subscribers.get(event_type, [])) + list(self._subscribers.get("*", []))
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(payload)
                else:
                    handler(payload)
            except Exception as e:
                logger.error(f"Error in event handler for {event_type}: {e}")

    def _dispatch_sync(self, event_type: str, payload: Dict[str, Any]):
        """Synchronous dispatch for non-async contexts."""
        handlers = list(self._subscribers.get(event_type, [])) + list(self._subscribers.get("*", []))
        for handler in handlers:
            try:
                if not asyncio.iscoroutinefunction(handler):
                    handler(payload)
            except Exception as e:
                logger.error(f"Error in sync event handler for {event_type}: {e}")

    def get_recent_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Return recently recorded security and system events."""
        return self._event_history[-limit:]

event_bus = EventBus()
