"""
Context Manager - Maintains message history and manages token limits
"""

import json
from typing import List, Dict, Optional
from datetime import datetime


class ContextManager:
    """Manages conversation context with auto-compaction."""

    MAX_TOKENS = 170000  # Hugging Face ml-intern uses ~170k
    TOKENS_PER_CHAR = 4  # Rough estimate

    def __init__(self):
        self.messages: List[Dict] = []
        self.action_history: List[Dict] = []

    def add_message(self, role: str, content: str) -> None:
        """Add message to history."""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

        # Auto-compact if needed
        if self.estimate_tokens() > self.MAX_TOKENS:
            self.compact()

    def add_action(self, action: str, tool: str, result: str) -> None:
        """Log executed action."""
        self.action_history.append({
            "action": action,
            "tool": tool,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })

    def estimate_tokens(self) -> int:
        """Rough token count estimate."""
        total_chars = sum(len(m.get("content", "")) for m in self.messages)
        return int(total_chars / self.TOKENS_PER_CHAR)

    def compact(self) -> None:
        """Compact old messages when approaching limit."""
        if len(self.messages) <= 2:
            return

        # Keep first 2 and last 10 messages
        kept_messages = self.messages[:2] + self.messages[-10:]

        # Summarize removed messages
        removed_count = len(self.messages) - len(kept_messages)
        if removed_count > 0:
            summary = {
                "role": "system",
                "content": f"[Context compacted: {removed_count} messages summarized]"
            }
            self.messages = [summary] + kept_messages

    def get_messages(self) -> List[Dict]:
        """Get all messages."""
        return self.messages

    def get_last_n_messages(self, n: int) -> List[Dict]:
        """Get last N messages."""
        return self.messages[-n:]

    def clear(self) -> None:
        """Clear all history."""
        self.messages = []
        self.action_history = []

    def get_summary(self) -> Dict:
        """Get context summary."""
        return {
            "total_messages": len(self.messages),
            "estimated_tokens": self.estimate_tokens(),
            "actions_taken": len(self.action_history),
            "max_tokens": self.MAX_TOKENS,
        }
