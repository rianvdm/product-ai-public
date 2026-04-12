# My Product Philosophy

In this document I try to articulate how I think about product work. It's not a methodology, and I wouldn't adopt it wholesale. It's what I've picked up over the years about what works and what doesn't.

---

## Start with the Problem, Not the Solution

I've seen more product initiatives fail because they started with a solution than for any other reason. "We should build a developer portal" is not a problem statement. "Engineers waste 2-3 hours per week searching for documentation across fragmented systems" is.

Before jumping into what to build, I always try to answer:
- What pain or friction exists today?
- Who is experiencing it, and how often?
- What happens if we do nothing?

This sounds obvious, but it's hard to maintain discipline around. We're wired to solve things. Someone says "we need better monitoring" and our brains immediately start sketching architectures. But the best specs start with pain, not features. Every time. And if you can't clearly articulate the problem, you're probably not ready to build the solution.

---

## Outcomes Over Outputs

There's a difference between shipping things and changing things. Launching a new dashboard is an output. Reducing incident response time by 40% is an outcome.

I try to focus relentlessly on the change we want to see in the world, not the activities or deliverables along the way. "Launch X" or "Ship Y" are tasks, not goals. The goal is what happens *after* you ship. Did behavior change? Did the pain go away? Did customers succeed in ways they couldn't before?

This distinction matters because it keeps us honest about whether we're actually solving problems or just staying busy.

---

## Empowered Teams Make Better Products

