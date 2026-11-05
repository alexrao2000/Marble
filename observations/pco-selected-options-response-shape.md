---
name: pco-selected-options-response-shape
description: PCO form selections use field-prefixed keys and option labels rather than bare field IDs
metadata:
  type: observation
  subject: Planning Center People API 2025-07-17
  observed: 2026-11-05
  status: active
  recheck_after_days: 30
---

## Observed

When explicitly requested as a sparse FormSubmission field, selected_options_by_field returned a JSON object keyed by field_<field-id>, with arrays of option labels. Looking up the bare numeric field ID returned no result despite recorded choices being present. The public API reference describes this attribute as JSON but does not specify these keys or values.

## Evidence

Read the target form's field definitions and its referral field's fixed options using GET requests. Requesting the latest 100 submission metadata records showed nonempty selection maps in 85 records, while lookup by the bare field ID matched none. Inspecting a nonempty map showed a field-prefixed key and an array containing a label matching the field options. The complete form history then yielded nonzero referral aggregates in two matching calendar months a year apart. No form records or permissions were changed. No personal answers, field IDs, or credentials are retained in this observation.

## Re-check

With authorized local credentials, GET the chosen form's fields and the target field's options, then request submission metadata with fields[FormSubmission]=created_at,selected_options_by_field. Inspect only map key structure and whether target values match known option labels or IDs; do not print unrelated selections or written responses. Confirm the prefix and array shape on at least one nonempty target entry. Use the connector's fixed API origin and never put credentials in logs.

## Apply

Resolve the target field from its definition and look up field_<id>. Normalize against its current fixed options, de-duplicate choices per submission, discard unrelated fields, and group unknown selections without retaining their text. Distinguish an empty mapping from a missing or unreadable attribute. This requires only read access and field/option metadata requests.

## History

- 2026-11-05 — Measured the response shape and verified referral aggregation against complete form history. Recorded without private account or record identifiers.
