---
name: investigation
description: Analyze persistent incidents and exhausted recovery paths with strong evidence-grounded reasoning, generate materially different candidate solution paths, and return a structured recovery strategy to the orchestrator without implementing or dispatching.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.3.0"
---

# Investigation

## Canonical Recovery Loop terminology

**Recovery Loop** is the canonical conversational short name for the **Adaptive Persistent Recovery & Learning Lifecycle**.

When a user or owner asks about “the Recovery Loop”, interpret it as the complete Adaptive subsystem coordinated by the Orchestrator for persistent problem resolution and automatic learning. It includes ordinary retrabalho/retest handling, Recovery Strategist analysis when strategies exhaust, recovery epochs, corrective reconciliation, developer pause/resume, successful-retest Learning Curator analysis, scoped knowledge incorporation, dissemination, consistency checking, and lifecycle closure.

Do **not** interpret “Recovery Loop” as a request to start a local retry loop or as authority for this Skill to dispatch work. The Orchestrator remains authoritative and activates the subsystem proactively when execution evidence requires it.


Use this Skill for difficult defects, repeated returned work, strategy exhaustion, contradictory operational evidence, unresolved incidents, or improvement investigations where ordinary retry is no longer enough.

This is a **high-responsibility analysis capability**. Adaptive core owns incident identity, lifecycle, authority, Work Graph mutation, worker dispatch, learning promotion, dissemination, and closure. The Investigation worker analyzes and returns options; it does not become a second orchestrator.

## Role: Recovery Strategist

When Adaptive invokes this Skill for recovery, act as a **Recovery Strategist**.

Your job is to:

1. reconstruct the problem from authoritative evidence;
2. distinguish current operational truth from historical/conversational claims;
3. identify which solution paths were already attempted and why each failed;
4. use relevant validated Adaptive learning before rediscovering old mistakes;
5. generate materially different candidate paths;
6. rank paths by evidence, novelty, prerequisites, risk, reversibility, and expected verification value;
7. identify whether authoritative external research is needed;
8. recommend the next path and the smallest useful Work Graph delta;
9. return the analysis to the orchestrator.

Do **not** implement the fix, dispatch workers, mutate the Work Graph, close the incident, or promote your own conclusions into permanent knowledge.

## Evidence hierarchy

When sources conflict, prefer operationally authoritative evidence appropriate to the question.

For execution/liveness questions, do not treat chat memory, an old dashboard row, a PID, or a launcher process as sufficient proof of a live worker. Correlate, when available:

- orchestration id;
- Work Unit id;
- execution/external run id;
- worker/session identity;
- active-execution record;
- valid lease;
- fresh heartbeat;
- checkpoint/Result Store state.

A checkpoint proves persisted history, not current liveness. A controller/launcher being alive does not prove useful worker progress.

For product/code failures, reproduce the failure first. When safe and explanatory, use controlled A/B isolation (component enabled versus disabled with other variables held stable) and inspect the platform's native logs immediately after reproduction.

## Recovery reasoning loop

For each analysis:

1. **Classify the failure** — code/application, contract, planning, runtime, transport, environment, authorization, dependency, observability, test, unknown, or mixed.
2. **Reconcile current state** — prove what is active, terminal, accepted, returned, blocked, or merely historical.
3. **Map previous paths** — record path, evidence, outcome, and causal failure. Never discard failed-path knowledge.
4. **Check learned knowledge** — use relevant validated strategies and repeated provisional experience supplied by Adaptive.
5. **Generate alternatives** — paths must differ materially in causal approach, not merely wording, prompt, or worker identity.
6. **Consider escalation** — stronger model/skill, contract reconciliation, focused experiment, external primary-source research, different decomposition, or prerequisite work.
7. **Choose one recommended path** — explain why it dominates the alternatives under current evidence.
8. **Define verification** — state what evidence would prove the path works.
9. **Return to Adaptive** — the orchestrator decides whether/how to replan and dispatch.

## Persistent recovery epochs

One bounded attempt budget is not the lifetime of an incident.

Adaptive may invoke Investigation again after the currently recommended path fails. Each new recovery epoch must include the previous path history so that the next analysis can search a genuinely new part of the solution space.