I'm a big believer in [Daniel Pink's assertion](https://bookshop.org/a/89364/9781594484803) that people are ultimately motivated by *Autonomy*, *Mastery*, and *Purpose*. That belief shapes how I think about product teams.

Instead of handing teams a roadmap of features to build, I believe in giving them problems to solve and the strategic context to solve them well. [In the words of Marty Cagan](https://www.svpg.com/empowered-product-teams/): "Instead of being given a roadmap of features, an empowered team is given a problem to solve and they get to figure out the best way to solve that problem."

My role as a product leader is to provide:
- **Strategic context** — where the company is going and why
- **Clear goals** — what outcomes we're trying to achieve
- **Guardrails** — constraints, dependencies, and things that are off the table

And then I trust teams to figure out the *how*. This doesn't mean I disappear. I stay close to the details, ask questions, offer suggestions, and help remove obstacles. But the decisions should be made by those closest to the data.

---

## Collaboration Over Consensus

I want diverse input and perspectives when making decisions. The best ideas often come from unexpected places. An engineer noticing a pattern in support tickets, a designer who's been watching user sessions, a customer success rep who keeps hearing the same complaint.

But collaboration doesn't mean consensus. "Nothing is what happens when everyone has to agree," as Seth Godin puts it. At some point, someone needs to make a call. I believe that call should be made by the people closest to the problem and the data, not by the most senior person in the room or the loudest voice.

This is why I like frameworks like [DACI](https://github.com/rianvdm/pm-resources/blob/main/processes/daci.md). Clear decision rights mean faster decisions and less second-guessing.

---

## Roadmaps Are Road Signs Into the Fog

I think about planning through the lens of [The Fog of War](https://elezea.com/2023/03/product-management-and-the-fog-of-war/). In strategy games, the fog of war hides parts of the map you haven't explored yet. You can't see what's there until you move toward it.

Product planning is the same. We can't predict the future. We can only make the best decisions with the information we have right now. Customers will surprise us and the market will change in ways we didn't anticipate.

So I treat planning documents as "a road sign into the fog." We make sure the direction and first few steps are known, and then we add and edit as the fog starts to lift. This is why I prefer [Now/Next/Later roadmaps](https://elezea.com/2024/02/why-using-a-now-next-later-roadmap-might-be-right-for-you/) over deadline-driven quarterly roadmaps:

- **Now** — what we're actively working on (limited to 1-2 things per team)
- **Next** — what's coming in the next few weeks, fully spec'd and ready to go
- **Later** — what we believe is important, but may shift as we learn more

The further out you go, the more likely things will change. That's not a bug, it's an honest reflection of reality.

---

## Deadline-Driven Development Is Fraught

Speaking of roadmaps: I've become deeply skeptical of arbitrary deadlines. Dates matter when there are real external commitments or dependencies. The problem is that deadlines often get set without any input from the teams that have to do the work.

When that happens, teams are forced to make quality tradeoffs to hit the date. Technical debt accumulates. Corners get cut. And the thing you ship is worse than what you could have shipped if you'd taken the time to do it right.

I prefer working with [high-integrity commitments](https://www.svpg.com/managing-commitments-in-an-agile-team/): dates that teams commit to *after* they've had a chance to scope the work properly. Teams are accountable to these dates because they were involved in setting them. And if something changes, we talk about it openly rather than pretending we can still hit an impossible target.

---

## Teams Make Better Products in Calm Environments

Every time I travel, I remind myself: [no running in airports](https://elezea.com/2024/02/no-running-in-airports/). Running means something went wrong. A delay, a missed detail. The goal is to be prepared enough that running isn't necessary.

I think about product work the same way. Urgency is sometimes unavoidable, but chronic urgency is a sign that something is broken. When teams are constantly in crisis mode, they can't do their best work. They make mistakes, burn out, and eventually leave.

I believe in quality over speed. Taking the time to understand the problem. Giving teams space to do focused, deep work. Building things right the first time instead of accumulating technical debt. It's slower in the short term, but faster in the long term—and much better for the humans involved.

---

## Choose Your Battles Wisely

Product managers tend to gravitate toward [wicked problems](https://elezea.com/2023/05/product-life-force/), the complex and ambiguous challenges with no clear solution. It's what makes us good at our jobs. But it can also be self-defeating if we're not careful about where we spend our energy.

I think about this as "life force": the finite amount of energy and willpower we have available. Some battles are worth fighting: hard problems where we have real influence and can make a meaningful difference. Others are not: hard problems where organizational dynamics or lack of buy-in mean we're unlikely to succeed no matter how hard we try.

The goal is to pick the *right* hard problems—the ones where the effort will actually pay off.

---

## Process Should Serve the Team, Not the Other Way Around

I'm not dogmatic about specific frameworks or ways of doing things. OKRs, Scrum, Kanban, Shape Up. They're all tools. What matters is whether they help your team do good work in your specific context.

That said, here are some approaches I've found useful:

- **[W Planning](https://elezea.com/2023/03/okr-alternatives-empowered-teams-w-planning-eos/)** — a collaborative goal-setting process where leadership provides strategic context and teams propose how to achieve the goals. It's a back-and-forth that ensures alignment without top-down mandates.

- **[EOS Vision & Focus](https://elezea.com/2023/03/okr-alternatives-empowered-teams-w-planning-eos/)** — a lightweight alternative to OKRs that combines long-term vision with quarterly priorities and a running issues list.

- **[Product Discovery](https://alistapart.com/article/usable-yet-useless-why-every-business-needs-product-discovery/)** — a structured process for understanding problems before jumping to solutions, including problem framing, solution exploration, and prioritization.

The common thread is that all of these prioritize understanding over action and collaboration over hierarchy.

---

## Learn to Love Documentation

I'm a big fan of "working in the open." When we document our decisions, including the context and reasoning behind them, we build organizational memory. A year from now, when someone asks "why did we decide to do that?", we have an answer.

This is especially important for strategy work. Strategies change often in some organizations precisely because no one remembers why the last one was chosen. If the context and reasoning are documented, the next person to come along has what they need to make an informed decision about whether to stay the course or change direction.

Documentation is a gift to your future self and your teammates.

---

## Strategy Is Collaborative

Product strategy isn't something that should happen in a room with three executives and a whiteboard. The people closest to customers and the technology often have the best insights about what's possible and what's needed.

When I've done [collaborative product strategy work](https://elezea.com/2023/01/product-strategy-framework-process/), we've involved the whole team: engineers, designers, customer success, marketing, everyone. It takes longer, and it's messier, but the outcomes are better because we're drawing on everyone's knowledge. And the team buys in because they helped shape it.

This is the philosophy behind W Planning too: leadership sets the direction, but teams propose the path. It's a partnership, not a mandate.

---

## Iteration Over Big Bang

Ship early. Ship often. Learn and adjust.

I'd rather release something small that delivers real value and iterate based on feedback than spend six months building the "complete" solution only to discover we got something wrong. The longer you wait to get something in front of users, the more risk you're accumulating.

This doesn't mean shipping half-baked work. Each release should deliver standalone value. But breaking big initiatives into smaller, shippable chunks reduces risk and accelerates learning.

---

## The Person Comes First

Products are made by people. And people do their best work when they're happy, healthy, and feel supported.

I believe the person will always be more important than the project. If someone is struggling—whether with the work, with something at home, or with their own wellbeing—that takes priority. We can adjust timelines. We can redistribute work. What we can't do is burn people out and expect great products to emerge.

Happy teams make better products.

---

None of this is original. I've learned from countless people, books, and experiences along the way. What I've tried to do here is synthesize what's worked for me into something coherent. Take what resonates, adapt it to your situation, and leave the rest.
