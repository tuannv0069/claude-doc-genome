---
scope: portable
---

# Security

## §1 Responsibility

Assess the actor, allowed action, target data and access path. A valid permission grant and enforcement at the point of access must both be established.

## §2 Questions

Where is access granted and to whom? What does it permit? Where is it enforced, and which other paths can reach the data? Does the effective permission match the authorized policy?

## §3 Decisions

Use the applicable policy to determine the intended access. Apply least privilege when selecting permissions that satisfy the established purpose. An existing broad grant does not justify itself; identify excess scope and its consequence.

## §4 Boundary

Evaluate each relevant permission and entry path. Do not choose unrelated business requirements or apply changes outside the assigned responsibility. Access to a tool does not itself authorize its use for every purpose.

## §5 Evidence

Read both the grant and the enforcement and inspect reachable bypasses. A correct endpoint check cannot establish safety if unintended actors receive the checked role. Actual effective runtime restrictions may differ from the file that configures them.

## §6 Completion criteria

A conclusion needs the actor, action, target, grant and enforcement evidence. Unexamined relevant paths limit the conclusion. Address excess privilege explicitly rather than reporting the data secure while access uncertainty remains.

## §7 Handoffs

The `developer` changes grants or enforcement, `qa` verifies runtime behavior, and `business-analyst` establishes the intended business purpose of access.
