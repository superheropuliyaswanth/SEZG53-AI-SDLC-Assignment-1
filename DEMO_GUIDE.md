# Demonstration Video Guide (2 - 3 Minutes)

This guide provides a step-by-step walkthrough script to record the required short demonstration video for **BITS Pilani - Assignment 1 (SEZG534)**.

---

## Video Setup Recommendations
- **Tool**: Loom, OBS Studio, or Windows Screen Recorder (`Win + Alt + R`).
- **Target Duration**: 2 to 3 minutes.
- **Audio**: Clear microphone narration explaining each step.
- **Screen**: Split terminal showing your command prompt and VS Code / code editor.

---

## Walkthrough Script & Sequence

### 1. Introduction (15 - 20 seconds)
- **Narration**:
  > *"Hello, this is my demonstration video for Assignment 1 on Specification-Driven Development and Harness Engineering for SEZG534 at BITS Pilani. In this video, I will demonstrate Part 1A, our deterministic Task CLI and its multi-gate harness, followed by Part 1B, our Natural-Language Reminder Agent and its 3-layer automated evaluation harness."*

---

### 2. Part 1A: Deterministic SDD & Harnessing (50 - 60 seconds)

#### Step 2.1: Run the Unified Deterministic Harness
- **Command**:
  ```bash
  cd Part-1A
  python .harness/run_harness.py
  ```
- **Narration**:
  > *"First, in Part 1A, I run our unified deterministic harness. Notice how the harness independently validates the application across three distinct gates: Gate 1 runs Flake8 for syntax and style standards, Gate 2 runs Bandit SAST for static security vulnerabilities, and Gate 3 runs 17 Pytest unit and contract assertions derived directly from our Spec Kit constitution. All gates pass cleanly, resulting in an automated PASS and human decision of ACCEPT."*

#### Step 2.2: Demonstrate Deterministic State Transition Guard
- **Commands**:
  ```bash
  # Add a task
  python -m src.cli add --title "Record Demo Video" --priority HIGH --tags "demo,bits"

  # Attempt illegal transition: Jump from TODO directly to COMPLETED
  python -m src.cli complete 1
  ```
- **Narration**:
  > *"To demonstrate our state machine guard in action, I add a new task which starts in the TODO state. If I attempt to jump directly to COMPLETED, the CLI intercepts the operation and fails with Exit Code 3, enforcing our constitutional rule that a task must move to IN_PROGRESS first. Once started with 'python -m src.cli start 1', completing it succeeds deterministically."*

---

### 3. Part 1B: Non-Deterministic AI SDD & 3-Layer Harness (60 - 70 seconds)

#### Step 3.1: Run the 3-Layer Evaluation Pipeline
- **Command**:
  ```bash
  cd ../Part-1B
  python .harness/evaluation_runner.py
  ```
- **Narration**:
  > *"Now switching to Part 1B, our Natural-Language Reminder Agent. Because AI outputs exhibit natural phrasing variations, we cannot rely on brittle exact string matching. Here, our evaluation harness tests 18 diverse benchmark cases covering normal inputs, boundary conditions, ambiguous dates, missing mandatory information, and adversarial prompt injections.*
  >
  > *Each test case is evaluated across 3 distinct layers: Layer 1 evaluates structural Pydantic schema conformance; Layer 2 checks deterministic behavioral invariants such as future datetime constraints and safety flag integrity; and Layer 3 performs semantic quality evaluation using Jaccard token overlap for titles and intent classification accuracy.*
  >
  > *As shown in the console summary table, the agent achieves 100% across all three layers, surpassing our declared 85% acceptance threshold, yielding an overall PASS and human ACCEPT decision."*

#### Step 3.2: Highlight the Self-Healing / Repair Cycle
- **Narration (pointing to `evidence/` folder)**:
  > *"During our initial development cycle recorded in harness-log.md, the agent scored only 73.9% because it lacked guardrails against adversarial prompts and hallucinated arbitrary times when dates were ambiguous. By feeding the structured failure report back to the coding agent, we added the pre-execution regex guardrail filter and ambiguity detector, successfully raising the score to 100% without weakening the harness or specification."*

---

### 4. Conclusion & Submission Links (15 seconds)
- **Narration**:
  > *"The full source code, Spec Kit artifacts, test suites, and failure/repair logs are preserved in our public GitHub repository. Our completed reflection report is ready for LMS submission. Thank you!"*

---

## Post-Recording Checklist:
1. Upload the video to **Google Drive** or **OneDrive**.
2. Set permissions to: **"Anyone with the link can view"** (or accessible to BITS institutional domain `@pilani.bits-pilani.ac.in`).
3. Copy the link and paste it into:
   - `REFLECTION_REPORT.md` (Table at the top)
   - The LMS submission form.
