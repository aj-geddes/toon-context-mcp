#!/usr/bin/env python3
"""
Token Usage Monitor
Monitors conversation token usage and provides optimization recommendations.
"""

import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "mcp-server-toon"))
from src.toon_converter import TOONConverter
from src.patterns import PatternDetector, SmartCompressionStrategy


@dataclass
class TokenUsage:
    """Represents token usage for a message or conversation."""
    timestamp: float
    message_id: str
    role: str  # 'user', 'assistant', 'tool'
    content_type: str  # 'text', 'json', 'code'
    token_count: int
    optimized_token_count: Optional[int] = None
    savings_potential: float = 0.0
    optimization_applied: bool = False


@dataclass
class ConversationMetrics:
    """Metrics for a conversation."""
    total_tokens: int
    user_tokens: int
    assistant_tokens: int
    tool_tokens: int
    optimized_tokens: int
    total_savings: int
    savings_percent: float
    message_count: int
    optimization_count: int


class TokenMonitor:
    """
    Monitors token usage in conversations and suggests optimizations.
    """

    # Approximate tokens per character (rough estimate)
    CHARS_PER_TOKEN = 4

    def __init__(self, warn_threshold: int = 50000, critical_threshold: int = 100000):
        """
        Initialize token monitor.

        Args:
            warn_threshold: Token count to trigger warning
            critical_threshold: Token count to trigger critical alert
        """
        self.warn_threshold = warn_threshold
        self.critical_threshold = critical_threshold
        self.converter = TOONConverter()
        self.detector = PatternDetector()
        self.strategy = SmartCompressionStrategy(self.detector)

        # Conversation state
        self.messages: List[TokenUsage] = []
        self.current_token_count = 0
        self.total_savings = 0

    def estimate_tokens(self, content: str) -> int:
        """
        Estimate token count for content.

        Args:
            content: Text content

        Returns:
            Estimated token count
        """
        # Simple estimation: length / 4
        # More accurate would use tiktoken, but this is a reasonable approximation
        return len(content) // self.CHARS_PER_TOKEN

    def analyze_message(self, content: str, role: str = 'user', message_id: str = None) -> TokenUsage:
        """
        Analyze a message for token usage and optimization potential.

        Args:
            content: Message content
            role: Message role
            message_id: Message identifier

        Returns:
            TokenUsage object
        """
        if message_id is None:
            message_id = f"{role}_{len(self.messages)}"

        # Estimate tokens
        token_count = self.estimate_tokens(content)

        # Detect content type and optimization potential
        content_type, optimized_tokens, savings = self._analyze_content(content)

        usage = TokenUsage(
            timestamp=time.time(),
            message_id=message_id,
            role=role,
            content_type=content_type,
            token_count=token_count,
            optimized_token_count=optimized_tokens,
            savings_potential=savings,
            optimization_applied=False
        )

        self.messages.append(usage)
        self.current_token_count += token_count

        return usage

    def _analyze_content(self, content: str) -> Tuple[str, Optional[int], float]:
        """
        Analyze content and determine optimization potential.

        Args:
            content: Content to analyze

        Returns:
            Tuple of (content_type, optimized_token_count, savings_percent)
        """
        # Try to detect JSON
        try:
            data = json.loads(content)
            toon = self.converter.json_to_toon(data)
            original_tokens = self.estimate_tokens(content)
            toon_tokens = self.estimate_tokens(toon)
            savings_percent = ((original_tokens - toon_tokens) / original_tokens * 100) if original_tokens > 0 else 0

            return 'json', toon_tokens, savings_percent

        except json.JSONDecodeError:
            pass

        # Check if content contains JSON blocks
        json_pattern = r'```json\s*\n(.+?)\n```'
        import re
        matches = re.findall(json_pattern, content, re.DOTALL)

        if matches:
            # Contains JSON code blocks
            total_original = self.estimate_tokens(content)
            potential_savings = 0

            for match in matches:
                try:
                    data = json.loads(match)
                    toon = self.converter.json_to_toon(data)
                    original_block_tokens = self.estimate_tokens(match)
                    toon_block_tokens = self.estimate_tokens(toon)
                    potential_savings += (original_block_tokens - toon_block_tokens)
                except:
                    pass

            savings_percent = (potential_savings / total_original * 100) if total_original > 0 else 0
            optimized_tokens = total_original - potential_savings

            return 'code', optimized_tokens, savings_percent

        # Regular text
        return 'text', None, 0.0

    def get_metrics(self) -> ConversationMetrics:
        """
        Get current conversation metrics.

        Returns:
            ConversationMetrics object
        """
        total_tokens = sum(m.token_count for m in self.messages)
        user_tokens = sum(m.token_count for m in self.messages if m.role == 'user')
        assistant_tokens = sum(m.token_count for m in self.messages if m.role == 'assistant')
        tool_tokens = sum(m.token_count for m in self.messages if m.role == 'tool')

        optimizable_messages = [m for m in self.messages if m.optimized_token_count is not None]
        optimized_tokens = sum(
            m.optimized_token_count or m.token_count
            for m in self.messages
        )

        total_savings = total_tokens - optimized_tokens
        savings_percent = (total_savings / total_tokens * 100) if total_tokens > 0 else 0

        optimization_count = sum(1 for m in self.messages if m.optimization_applied)

        return ConversationMetrics(
            total_tokens=total_tokens,
            user_tokens=user_tokens,
            assistant_tokens=assistant_tokens,
            tool_tokens=tool_tokens,
            optimized_tokens=optimized_tokens,
            total_savings=total_savings,
            savings_percent=savings_percent,
            message_count=len(self.messages),
            optimization_count=optimization_count
        )

    def check_thresholds(self) -> Optional[str]:
        """
        Check if token usage has crossed thresholds.

        Returns:
            Warning message if threshold crossed, None otherwise
        """
        metrics = self.get_metrics()

        if metrics.total_tokens >= self.critical_threshold:
            return f"🚨 CRITICAL: Token usage ({metrics.total_tokens:,}) exceeds critical threshold ({self.critical_threshold:,}). Consider optimizing or starting new conversation."

        elif metrics.total_tokens >= self.warn_threshold:
            potential_savings = metrics.total_savings
            return f"⚠️  WARNING: Token usage ({metrics.total_tokens:,}) approaching limit. Potential savings: {potential_savings:,} tokens ({metrics.savings_percent:.1f}%) with TOON optimization."

        return None

    def get_optimization_recommendations(self) -> List[str]:
        """
        Get recommendations for optimizing token usage.

        Returns:
            List of recommendation strings
        """
        recommendations = []
        metrics = self.get_metrics()

        # Check for high JSON usage
        json_messages = [m for m in self.messages if m.content_type == 'json']
        if json_messages:
            total_json_tokens = sum(m.token_count for m in json_messages)
            if total_json_tokens > metrics.total_tokens * 0.3:  # >30% is JSON
                recommendations.append(
                    f"📊 {len(json_messages)} messages contain JSON ({total_json_tokens:,} tokens). "
                    f"Convert to TOON format to save ~{metrics.total_savings:,} tokens."
                )

        # Check for unoptimized messages
        unoptimized = [m for m in self.messages if m.savings_potential > 20 and not m.optimization_applied]
        if unoptimized:
            recommendations.append(
                f"💡 {len(unoptimized)} messages have >20% optimization potential. "
                f"Apply TOON conversion to reduce token usage."
            )

        # Check if approaching limits
        if metrics.total_tokens > self.warn_threshold:
            recommendations.append(
                "🔄 Consider starting a new conversation or summarizing previous context."
            )

        # Tool output optimization
        tool_messages = [m for m in self.messages if m.role == 'tool']
        if tool_messages:
            total_tool_tokens = sum(m.token_count for m in tool_messages)
            if total_tool_tokens > metrics.total_tokens * 0.4:  # >40% is tool output
                recommendations.append(
                    f"🔧 Tool outputs account for {total_tool_tokens:,} tokens ({total_tool_tokens/metrics.total_tokens*100:.1f}%). "
                    f"Enable automatic TOON conversion for tool outputs."
                )

        return recommendations

    def export_report(self, file_path: Optional[Path] = None) -> str:
        """
        Export detailed token usage report.

        Args:
            file_path: Optional file path to save report

        Returns:
            Report as string
        """
        metrics = self.get_metrics()
        recommendations = self.get_optimization_recommendations()

        report = f"""
# Token Usage Report

Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}

## Summary

- **Total Tokens**: {metrics.total_tokens:,}
- **Messages**: {metrics.message_count}
- **Optimizations Applied**: {metrics.optimization_count}

### Breakdown by Role

- User: {metrics.user_tokens:,} tokens ({metrics.user_tokens/metrics.total_tokens*100:.1f}%)
- Assistant: {metrics.assistant_tokens:,} tokens ({metrics.assistant_tokens/metrics.total_tokens*100:.1f}%)
- Tool: {metrics.tool_tokens:,} tokens ({metrics.tool_tokens/metrics.total_tokens*100:.1f}%)

## Optimization Potential

- **Current Usage**: {metrics.total_tokens:,} tokens
- **Optimized Usage**: {metrics.optimized_tokens:,} tokens
- **Potential Savings**: {metrics.total_savings:,} tokens ({metrics.savings_percent:.1f}%)

## Recommendations

"""
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"

        if not recommendations:
            report += "No specific recommendations at this time.\n"

        report += "\n## Message Details\n\n"
        for msg in self.messages[-10:]:  # Last 10 messages
            report += f"- {msg.role}: {msg.token_count:,} tokens"
            if msg.savings_potential > 0:
                report += f" (potential savings: {msg.savings_potential:.1f}%)"
            report += "\n"

        if file_path:
            with open(file_path, 'w') as f:
                f.write(report)

        return report


