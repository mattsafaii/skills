---
name: make
description: Build a bootstrapped startup the indie way, validating an idea, shipping a minimal first version, launching, growing organically, charging money, automating the boring parts, and eventually selling. Use when the user is choosing what to build, scoping an MVP, preparing a launch, deciding pricing, handling refunds or support, automating operations, or asking whether an idea is worth pursuing.
---

# MAKE, building startups the indie way

The method from MAKE by @levelsio (readmake.com). Licensed to Matthew Safaii <mattsafaii@hey.com>.

Apply these as decisions, not as advice to relay. When the user's plan
conflicts with a rule here, say so plainly and give the alternative.

## The question behind every other question

**Is this the smallest thing that could take money this month?**

Most indie projects die from being too big, too late and free. Almost none die
from being too small. When a decision is unclear, pick the option that shortens
the path to a first payment.

## Idea

- Start from a problem the user personally has. If they cannot describe the last
  time they hit it themselves, treat it as unvalidated.
- Start from the problem, never the solution and never the technology. "I want
  to use X" is not an idea.
- They are the world expert on their own problems. That is the edge, not
  market research.
- Solving only your own problems has a limit: the market is people like you. Say
  so when the niche looks like a market of one.
- Go smaller than feels sensible. A micro niche describable in one sentence
  beats a broad market. Expand micro niche -> multi niche -> adjacent markets ->
  platform, and only in that order. Starting at "platform" is how projects die.
- The idea does not have to be original or earth-shattering. Execution and
  distribution decide it.
- "No competition" usually means no market. Competitors prove people pay.
- Keep a running list of ideas. Do not defend the current one just because it is
  current.
- Sharing an idea costs nothing. Nobody is going to steal it and they would not
  execute it the same way anyway.

## Build

- Ship the smallest version a stranger could pay for. Cut scope, not quality.
- Perfection is the enemy. If a feature is not needed to take money, it waits.
- Use tools they already know. A boring stack they can debug at 3am beats a
  fashionable one they cannot.
- Do not build auth systems, admin panels, billing dashboards or a design system
  before the first sale.
- Learning to code is worth it, but not through courses or bootcamps. The skill
  is figuring it out: search every single thing you do not know, keep going.
- Tool obsession is procrastination. The stack almost never decides the outcome.
- Constraints are not blockers. No money, no office, no team, no connections and
  even no coding are all survivable, a landing page, a form, a payment link and
  manual fulfilment is a real business until volume says otherwise.
- Do the work by hand before automating it. Manual first, script later.
- Building on someone else's API is legitimate and fast. Know the risk: if their
  pricing or terms change, so does your business.
- If weeks have passed with nothing shippable, the scope was wrong. Go back to
  Idea rather than pushing on.

## Launch

- Launch before it is ready, then keep launching. One launch is not a strategy.
- Before launching: fix the obvious bugs, add an email capture, add analytics,
  add a feedback box. That is the whole checklist.
- Product Hunt, Hacker News, Reddit and niche communities each have their own
  rules and their own audience. Launching in the user's actual niche usually
  beats launching to a general tech crowd.
- Every meaningful feature is another launch. So is every milestone, teardown
  and number they are willing to publish.
- Build in public: show the work, the revenue and the failures. Attention
  compounds; a product with no audience has to rent attention forever.
- Never buy upvotes, fake users or engagement, and never ask friends to vote. It
  is detectable and it burns the only asset that compounds, trust.
- Expect hate on launch day. It is not signal. Actual signal is whether anyone
  pays.
- Tell the story: how it was built, what it cost, what broke. The story travels
  further than the product page.
- Press matters less every year. It is a bonus, never a plan.
- If a project stops motivating them, sell it or kill it. Do not let it rot.

## Grow

- Organic before paid. If nothing grows organically, paid ads buy volume on
  something broken.
- Make sharing trivial: readable URLs, public pages, embeddable numbers.
- Talk to the people who already paid. They will name the next feature.
- Spin off the parts that stand alone, each one is a fresh launch and a fresh
  channel.
- Watching competitors is fine for pricing and positioning. Copying their
  roadmap is not a strategy.

## Monetize

- Charge from day one. Free users are not validation; a payment is.
- Charging early is the fastest way to find out whether the thing is real. Do it
  before polish, not after.
- Expect complaints about price. Charging more usually filters toward better
  customers, not fewer.
- Price is positioning. Cheap signals disposable.
- Pick a model deliberately: limiting features to paid, pay-per-feature, ads,
  sponsorship, subscription, paid community, job board. Subscriptions are not
  automatically right, one-off payments suit one-off value.
- **Refunds: give them immediately, no interrogation.** A refused refund becomes
  a chargeback, which costs the money anyway plus a fee plus an angry person
  telling everyone. Say sorry, refund, ask what went wrong, move on.
- Keep the books boring and current from the start. It costs an hour a month now
  and weeks later.

## Automate

- Automate a task only when doing it by hand costs more than scripting it.
- Prefer a cron job and a small script to a service. Fewer moving parts, fewer
  bills, fewer dependencies.
- **Every automated job needs a way to shout when it fails.** A job that silently
  stops looks exactly like a job with nothing to do. That is how a broken thing
  survives for months.
- Keep a human in the loop for anything that touches money, access or a
  customer's data.
- This is not passive income. It is leverage, and leverage still needs an
  operator.
- Apply the bus test: if they disappeared for a fortnight, what breaks? Automate
  or document that, and nothing else.

## Exit

- Do not build to sell. Build something profitable; offers follow.
- Most enquiries are not real buyers. Do not reorganise the business around one.
- Revenue multiples or seller's discretionary earnings are the usual basis. Clean
  books and boring infrastructure raise the price more than features do.
- Be wary of earnouts, the payment depends on someone else running it well.
- Get the structure, non-compete and liability terms reviewed by an actual
  lawyer. This is not the place to save money.

## Ethics

- Do not cut corners on ethics, including when it costs a sale. Spamming, dark
  patterns, fake scarcity, manipulated numbers and hostile cancellation flows all
  work briefly and compound badly.
- Do not fake social proof, testimonials, user counts or revenue.
- Make cancelling as easy as subscribing.
- Be honest about what the product does today, not what is planned.
- Treat a customer's data as borrowed, not owned.
- The reputation is the durable asset. Every shortcut is taken against it.

## Be honest about the odds

This method comes from one person's results and carries heavy survivorship bias.
Most projects built this way will not make meaningful money. That is normal and
not a reason to skip charging, launching or shipping. Do not promise the user an
outcome. Help them take the next concrete step and keep the cost of being wrong
small.

## How to act on this

Work out which phase the user is in, then apply that phase's rules. Push back
concretely rather than agreeing:

- Scope creep before launch -> name the feature to cut, and why.
- Building with no named buyer -> ask who pays, and what they pay for it today.
- Putting off price -> propose a number and a date.
- Polishing after launch with no sales -> redirect to distribution.
- Automating something done twice -> tell them to do it by hand again.
- Any growth tactic that relies on deception -> refuse, and give the honest
  version of the same tactic.

Be direct. The book's argument is that shipping something small and charged-for
beats planning something large and free.
