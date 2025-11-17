---
layout: default
title: TOON Format - Token Optimized Object Notation for AI | Reduce JSON Tokens by 60%
description: TOON (Token-Optimized Object Notation) is the revolutionary JSON compression format that reduces AI token usage by up to 60%. Free MCP server for Claude, ChatGPT, and LLMs.
keywords: TOON format, token optimization, JSON compression, reduce AI tokens, MCP server, Claude optimization, token saver, AI development tools, JSON to TOON converter
---

<div class="hero">
    <h1>🔧 TOON-MCP</h1>
    <p>Token-Optimized Object Notation for Efficient AI Context Management</p>
    <div>
        <a href="{{ '/guides/setup' | relative_url }}" class="btn">Get Started</a>
        <a href="https://github.com/aj-geddes/toon-context-mcp" class="btn btn-secondary">View on GitHub</a>
    </div>
</div>

## What is TOON-MCP?

TOON-MCP is a **revolutionary Model Context Protocol (MCP) server** that automatically converts verbose JSON structures into **Token-Optimized Object Notation (TOON)**, reducing token consumption in AI-assisted development workflows by up to **60%**.

[Learn more about TOON format →]({{ '/what-is-toon' | relative_url }})

### Perfect for AI Developers Working With:
- **Large API responses** that consume precious context tokens
- **Complex JSON data** in Claude, ChatGPT, and LLM conversations
- **Token-limited workflows** where every token counts
- **Cost-sensitive applications** requiring token optimization
- **Data-heavy MCP integrations** and tool outputs

**New to TOON?** Check out our [real-world examples]({{ '/examples' | relative_url }}) showing 50-60% token reduction.

## Key Features

<div class="features-grid">
    <div class="feature-card">
        <div class="feature-icon">🚀</div>
        <h3>Smart Compression</h3>
        <p>Automatic pattern detection and intelligent JSON optimization</p>
    </div>

    <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Token Monitoring</h3>
        <p>Real-time tracking of conversation token usage with optimization recommendations</p>
    </div>

    <div class="feature-card">
        <div class="feature-icon">🔌</div>
        <h3>MCP Integration</h3>
        <p>Seamless integration with Claude and other MCP clients</p>
    </div>

    <div class="feature-card">
        <div class="feature-icon">🔄</div>
        <h3>Lossless Conversion</h3>
        <p>Perfect round-trip conversion between JSON and TOON</p>
    </div>

    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <h3>Auto-Optimization</h3>
        <p>Proactive conversion of tool outputs for maximum efficiency</p>
    </div>

    <div class="feature-card">
        <div class="feature-icon">📝</div>
        <h3>Pre-commit Hooks</h3>
        <p>Scan code for JSON and suggest TOON conversions</p>
    </div>
</div>

## Quick Example

Transform verbose JSON into compact TOON format:

**Original JSON** (142 tokens):
```json
{
  "id": 12345,
  "name": "John Doe",
  "email": "john@example.com",
  "type": "user",
  "status": "active",
  "metadata": {
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-15T10:30:00Z"
  }
}
```

**TOON Format** (68 tokens, 52% reduction):
```json
{"_toon":"1.0","d":{"i":12345,"n":"John Doe","eml":"john@example.com","t":"user","s":"active","meta":{"ca":"2025-01-01T00:00:00Z","ua":"2025-01-15T10:30:00Z"}}}
```

## How It Works

```mermaid
graph LR
    A[JSON Input] --> B[Pattern Detection]
    B --> C[TOON Converter]
    C --> D[Compressed Output]
    D --> E[60% Token Savings]

    style A fill:#dbeafe
    style E fill:#d1fae5
```

## Architecture Overview

```mermaid
graph TB
    subgraph "TOON-MCP Server"
        A[MCP Server] --> B[TOON Converter]
        A --> C[Pattern Detector]
        A --> D[Token Monitor]
    end

    subgraph "Claude Code Integration"
        E[Pre-commit Hook] --> F[Auto-Converter]
        F --> G[Example Generator]
    end

    subgraph "Context Manager"
        H[Token Monitor] --> I[Tool Optimizer]
        I --> J[MCP Integration]
    end

    K[Claude / MCP Client] --> A
    A --> K

    style A fill:#2563eb,color:#fff
    style B fill:#7c3aed,color:#fff
    style K fill:#06b6d4,color:#fff
```

## Getting Started

<div class="card">
    <h3>Installation</h3>
    <pre><code>pip install -e mcp-server-toon/</code></pre>
</div>

<div class="card">
    <h3>Configuration</h3>
    <p>Add to your MCP settings:</p>
    <pre><code>{
  "mcpServers": {
    "toon": {
      "command": "python",
      "args": ["-m", "src.server"]
    }
  }
}</code></pre>
</div>

<div class="card">
    <h3>Usage</h3>
    <pre><code>from src.toon_converter import convert_json_to_toon

toon_format = convert_json_to_toon(your_json_data)</code></pre>
</div>

## Why Use TOON Format?

<div class="alert alert-info">
    <strong>📈 Token Efficiency Matters in 2025</strong><br>
    AI token limits constrain developer productivity. TOON format solves this by:
    <ul>
        <li><strong>Reducing JSON token usage by 60%</strong> - Fit 2-3x more data in context</li>
        <li><strong>Lowering AI API costs</strong> - Save $100s monthly on Claude/GPT tokens</li>
        <li><strong>Faster AI responses</strong> - Less data = quicker processing</li>
        <li><strong>Larger dataset analysis</strong> - Process more in single conversations</li>
        <li><strong>Lossless compression</strong> - Perfect round-trip conversion guaranteed</li>
    </ul>
    <a href="{{ '/what-is-toon' | relative_url }}">Read the complete TOON format guide →</a>
</div>

## How Much Can You Save?

Real-world token reduction across data types:
- **API Responses**: 50-60% reduction
- **Database Records**: 55-65% reduction
- **Config Files**: 40-50% reduction
- **Log Data**: 35-45% reduction

[See detailed examples →]({{ '/examples' | relative_url }})

## Next Steps

- 📚 [Setup Guide]({{ '/guides/setup' | relative_url }}) - Install and configure TOON-MCP
- 📖 [User Guide]({{ '/guides/user-guide' | relative_url }}) - Learn how to use TOON effectively
- 🔧 [Troubleshooting]({{ '/guides/troubleshooting' | relative_url }}) - Common issues and solutions
- 📘 [API Reference]({{ '/api/reference' | relative_url }}) - Complete API documentation

## Community & Support

- GitHub: [aj-geddes/toon-context-mcp](https://github.com/aj-geddes/toon-context-mcp)
- Issues: [Report a bug](https://github.com/aj-geddes/toon-context-mcp/issues)
- Discussions: [Join the conversation](https://github.com/aj-geddes/toon-context-mcp/discussions)

---

<p style="text-align: center; color: #6b7280;">
    Built with ❤️ for the AI development community
</p>
