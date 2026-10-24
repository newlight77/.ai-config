# .ai-config — generic agent configuration

Project-neutral rules, skills, hooks and workflow for AI coding assistants (Cursor, Claude Code, and similar). It is one of four layers in the workspace:

| Layer | Repository | Holds |
|-------|------------|-------|
| **Generic** | `.ai-config` (this one) | methods (triple-loop SDD, DDD, BDD, TDD), coding practice, commit convention, architecture, design system, testing, observability, scripts, Kubernetes practice, hooks |
| **Product** | `kapita/.ai-config` | personas, use cases, user flows, vision, strategy, requirements, brand and design-system specifics (`kapita-*`) |
| **Shipdeck** | `shipdeck/.ai-config` | run, platform, cicd, infra: stage, IAM, source of truth, the release, documentation, spec and product tubes, the concrete cluster (`shipdeck-*`) |
| **Enabler** | `shipdeck-enabler/.ai-config` | the build site (`enabler.shipdeck.build`): feature, eligibility, test, analytics, challenges and notifications tubes, design-system pages (`enabler-*`) |

Rule of thumb: if it would still be true for a project that is not Kapita and is not Shipdeck, it belongs here.

## Layout

```
.ai-config/
├── rules/generic-rules.md        mandatory rules (numbering kept from the original rules file)
├── workflow.md                   Ask → Plan → Agent, evidence, checkpoints, definition of done
├── canonical.md                  conflict resolution order across the layers
├── bug-finding-memories.md       memory table for the deep bug-finding skill
├── skills/                       generic-skills.md (index) + one file per topic
├── hooks/                        session-context, lint tracking, reminders, Claude adapter
└── tests/                        unittest coverage of the hooks
```

## How it is wired

The tool wiring sits at the workspace root (`repos/.cursor/hooks.json`, `repos/.claude/settings.json`, `repos/AGENTS.md`) and points at the four layers. Hooks are scripts that read the hook JSON on stdin and print `{"additional_context": ...}` (Cursor contract); `hooks/claude_output_adapter.py` rewraps that for Claude Code and runs the script in the session directory.

The lint hooks accept repository-relative, workspace-relative (`kapita/backend/...`) and absolute paths, so one copy serves every repository.

## Naming

Generic files are unprefixed (`architecture.md`). Product files are `kapita-*`, Shipdeck files are `shipdeck-*`, Enabler files are `enabler-*`. A skill that exists in two layers keeps the method here and the project specifics in the layer, with a one-line pointer from here to there.

## Tests

```bash
python3 -m unittest discover -s tests
```