class ProactiveOptimizer:
    """
    Proactively optimizes content to reduce token usage.
    """

    def __init__(self, monitor: TokenMonitor):
        """Initialize with a token monitor."""
        self.monitor = monitor
        self.converter = TOONConverter()

    def optimize_content(self, content: str, content_type: str = 'auto') -> Tuple[str, bool]:
        """
        Optimize content to reduce tokens.

        Args:
            content: Content to optimize
            content_type: Type of content ('json', 'code', 'text', 'auto')

        Returns:
            Tuple of (optimized_content, was_optimized)
        """
        if content_type == 'auto':
            # Auto-detect
            try:
                json.loads(content)
                content_type = 'json'
            except:
                content_type = 'text'

        if content_type == 'json':
            try:
                data = json.loads(content)
                toon = self.converter.json_to_toon(data)

                # Check if optimization is worthwhile
                original_tokens = self.monitor.estimate_tokens(content)
                toon_tokens = self.monitor.estimate_tokens(toon)

                if toon_tokens < original_tokens * 0.9:  # At least 10% savings
                    return toon, True

            except:
                pass

        return content, False


def main():
    """Demo of token monitor."""
    monitor = TokenMonitor(warn_threshold=1000, critical_threshold=2000)

    # Simulate conversation
    sample_json = {
        "users": [
            {"id": i, "name": f"User {i}", "email": f"user{i}@example.com", "status": "active"}
            for i in range(20)
        ]
    }

    # Add messages
    monitor.analyze_message("Hello, can you help me with this data?", role='user')
    monitor.analyze_message(json.dumps(sample_json, indent=2), role='tool')
    monitor.analyze_message("Sure, I can help with that data.", role='assistant')

    # Get metrics
    metrics = monitor.get_metrics()
    print("="*60)
    print("Conversation Metrics")
    print("="*60)
    print(f"Total Tokens: {metrics.total_tokens:,}")
    print(f"Potential Savings: {metrics.total_savings:,} ({metrics.savings_percent:.1f}%)")
    print()

    # Get recommendations
    recommendations = monitor.get_optimization_recommendations()
    print("Recommendations:")
    for rec in recommendations:
        print(f"  {rec}")

    # Check thresholds
    warning = monitor.check_thresholds()
    if warning:
        print(f"\n{warning}")

    # Export report
    print("\n" + "="*60)
    print(monitor.export_report())


if __name__ == "__main__":
    main()
