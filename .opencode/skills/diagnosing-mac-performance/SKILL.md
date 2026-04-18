---
name: diagnosing-mac-performance
description: Use when the user reports their Mac is slow, sluggish, laggy, or unresponsive — or asks what's using CPU, memory, or battery. Also triggers on "check system performance", "what's eating my CPU", "Mac is hot", "fan is loud", or any request to diagnose macOS resource usage. Covers CPU hogs, memory pressure, swap thrashing, and runaway system daemons.
---

# Diagnosing Mac Performance Issues

## When to Use

* User says their Mac feels slow, laggy, or unresponsive
* User asks what's consuming CPU, memory, or battery
* User reports fans running loud or machine running hot
* Proactive check during long sessions if the user mentions sluggishness

## Steps

1. **Snapshot system state** — run these in parallel:
   ```bash
   # Top processes by CPU
   ps -eo pid,pcpu,pmem,comm -r | head -25

   # System overview (load avg, memory, swap)
   top -l 1 -n 1 -stats pid,command,cpu | head -10

   # Memory pressure and swap
   sysctl vm.swapusage && memory_pressure
   ```

2. **Triage into CPU-bound vs memory-bound:**
   - **CPU-bound:** One or more processes above 30% CPU. Identify and investigate.
   - **Memory-bound:** Swap used > 2 GB, compressor > 4 GB, or "Pages free" under 10,000. Even if no single process is hot, the system spends CPU on compression/decompression and swap I/O.
   - **Both:** Common. A runaway daemon often causes memory pressure too.

3. **For CPU hogs — identify the category:**

   | Process type | Normal range | Investigate if | Common fix |
   |-------------|-------------|----------------|------------|
   | WindowServer | 10-20% | >35% sustained | Usually driven by another app doing excessive redraws. Fix the other app. |
   | contactsd / AddressBookManager | <2% | >10% | Stuck sync loop. Check error logs, disable problematic account sync (Gmail CardDAV is a known offender). |
   | mds / mds_stores / mdworker | <5% each | >20% or many workers | Spotlight indexing. Usually transient after updates. `sudo mdutil -i off /` to pause if urgent. |
   | kernel_task | varies | >200% | Thermal throttling. Not fixable via software — machine needs cooling. |
   | nsurlsessiond / cloudd | <5% | >15% | iCloud sync stuck. Check System Settings > Apple ID > iCloud. |
   | trustd | <1% | >10% | Certificate validation loop. Often clears on reboot. |
   | Electron apps (Discord, Slack, VS Code, Windsurf) | 2-5% each | >15% | Restart the app. Electron apps leak memory over time. |

4. **For memory pressure — assess severity:**
   ```bash
   # Quick summary
   sysctl vm.swapusage
   # Detailed breakdown
   memory_pressure
   ```

   | Indicator | Healthy | Warning | Critical |
   |-----------|---------|---------|----------|
   | Swap used | <500 MB | 500 MB - 2 GB | >2 GB |
   | Compressor | <2 GB | 2-5 GB | >5 GB |
   | Pages free | >20,000 | 5,000-20,000 | <5,000 |
   | Free percentage | >30% | 10-30% | <10% |

   If critical: recommend quitting the heaviest apps. List them with memory percentages so the user can make an informed choice.

5. **For runaway system daemons — pull error logs:**
   ```bash
   /usr/bin/log show --predicate 'process == "<daemon_name>" AND (messageType == 16 OR messageType == 17)' --last 5m --style compact 2>&1 | head -50
   ```
   - `messageType == 16` = Error, `messageType == 17` = Fault
   - Use `/usr/bin/log` (full path) because shell aliases can interfere
   - Look for repeated errors in tight loops — that's the signature of a stuck daemon

6. **Report findings** using this structure:

   **Top resource consumers:**

   | Process | CPU % | RAM % | Status |
   |---------|-------|-------|--------|
   | contactsd | 124% | 0.9% | Stuck — sync loop (see below) |
   | WindowServer | 47% | 0.7% | Elevated — driven by contactsd churn |

   **Memory pressure:** Critical — 15 GB / 16 GB used, 4.3 GB swap, 6.5 GB compressor

   **Diagnosis:** contactsd is in a sync error loop caused by [root cause]. This is stuck, not transient.

   **Recommended fixes** (least to most disruptive):
   1. [First option]
   2. [Second option]
   3. [Nuclear option, if applicable]

   Adapt the structure to fit — skip sections that don't apply, add detail where it matters. The key is: show the data, state the diagnosis, order the fixes.

## Gotcha Section

- **`ps` syntax is different on macOS.** No `--sort` flag. Use `ps -eo pid,pcpu,pmem,comm -r` (sort by CPU) or `-m` (sort by memory). GNU-style `ps aux --sort=-%cpu` will error.
- **`top -l 1` is a snapshot, not live.** The CPU percentages in a single `top` snapshot can be misleading — a process caught mid-burst looks worse than it is. Use `ps -r` as the primary view; `top` for the load average and memory summary.
- **Killing system daemons usually just restarts them.** `killall contactsd` → launchd restarts it immediately. This is fine for breaking a stuck loop, but if the root cause isn't fixed, it'll spin right back up.
- **Sandbox/TCC blocks terminal access to some directories.** `~/Library/Application Support/AddressBook/`, `~/Library/Messages/`, and others are protected. Even `sudo` won't help — the terminal app needs Full Disk Access in System Settings > Privacy & Security. Don't waste time retrying with sudo; tell the user to either grant FDA or run the commands from Finder.
- **"Could not convert account" errors in contactsd** are almost always a Gmail CardDAV sync issue on modern macOS. The account can't be mapped to the SwiftData format. Fix: disable contact sync for that Google account in System Settings > Internet Accounts, not in iCloud settings.
- **Memory pressure is often the real culprit even when the user says "slow."** High CPU with healthy memory feels snappy. Normal CPU with thrashed swap feels awful. Always check swap alongside CPU.
- **WindowServer CPU tracks the number of active rendering clients.** High WindowServer isn't a WindowServer bug — it's a symptom. Count the Electron apps, browser tabs, and GPU-using apps to find the actual cause.
- **Compressor memory is "used" memory doing useful work.** Don't alarm the user about 4 GB compressor usage on a 16 GB machine if swap is low and things feel fine. It becomes a problem only when combined with high swap.
- **`memory_pressure` might not exist on older macOS.** Fall back to parsing `vm_stat` output if it fails.

## Constraints

- Never suggest `sudo rm -rf` on system directories
- Never modify launchd plists or system daemon configs — suggest the user do it via System Settings
- Don't recommend disabling SIP, Gatekeeper, or any macOS security feature to fix performance
- If recommending file deletion (e.g., rebuilding a cache), always back up first
- Don't present swap usage as inherently bad — some swap is normal. Focus on whether it's causing perceptible slowness
- Report what you observe, not what you assume. "contactsd is at 124%" is a fact; "your contacts are corrupt" is an inference — qualify it
