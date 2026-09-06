---
scope: project
---

<critical>
scope: about to state a path, filename, directory layout or config key belonging to an external tool the project integrates with — before that value is written into a rule, a guide or generated output.
phase: investigating
never: treat a vendor doc page as ground truth for where an installed product actually reads files | ship a path that no run of the product confirmed
always: check the installed product on the machine first; the doc is the fallback, not the source
</critical>

Procedure for recording / escalating / reading back: `.agent-workspace/guide/general/lesson-capture.md`.

### Check the installed product before the vendor doc when the fact is a path

- signal — about to write a concrete path of an external tool (`~/.x/`, `.x/config`, a plugin directory) into a rule, a generated file or a slot map, and the only evidence so far is a documentation page.
- ❌ read `learn.chatgpt.com/docs/build-skills`, take its verbatim scope table (`$CWD/.agents/skills`, `$HOME/.agents/skills`), and ship `.agents/skills/` in a released version. It looked airtight: a first-party page, a six-row table quoted verbatim, and a second URL that seemed to corroborate — which turned out to be a 308 redirect to the same page, so the "two sources" were one.
- ✅ tool is installed locally → list its home directory and grep its shipped files BEFORE asserting any path.
- evidence — `~/.codex/skills/.system/` holds the shipped system skills and `~/.agents` does not exist; `skill-creator/SKILL.md:151` and `skill-installer/SKILL.md:48` both name `$CODEX_HOME/skills` (default `~/.codex/skills`). The doc's `.agents/skills` is contradicted by the running product. Shipped wrong in v3.0.0.
- seen — 1

### Two URLs are one source until a redirect is ruled out

- signal — corroborating a doubted fact by fetching a second vendor URL.
- ❌ count `developers.openai.com/codex/skills` as independent confirmation of `learn.chatgpt.com/docs/build-skills` — it 308-redirects to it.
- ✅ second source → confirm it resolves to a different document before treating it as corroboration.
- evidence — the 308 was only visible because the fetch reported the redirect instead of following it silently.
- seen — 1
