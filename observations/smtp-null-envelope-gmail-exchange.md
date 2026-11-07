---
name: smtp-null-envelope-gmail-exchange
description: Gmail rejected an unsigned probe with an empty SMTP return address. Exchange Online and consumer Outlook.com queued comparable probes.
metadata:
  type: observation
  subject: Gmail, Exchange Online, and consumer Outlook.com inbound SMTP
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
The receiving headers confirmed DMARC failure and a quarantine action,
including for a later probe that passed SPF for an unrelated return domain.
The recipient reported that a matching control sent through their signed-in
mailbox reached the Inbox. Consumer Outlook.com accepted a comparable
probe addressed from and to the same Hotmail mailbox and delivered it to Junk. A
signed-in self-send reached the Inbox and passed SPF, DKIM, and DMARC.

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

A final unsigned probe used a separate controlled domain for the SMTP
return path. A temporary SPF TXT record authorized the sending IP.
Exchange Online queued the message at DATA and recorded spf=pass for
the return domain, dkim=none, and dmarc=fail action=quarantine for the
organization-domain From. Composite authentication failed with
reason=000 and the report again showed CAT:SPOOF. The recipient
confirmed that the probe appeared in Defender Quarantine.

The client submitted one unsigned plain-text probe to the consumer Hotmail
MX over STARTTLS. The visible From and To used the same recipient address.
The SMTP return path was empty. The server returned 250 2.6.0 after DATA
and reported that the message was queued. The recipient found it in Junk.
The recipient supplied headers showing SPF failure for the SMTP greeting,
no DKIM signature, dmarc=fail action=none, and compauth=fail reason=001.
Outlook recorded SCL 5 and RF:JunkEmail. The headers record the
authentication and placement results but do not isolate the signals
that produced the spam verdict.

The signed-in Hotmail control used the same visible From and To addresses.
The recipient reported Inbox placement. The receiving headers recorded
spf=pass for the Hotmail return domain, dkim=pass for the Hotmail signing
domain, dmarc=pass, and compauth=pass reason=100. The mailbox header recorded
dest:I and OFR:SpamFilterPass, and the organization SCL was 1. The pasted
control had an empty subject and body. Content and submission route differed
between messages, so this comparison does not isolate a filtering signal.

A later Resend API submission from a custom domain to consumer Hotmail
returned a message ID. The recipient supplied Resend's bounce detail,
which recorded Hotmail's SMTP 550 5.7.1 authentication rejection
(AS9031519), despite a generic temporary failure label in the dashboard.
DNS lookups found Resend's DKIM key and SPF on the return domain, but no
DMARC record for the visible From domain. No receiving headers were
available to establish which message-level checks passed.

After the domain owner added a DMARC record with p=none, both authoritative
nameservers and two public resolvers returned it. A retry through Resend
used the same visible sender, recipient, subject, and body. The recipient
reported that Hotmail placed the retry in Junk. The headers show SPF pass
for the custom return subdomain, DKIM pass for the visible From domain,
DMARC pass, and composite authentication pass (reason 100). The mailbox
delivery header reported auth:1, dest:J, and RF:JunkEmail, and the
organization SCL was 5. The headers do not identify which spam-filter
signals caused Junk placement.

A follow-up Resend test kept the sender address, recipient, and DNS settings.
It used a different subject and body. The recipient reported Inbox placement.
The receiving headers and source IP were not inspected, so this comparison
does not isolate message content from other filtering signals.

## Re-check

During the next authorized provider comparison, use controlled recipients and
compare the final replies after DATA for equivalent probes from the same client.
Inspect message trace or mailbox placement separately where access permits.

## Apply

Record the final SMTP response and mailbox placement as separate outcomes.
A queued response establishes SMTP acceptance. Recipient policy and
subsequent filtering can change the outcome.

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
- 2026-11-07 — The recipient confirmed quarantine even with SPF passing
  for an unrelated return domain.
- 2026-11-07 — Consumer Outlook.com queued an unsigned probe with the same Hotmail address in From and To.
- 2026-11-07 — The recipient confirmed the consumer Hotmail probe reached Junk.
- 2026-11-07 — The consumer Hotmail headers confirmed a DMARC failure
  with action=none, a composite authentication failure, and a Junk verdict.
- 2026-11-07 — The recipient confirmed Inbox placement for the signed-in
  Hotmail control and supplied its passing authentication results.
- 2026-11-07 — The recipient supplied the SMTP rejection for a Resend test
  from a custom domain without a published DMARC record.
- 2026-11-07 — A Resend retry after the DMARC record was published reached
  Junk in the consumer Hotmail mailbox.
- 2026-11-07 — Hotmail's receiving headers confirmed SPF, DKIM, DMARC,
  and composite authentication passed for the Resend retry placed in Junk.
- 2026-11-07 — The recipient confirmed that a Resend follow-up with
  different message content reached the Hotmail Inbox.
