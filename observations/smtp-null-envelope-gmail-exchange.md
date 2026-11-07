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
The recipient found the original Exchange Online probe in Junk. The probe
claiming the recipient's own address was quarantined after SMTP acceptance.
The receiving headers confirmed DMARC failure and a quarantine action.
The recipient reported that a matching control sent through their signed-in
mailbox reached the Inbox. Outlook.com consumer delivery was not tested.

## Evidence

Both receiving servers accepted the empty SMTP MAIL FROM and the single
recipient before the message content was submitted over STARTTLS. After DATA,
Gmail returned 550 5.7.26 and reported that SPF and DKIM did not pass.
Exchange Online returned 250 2.6.0, Queued mail for delivery. The second probe
had a different recipient, To header, timestamp, and message ID.

Follow-up probes used the same SMTP method and tested both matching and
different From and To addresses. At DATA, Gmail again returned 550 5.7.26
for a From address from the other domain. Exchange Online queued probes
with a Gmail From and with its own recipient address in From. The probe
subjects and message IDs differed. The recipient supplied the quarantine
record for the probe claiming their own address. It showed Phish as the
reason, Anti-phishing policy as the policy type, and no sender address
override. The recipient later supplied the receiving headers. The empty
return path caused SPF to evaluate the SMTP greeting, which failed. DKIM
was absent. The receiver recorded dmarc=fail action=quarantine and
compauth=fail reason=000, an explicit authentication failure. The
anti-spam report categorized the message as CAT:SPOOF. The headers do
not establish whether other detections contributed.

The recipient sent a matching control from their signed-in mailbox to
themselves and confirmed Inbox placement. The submission route and sender
authentication changed together. The control headers were not inspected,
so the comparison does not isolate a specific authentication check.

Two later probes kept the same organization-domain From and recipient but
used nonempty SMTP return paths. Exchange Online queued both at DATA. SPF
failed for the organization-domain return path and softfailed for the Gmail
return path. Both lacked DKIM signatures and produced dmarc=fail
action=quarantine, compauth=fail reason=000, and CAT:SPOOF. The recipient
supplied the receiving headers. Folder placement was not stated.

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
- 2026-11-07 — Codex repeated the provider comparison with matching and
  different addresses. The recipient confirmed Junk placement for the
  original queued probe.
- 2026-11-07 — The recipient supplied the quarantine result for the probe
  that used their own address as both From and To.
- 2026-11-07 — The recipient confirmed Inbox placement for the signed-in
  self-send control.
- 2026-11-07 — The recipient supplied receiving headers confirming
  DMARC failure and quarantine for the unsigned self-addressed probe.
- 2026-11-07 — The recipient supplied headers from two return-path variants.
  SPF changed from fail to softfail, while the DMARC action stayed quarantine.
