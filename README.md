# Product AI Public

Curated prompts, commands, and agents for AI-assisted product management. A subset of my personal "second brain" repo, published for others to adapt.

## What's here

This is a curated subset of my personal AI-assisted product management toolkit. These prompts, context files, and commands work with Claude, ChatGPT, OpenCode, Cursor, or any LLM-based coding/writing assistant.

### Context Files

* [`context/avoid-ai-patterns.md`](context/avoid-ai-patterns.md) -- To keep writing natural and human, avoid these telltale AI patterns:
* [`context/product-philosophy.md`](context/product-philosophy.md) -- In this document I try to articulate something that can be notoriously hard to pin down: how I think about product work.

### Prompts

* [`prompts/meta/meeting-summary.md`](prompts/meta/meeting-summary.md) -- Transform a meeting transcript into structured, scannable meeting notes that surface what matters: themes, decisions,...
* [`prompts/pm/debate-product-idea.md`](prompts/pm/debate-product-idea.md) -- You are a simulator for a high-stakes product strategy debate.

## How to use these

Most of these files are **system prompts** or **prompt templates** you can paste into any LLM conversation. Some are designed for specific tools:

* **`context/`** files work well as persistent context (system prompts, custom instructions, or project knowledge files)
* **`prompts/`** files are task-specific prompts you paste when needed
* **`.opencode/command/`** files are [OpenCode](https://opencode.ai) slash commands (but the prompt content works anywhere)

## Adapting to your context

These prompts reference a few personal conventions you'll want to adapt:

* References to `context/*.md` files point to personal context documents (writing style, philosophy, etc.). Create your own equivalents.
* Some prompts mention MCP servers or tool integrations. Replace with whatever tools you use.
* The writing style and product philosophy reflect my preferences. Adjust to match yours.

## About

I'm [Rian van der Merwe](https://elezea.com), a product manager who uses AI tools extensively in my daily work. This repo contains the prompts and context files I've found most useful, published so others can adapt them.

For more on my approach to product management and AI, see [`context/product-philosophy.md`](context/product-philosophy.md).

## License

MIT. Use these however you like.
