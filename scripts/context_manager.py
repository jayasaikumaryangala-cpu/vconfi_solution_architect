#!/usr/bin/env python3
"""
VConfi Context Manager — Saves conversation state to files to prevent context overflow

Usage:
    from context_manager import ContextManager
    
    cm = ContextManager("ClientName_Project")
    
    # Save decisions as they're made
    cm.save_decision("firewall_model", "FortiGate 200F")
    cm.save_decision("user_count", 500)
    
    # Save conversation summary
    cm.save_conversation_summary("Discussed network requirements, agreed on 8 VLANs...")
    
    # Load when starting fresh
    state = cm.load_state()

This module helps manage context window by:
1. Writing all decisions to files immediately
2. Keeping only references/summaries in active context
3. Allowing fresh conversations to resume from file
"""

import json
import os
from datetime import datetime
from pathlib import Path


class ContextManager:
    """Manages conversation state to prevent context overflow."""
    
    def __init__(self, session_name, base_dir=".context"):
        """
        Initialize context manager.
        
        Args:
            session_name: Unique name for this session (e.g., "AcmeCorp_NetworkUpgrade")
            base_dir: Directory to store context files
        """
        self.session_name = session_name
        self.base_dir = Path(base_dir)
        self.session_dir = self.base_dir / session_name
        
        # Create directories
        self.session_dir.mkdir(parents=True, exist_ok=True)
        
        # File paths
        self.decisions_file = self.session_dir / "decisions.json"
        self.summary_file = self.session_dir / "conversation_summary.md"
        self.state_file = self.session_dir / "state.json"
        
        # Initialize files if don't exist
        self._init_files()
    
    def _init_files(self):
        """Initialize empty files if they don't exist."""
        if not self.decisions_file.exists():
            self._write_json(self.decisions_file, {})
        
        if not self.summary_file.exists():
            self.summary_file.write_text("# Conversation Summary\n\n", encoding='utf-8')
        
        if not self.state_file.exists():
            self._write_json(self.state_file, {
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "phase": "discovery",
                "completed_groups": []
            })
    
    def _write_json(self, path, data):
        """Write JSON to file."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def _read_json(self, path):
        """Read JSON from file."""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_decision(self, key, value, category="general"):
        """
        Save a decision to file.
        
        Args:
            key: Decision identifier (e.g., "firewall_model")
            value: Decision value
            category: Category for grouping (e.g., "network", "servers")
        """
        decisions = self._read_json(self.decisions_file)
        
        if category not in decisions:
            decisions[category] = {}
        
        decisions[category][key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
        
        self._write_json(self.decisions_file, decisions)
        
        # Update state
        self._update_state()
    
    def get_decision(self, key, category="general"):
        """Retrieve a decision."""
        decisions = self._read_json(self.decisions_file)
        
        if category in decisions and key in decisions[category]:
            return decisions[category][key]["value"]
        
        return None
    
    def get_all_decisions(self):
        """Get all decisions as a flat dictionary."""
        decisions = self._read_json(self.decisions_file)
        flat = {}
        
        for category, items in decisions.items():
            for key, data in items.items():
                flat[f"{category}.{key}"] = data["value"]
        
        return flat
    
    def save_conversation_summary(self, summary, phase=None):
        """
        Append to conversation summary.
        
        Args:
            summary: Text summary of conversation
            phase: Current phase (discovery, design, document_generation)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        with open(self.summary_file, 'a', encoding='utf-8') as f:
            f.write(f"\n## [{timestamp}]\n")
            if phase:
                f.write(f"**Phase:** {phase}\n\n")
            f.write(f"{summary}\n")
        
        if phase:
            self.update_state(phase=phase)
    
    def update_state(self, **kwargs):
        """Update state file."""
        state = self._read_json(self.state_file)
        state.update(kwargs)
        state["last_updated"] = datetime.now().isoformat()
        self._write_json(self.state_file, state)
    
    def _update_state(self):
        """Update timestamp only."""
        state = self._read_json(self.state_file)
        state["last_updated"] = datetime.now().isoformat()
        self._write_json(self.state_file, state)
    
    def load_state(self):
        """Load complete state."""
        return {
            "decisions": self._read_json(self.decisions_file),
            "summary": self.summary_file.read_text(encoding='utf-8'),
            "state": self._read_json(self.state_file)
        }
    
    def generate_resume_prompt(self):
        """
        Generate a prompt to resume work in a fresh conversation.
        
        Returns text that can be pasted into a new conversation.
        """
        state = self.load_state()
        
        prompt = f"""# Resume Session: {self.session_name}

## Current Phase
{state['state'].get('phase', 'unknown')}

## Key Decisions Made
"""
        
        for category, items in state['decisions'].items():
            prompt += f"\n### {category.title()}\n"
            for key, data in items.items():
                prompt += f"- **{key}:** {data['value']}\n"
        
        prompt += f"\n## Conversation History\n{state['summary']}\n"
        
        return prompt
    
    def mark_group_completed(self, group_number):
        """Mark a questioning group as completed."""
        state = self._read_json(self.state_file)
        
        if "completed_groups" not in state:
            state["completed_groups"] = []
        
        if group_number not in state["completed_groups"]:
            state["completed_groups"].append(group_number)
        
        self._write_json(self.state_file, state)
    
    def is_group_completed(self, group_number):
        """Check if a questioning group is completed."""
        state = self._read_json(self.state_file)
        return group_number in state.get("completed_groups", [])


def main():
    """CLI for context management."""
    import argparse
    
    parser = argparse.ArgumentParser(description='VConfi Context Manager')
    parser.add_argument('session', help='Session name')
    parser.add_argument('--show', '-s', action='store_true', help='Show state')
    parser.add_argument('--resume', '-r', action='store_true', help='Generate resume prompt')
    
    args = parser.parse_args()
    
    cm = ContextManager(args.session)
    
    if args.show:
        import pprint
        state = cm.load_state()
        pprint.pprint(state)
    
    if args.resume:
        print(cm.generate_resume_prompt())


if __name__ == '__main__':
    main()
