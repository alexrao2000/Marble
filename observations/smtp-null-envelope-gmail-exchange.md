---
name: smtp-null-envelope-gmail-exchange
description: Gmail rejected an unsigned probe with an empty SMTP return address that one Exchange Online tenant queued.
metadata:
  type: observation
  subject: Gmail and Exchange Online inbound SMTP
  observed: 2026-11-07
  status: active
  recheck_after_days: 30
---

## Observed

Gmail rejected an unsigned, plain-text probe that claimed a Gmail From address
and used an empty SMTP return address. A probe from the same client to one
Exchange Online tenant with the same From and empty return address was queued.
Mailbox placement was not checked. Outlook.com consumer delivery was not tested.

## Evidence

Both receiving servers accepted the empty SMTP MAIL FROM and the single
recipient before the message content was submitted over STARTTLS. After DATA,
Gmail returned 550 5.7.26 and reported that SPF and DKIM did not pass.
Exchange Online returned 250 2.6.0, Queued mail for delivery. The second probe
had a different recipient, To header, timestamp, and message ID.

## Re-check

During the next authorized provider comparison, use controlled recipients and
compare the final replies after DATA for equivalent probes from the same client.
Inspect message trace or mailbox placement separately where access permits.

## Apply

Record the final SMTP response and mailbox placement as separate outcomes.
A queued response establishes SMTP acceptance for the tested tenant. Tenant
policy and subsequent filtering can change the outcome.

## History

- 2026-11-07 — Codex measured different SMTP outcomes for two controlled probes.
