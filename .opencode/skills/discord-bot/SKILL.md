---
name: discord-bot
description: Discord bot development on Cloudflare Workers — Discord API, Developer Portal, slash commands, Gateway WebSocket, Interactions Endpoint, bot permissions, intents, and Ed25519 verification.
---

# Discord Bot Development

Use this skill when working on Discord bots, Discord API integration, bot setup/configuration, or slash command registration. Triggered by mentions of Discord bots, Discord Developer Portal, Discord API, slash commands, Gateway, or Interactions Endpoint.

## Critical Rule: Always Web Search

**The Discord Developer Portal UI changes frequently.** Do NOT rely on pre-trained knowledge for:
* Where settings are located in the Developer Portal
* OAuth2 flow steps
* Bot permission configuration
* Interactions Endpoint setup
* Install link generation

**Always web search first** for any Developer Portal instructions. Use queries like:
* `Discord Developer Portal [specific task] 2026` (include the current year)
* `Discord bot setup [specific feature] latest`

If search results are older than 6 months, note this to the user and suggest they verify in the portal.

## Discord Bot Architecture on Cloudflare Workers

Two models for receiving Discord events:

### Interactions Endpoint (HTTP)
* Discord POSTs slash commands and component interactions to your Worker URL
* No persistent connection needed — pure request/response
* Set the URL in Developer Portal → General Information → Interactions Endpoint URL
* Requires Ed25519 signature verification on every request (`discord-interactions` npm package)
* Supports: slash commands, buttons, select menus, modals, autocomplete

### Gateway (WebSocket)
* Persistent WebSocket connection to `wss://gateway.discord.gg`
* Required for: reaction events, message events, presence, voice state, typing indicators
* On Cloudflare Workers: use a **Durable Object** with `new WebSocket(url)` for the outbound connection
* NOT `fetch()` with `Upgrade: websocket` — that doesn't work for `wss://` URLs
* DO won't hibernate while outbound WS is open — use alarm-based keepalive (30s interval)
* Deploys evict the DO; alarm reconnects within ~30 seconds

### Which Do You Need?

| Feature | Interactions Endpoint | Gateway |
|---------|----------------------|---------|
| Slash commands | Yes | Not needed |
| Message reactions | No | Required |
| Message content | No | Required (with intent) |
| Typing indicators | No | Required |
| Presence updates | No | Required |
| Voice state | No | Required |

Most bots need both: Interactions Endpoint for slash commands, Gateway for real-time events.

## Setting Up a New Discord Bot

### 1. Create Application
* Go to https://discord.com/developers/applications
* Click **New Application**, name it, click Create
* Copy **Application ID** and **Public Key** from General Information page

### 2. Get Bot Token
* Sidebar → **Bot**
* Click **Reset Token**, copy immediately (shown once)
* Toggle privileged intents as needed (see Intents section below)

### 3. Configure Installation
* Sidebar → **Installation**
* Enable **Guild Install**
* Select **Discord Provided Link**
* Under Default Install Settings → Guild Install:
  * **Scopes:** `bot`, `applications.commands`
  * **Permissions:** Select based on your bot's needs (see Permissions section)

### 4. Set Interactions Endpoint
* Sidebar → **General Information**
* Set **Interactions Endpoint URL** to your Worker's `/interactions` path
* Discord sends a PING to verify — your code must handle it (return Pong)
* Save — if verification fails, your endpoint isn't working

### 5. Register Slash Commands
* Use `PUT https://discord.com/api/v10/applications/{app_id}/commands`
* Global commands can take up to an hour to propagate
* Guild-specific commands update instantly (useful for testing)

### 6. Install to Server
* Copy the Install Link from the Installation page
* Paste in browser, select server, authorize

## Intents

Gateway intents control which events Discord sends to your bot.

**Standard intents** (no approval needed):
* `GUILDS` (1 << 0) — guild create/update/delete, role changes
* `GUILD_MESSAGES` (1 << 9) — message create/update/delete in guilds
* `GUILD_MESSAGE_REACTIONS` (1 << 10) — reaction add/remove

**Privileged intents** (must be enabled in Developer Portal → Bot):
* `MESSAGE_CONTENT` (1 << 15) — access to message content via Gateway AND REST API. Without this, `message.content` is empty for messages the bot didn't send or wasn't mentioned in.
* `GUILD_MEMBERS` (1 << 1) — member join/leave/update events
* `GUILD_PRESENCES` (1 << 8) — presence (online/offline) updates

**No approval needed for bots in <100 servers.** Over 100 servers requires Discord review.

## Common Permissions

| Permission | Bit | When needed |
|-----------|-----|-------------|
| View Channels | 1 << 10 | See channels and receive events from them |
| Send Messages | 1 << 11 | Send messages (DMs, channel messages) |
| Read Message History | 1 << 16 | Fetch messages via REST API |
| Use Slash Commands | 1 << 31 | Use application commands |
| Manage Roles | 1 << 28 | Assign/remove roles from members |
| Add Reactions | 1 << 6 | Add reactions to messages |

## Common Gotchas

### Bot doesn't receive reaction events
* **Missing intent:** Must request `GUILD_MESSAGE_REACTIONS` in Gateway IDENTIFY
* **Missing VIEW_CHANNEL:** The bot's role needs View Channels permission. Public channels inherit from @everyone, but **private channels require the bot role to be explicitly added** to the channel's permissions

### Empty message.content from REST API
* **Missing MESSAGE_CONTENT intent:** Must be enabled in Developer Portal → Bot → Privileged Gateway Intents. Also include `MESSAGE_CONTENT` (1 << 15) in the Gateway IDENTIFY intents value

### Slash command not visible
* **Propagation delay:** Global commands take up to an hour. Use guild-specific commands for testing
* **Permission restriction:** `default_member_permissions` hides commands from users without the specified permission
* **Subcommand required:** If a command has subcommands defined, the base command can't be run alone — Discord requires picking a subcommand

### WebSocket connection drops on Cloudflare Workers
* **DO eviction:** Use alarm-based keepalive (30s interval) to prevent idle eviction
* **Deploy:** Deploys always evict the DO. Alarm reconnects within ~30s. Use `/gateway/reconnect` for immediate recovery
* **Use `new WebSocket(url)` not `fetch()` with Upgrade header** for `wss://` URLs

### Discord rate limits
* REST API returns 429 with `retry_after` field (seconds). Wait and retry.
* Gateway has identify rate limits (1 per 5 seconds). Don't reconnect in a tight loop.

## Verification Checklist

When setting up or debugging a Discord bot:

- [ ] Bot token is set and valid (test with `GET /api/v10/users/@me`)
- [ ] Interactions Endpoint URL is set and verified (Developer Portal shows success)
- [ ] Slash commands are registered (`PUT .../commands` returns 200)
- [ ] Bot is installed to the target server (visible in member list)
- [ ] Bot role has necessary permissions (check via REST API `GET /guilds/{id}/members/{bot_id}`)
- [ ] Privileged intents are enabled in Developer Portal if needed
- [ ] Gateway intents in IDENTIFY include all needed flags
- [ ] VIEW_CHANNEL permission is set for private channels
- [ ] Gateway connection is alive (`/gateway/status` returns `connected: true`)

## Reference: Elereada v2

Working example of a Discord bot on Cloudflare Workers: `github.com/rianvdm/elereada-v2`
* Durable Object outbound WebSocket for Gateway
* Hono for HTTP routing + Interactions Endpoint
* D1 for storage
* Alarm-based keepalive for DO persistence
* Ed25519 verification via `discord-interactions` package