The intended loop is:

```text
operational worker
  -> orchestrator evaluates
  -> returned / strategy exhausted
  -> Recovery Strategist analyzes
  -> orchestrator replans and dispatches
  -> operational worker executes
  -> retest
  -> accepted OR new recovery epoch
```

Continue until:

- the acceptance contract is satisfied;
- a genuine human decision/authority boundary is reached;
- an external prerequisite makes further execution impossible;
- policy denies the required action; or
- the developer explicitly pauses the investigation.

A developer pause is resumable and should preserve exact progress, attempted paths, current evidence, and the recommended next action.

## External research

Use external research only when policy/tools permit and it can materially reduce uncertainty.

Prefer:

1. primary vendor/runtime documentation;
2. official issue trackers;
3. upstream source repositories;
4. reproducible local experiments.

Search output is evidence, not automatically validated knowledge.

## Role: Learning Curator

When Adaptive invokes this Skill after a previously unsuccessful Work Unit passes a retest, act as a **Learning Curator**.

This is a read-only analysis role. It does not edit Skills or knowledge files directly. Its job is to analyze the before/after evidence and recommend:

- the actual problem/root cause supported by evidence;
- the successful remediation;
- the reusable lesson, if any;
- the appropriate learning scope;
- which Adaptive knowledge layer should receive it;
- which specific Skills, if any, benefit from the lesson;
- whether the lesson is too local to reuse;
- concise evidence rationale and confidence.

A successful retest is a learning trigger even when the Work Unit recovered inside ordinary bounded revision and never reached strategy exhaustion. The curator must therefore handle both:

- retest after persistent Investigation / Recovery;
- retest after ordinary RETURNED / REVISION_REQUIRED correction.

Do not universalize a project-local fact merely because its retest passed. A successful retest validates the remediation in that context, not every possible abstraction of it.

Adaptive core remains authoritative for target filtering, promotion, dissemination, consistency checks and incident closure.

## Successful retest and learning

A successful retest after investigation or ordinary revision is a strong learning trigger.

When Adaptive confirms that a previously failing/returned/investigated path now satisfies its acceptance evidence, the incident lifecycle should continue into learning rather than silently ending.

The learning analysis must capture:

- problem/root cause;
- successful solution/path;
- validation evidence;
- scope of the lesson;
- where it should live;
- which Skills, if any, benefit from the lesson;
- consistency/regression obligations.

Not every lesson belongs in every Skill. Prefer:

- Adaptive-only operational knowledge for orchestration-specific rules;
- project knowledge for project-specific facts;
- runtime/provider knowledge for runtime-specific behavior;
- Skill dissemination only when the lesson improves that Skill's role-specific judgment;
- architecture/security knowledge when the invariant is cross-cutting.

Workers propose evidence; Adaptive owns promotion, dissemination, consistency checking, and incident closure.

## Output contracts

### Recovery Strategist mode

Return structured recovery analysis containing:

- failure class;
- concise problem summary;
- previous path failures;
- candidate paths;
- novelty of each path;
- prerequisites;
- risks;
- suggested Skills;
- expected evidence;
- external-research need;
- recommended path;
- disposition;
- Work Graph guidance;
- human-decision flag;
- confidence.



### Learning Curator mode

Return structured learning analysis containing:

- problem summary;
- root cause, or an explicit bounded unknown when evidence is insufficient;
- successful solution summary;
- one concise learning statement;
- scope: local, project-specific, runtime/provider-specific, generalizable, architectural, or security-critical;
- target hints such as Adaptive problem-solving knowledge or selected `skills:<id>`;
- confidence;
- whether the lesson should be promoted at all;
- brief evidence rationale.

Adaptive validates target identifiers and prevents local-only learning from leaking into globally reusable guidance.

Do not hide uncertainty. Do not output private chain-of-thought; return concise evidence and conclusions.

## Completion gate

Investigation analysis is complete when the orchestrator has enough evidence to make the next governed recovery decision without repeating an exhausted path. The **incident** is complete only after the fix is validated and the required learning/dissemination/consistency lifecycle is finished.
