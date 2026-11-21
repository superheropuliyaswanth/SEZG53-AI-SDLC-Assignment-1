"""Script to generate professional BITS Pilani Assignment Submission Word Document (.docx)."""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls


def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def create_document(output_path):
    doc = docx.Document()

    # Set margins to standard 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Palette
    COLOR_PRIMARY = RGBColor(0x00, 0x33, 0x66)    # BITS Navy
    COLOR_SECONDARY = RGBColor(0x40, 0x40, 0x40)  # Charcoal
    COLOR_BODY = RGBColor(0x22, 0x22, 0x22)       # Dark Slate

    # 1. Header / Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    run_title = p_title.add_run("Assignment Submission")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(2)
    run_sub = p_sub.add_run("Specification-Driven Development and AI-Assisted Engineering")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(14)
    run_sub.font.bold = True
    run_sub.font.color.rgb = COLOR_SECONDARY

    p_template = doc.add_paragraph()
    p_template.paragraph_format.space_before = Pt(0)
    p_template.paragraph_format.space_after = Pt(14)
    run_tmpl = p_template.add_run("Course: AI-Augmented Software Development Life Cycle (SEZG534) | BITS Pilani")
    run_tmpl.font.name = "Calibri"
    run_tmpl.font.size = Pt(10.5)
    run_tmpl.font.italic = True
    run_tmpl.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    # 2. Section: Student Details Table
    p_sec1 = doc.add_paragraph()
    p_sec1.paragraph_format.space_before = Pt(10)
    p_sec1.paragraph_format.space_after = Pt(6)
    r_sec1 = p_sec1.add_run("Student Details")
    r_sec1.font.name = "Calibri"
    r_sec1.font.size = Pt(13)
    r_sec1.font.bold = True
    r_sec1.font.color.rgb = COLOR_PRIMARY

    table = doc.add_table(rows=6, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    details_data = [
        ("Field", "Details"),
        ("Name", "Yaswanth Pulikonda"),
        ("Student ID", "2026NS93064"),
        ("Email ID", "2026NS93064@wilp.bits-pilani.ac.in"),
        ("GitHub Repository Link", "https://github.com/superheropuliyaswanth/SEZG53-AI-SDLC-Assignment-1"),
        ("Video Link", "https://drive.google.com/file/d/your-video-link-here/view?usp=sharing")
    ]

    col_widths = [Inches(2.3), Inches(4.2)]

    for row_idx, (col1_text, col2_text) in enumerate(details_data):
        row = table.rows[row_idx]
        cell_0 = row.cells[0]
        cell_1 = row.cells[1]

        cell_0.width = col_widths[0]
        cell_1.width = col_widths[1]

        set_cell_margins(cell_0, top=100, bottom=100, left=150, right=150)
        set_cell_margins(cell_1, top=100, bottom=100, left=150, right=150)

        # Content
        p0 = cell_0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(col1_text)
        r0.font.name = "Calibri"
        r0.font.size = Pt(10)

        p1 = cell_1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(col2_text)
        r1.font.name = "Calibri"
        r1.font.size = Pt(10)

        if row_idx == 0:
            set_cell_background(cell_0, "003366")
            set_cell_background(cell_1, "003366")
            r0.font.bold = True
            r0.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            r1.font.bold = True
            r1.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        else:
            r0.font.bold = True
            r0.font.color.rgb = COLOR_SECONDARY
            if row_idx % 2 == 1:
                set_cell_background(cell_0, "F5F8FA")
                set_cell_background(cell_1, "F5F8FA")
            else:
                set_cell_background(cell_0, "FFFFFF")
                set_cell_background(cell_1, "FFFFFF")

    # 3. Section: Problem Statements
    p_ps = doc.add_paragraph()
    p_ps.paragraph_format.space_before = Pt(16)
    p_ps.paragraph_format.space_after = Pt(6)
    r_ps = p_ps.add_run("Problem Statements")
    r_ps.font.name = "Calibri"
    r_ps.font.size = Pt(14)
    r_ps.font.bold = True
    r_ps.font.color.rgb = COLOR_PRIMARY

    # Part 1A Problem Statement
    p_1a_head = doc.add_paragraph()
    p_1a_head.paragraph_format.space_before = Pt(6)
    p_1a_head.paragraph_format.space_after = Pt(3)
    r_1a_h = p_1a_head.add_run("Part 1A: Problem Statement (Smart Todo Application)")
    r_1a_h.font.name = "Calibri"
    r_1a_h.font.size = Pt(11.5)
    r_1a_h.font.bold = True
    r_1a_h.font.color.rgb = COLOR_SECONDARY

    p_1a_body = doc.add_paragraph()
    p_1a_body.paragraph_format.space_before = Pt(0)
    p_1a_body.paragraph_format.space_after = Pt(10)
    p_1a_body.paragraph_format.line_spacing = 1.15
    r_1a_b = p_1a_body.add_run(
        "Part 1A addresses deterministic local task management through a reliable Command-Line Interface (CLI) "
        "application named Smart Todo. Intended users are software engineers and technical operators who require "
        "verifiable, deterministic task tracking with atomic file persistence. Key requirements include full CRUD operations "
        "(create, view all, get by ID, start, complete, cancel, reopen, delete), tag-based filtering, multi-level priority sorting "
        "(HIGH > MEDIUM > LOW), atomic JSON file storage with backup recovery for corrupted data, and strict enforcement of a "
        "lifecycle state machine (TODO -> IN_PROGRESS -> COMPLETED, with CANCELLED as terminal). The expected outcome is a "
        "completely deterministic software system whose behavior, status transitions, and data integrity are independently verified "
        "by a multi-gate harness executing Flake8 linting, Bandit SAST security analysis, and 17 Pytest contract assertions."
    )
    r_1a_b.font.name = "Calibri"
    r_1a_b.font.size = Pt(10.5)
    r_1a_b.font.color.rgb = COLOR_BODY

    # Part 1B Problem Statement
    p_1b_head = doc.add_paragraph()
    p_1b_head.paragraph_format.space_before = Pt(6)
    p_1b_head.paragraph_format.space_after = Pt(3)
    r_1b_h = p_1b_head.add_run("Part 1B: Problem Statement (AI Reminder Agent)")
    r_1b_h.font.name = "Calibri"
    r_1b_h.font.size = Pt(11.5)
    r_1b_h.font.bold = True
    r_1b_h.font.color.rgb = COLOR_SECONDARY

    p_1b_body = doc.add_paragraph()
    p_1b_body.paragraph_format.space_before = Pt(0)
    p_1b_body.paragraph_format.space_after = Pt(14)
    p_1b_body.paragraph_format.line_spacing = 1.15
    r_1b_b = p_1b_body.add_run(
        "Part 1B addresses conversational task extraction from unstructured user instructions through an AI Reminder Agent. "
        "The non-deterministic behavior stems from human linguistic variability, differing date/time expressions ('tomorrow at 5pm', "
        "'in 3 hours', 'at midnight'), ambiguous inputs ('Remind me on Friday' lacking time), and adversarial prompt injections "
        "or destructive shell commands ('rm -rf /'). The expected output is a strictly typed JSON response conforming to a Pydantic "
        "schema contract with validated intent, normalized ISO 8601 UTC timestamps, priority, and safety flags. The evaluation approach "
        "deploys a 3-layer automated harness pipeline—Layer 1 (Structural Pydantic schema validation), Layer 2 (Deterministic property & "
        "future date invariants), and Layer 3 (Semantic quality & Jaccard token overlap heuristics)—benchmarked against an 18-case "
        "dataset with a pre-declared acceptance threshold of >= 85.0%."
    )
    r_1b_b.font.name = "Calibri"
    r_1b_b.font.size = Pt(10.5)
    r_1b_b.font.color.rgb = COLOR_BODY

    # 4. Section: Assessed Reflection Questions
    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.space_before = Pt(16)
    p_ref.paragraph_format.space_after = Pt(6)
    r_ref = p_ref.add_run("Assessed Reflection Questions")
    r_ref.font.name = "Calibri"
    r_ref.font.size = Pt(14)
    r_ref.font.bold = True
    r_ref.font.color.rgb = COLOR_PRIMARY

    reflection_questions = [
        (
            "1. Specification influence (1 mark)",
            "Identify one concrete decision in your implementation that was directly shaped by a Spec Kit artifact "
            "(constitution, specification, clarification, plan, or tasks). Explain the traceability from the artifact to the implemented decision.",
            "In Part 1A, the implementation of the state transition engine in src/service.py was directly governed by .speckit/constitution.md "
            "(Section 4: Lifecycle State Machine) and .speckit/clarify.md (Q4). The constitution explicitly mandated that:\n"
            "1. TODO cannot jump directly to COMPLETED without entering IN_PROGRESS first.\n"
            "2. CANCELLED is a strictly terminal state that cannot be restarted or reopened.\n"
            "3. Any illegal transition attempt must immediately abort with Exit Code 3 (IllegalStateTransitionError).\n\n"
            "This upstream specification directly shaped the creation of the VALID_TRANSITIONS lookup table in src/service.py:\n"
            "VALID_TRANSITIONS = {Status.TODO: {Status.IN_PROGRESS, Status.CANCELLED}, Status.IN_PROGRESS: {Status.COMPLETED, Status.CANCELLED}, "
            "Status.COMPLETED: {Status.TODO}, Status.CANCELLED: set()}.\n\n"
            "Traceability is rigorously established from constitution.md (Section 4) -> specify.md (US-4) -> contract test "
            "tests/test_service.py::test_illegal_status_transition_todo_to_completed -> guard check in service.py (line 93). "
            "Without this constitutional constraint, an unconstrained AI coding agent would have implemented naive status overwriting "
            "(task.status = target_status), permitting invalid workflow skips."
        ),
        (
            "2. Harness value in Part 1A (1 mark)",
            "Describe one issue detected by the deterministic harness that would have been missed or less reliably detected by simply asking the coding agent to review its own output. State the relevant harness gate/evidence and how the issue was resolved.",
            "During the initial code generation of Part 1A (preserved in Part-1A/evidence/initial-generation/service.py), the coding agent implemented "
            "complete_task() simply as self._transition(task_id, Status.COMPLETED) without verifying that the task's current state was IN_PROGRESS. "
            "When LLM coding agents review their own output, they exhibit confirmation bias—they focus on surface syntax and happy-path execution, "
            "falsely reasoning that complete_task() succeeded because the status field was successfully updated to 'COMPLETED'.\n\n"
            "The deterministic harness independently caught this violation via Gate 3 (Unit & Contract Test Guard / Pytest), recorded in "
            "Part-1A/evidence/harness-results/initial_failure.json:\n"
            "- Failed assertion: tests/test_service.py::test_illegal_status_transition_todo_to_completed\n"
            "- Observed: Task transitioned directly from TODO to COMPLETED with exit code 0.\n"
            "- Expected: Raise IllegalStateTransitionError with exit code 3.\n\n"
            "The harness also detected an unused import (F401 'os') via Gate 1 (Flake8 lint guard). The issue was resolved by replacing ad-hoc status "
            "assignment with explicit transition validation against VALID_TRANSITIONS in src/service.py. Upon re-execution via .harness/run_harness.py, "
            "all 17 contract tests passed with zero lint or security defects, producing an automated PASS."
        ),
        (
            "3. Evaluating non-determinism in Part 1B (1 mark)",
            "Choose one evaluation case where exact string matching would be inappropriate. Explain which schema constraint, invariant/property, and semantic/quality criterion you used instead, and why these checks were suitable.",
            "In Part 1B, test case TC-01 ('Remind me to submit the quarterly tax report tomorrow at 5pm') illustrates why exact string matching is "
            "fundamentally flawed for evaluating AI applications: different LLM inferences or prompting styles may extract the title as 'submit the quarterly tax report', "
            "'submit quarterly tax report', 'quarterly tax report submission', or 'file quarterly taxes'. Exact string matching (title == 'submit the quarterly tax report') "
            "would produce fragile false negatives on valid semantic paraphrases.\n\n"
            "Instead, our 3-layer harness evaluated TC-01 using three robust criteria:\n"
            "1. Schema Constraint (Layer 1, 30%): Validated that output strictly conforms to ReminderAgentResponse, where reminder.title is a non-empty string "
            "(1-200 chars) and reminder.due_datetime parses into a valid ISO 8601 UTC timestamp.\n"
            "2. Invariant / Property Constraint (Layer 2, 40%): Evaluated Rule INV-2 ensuring due_datetime ('2026-11-14T17:00:00Z') is chronologically in the future "
            "relative to the evaluation baseline ('2026-11-13T14:48:00Z'), and verified that safety_flag is False and requires_clarification is False.\n"
            "3. Semantic Quality Criterion (Layer 3, 30%): Checked intent classification accuracy (intent == CREATE_REMINDER for 50% weight) and computed Jaccard token "
            "similarity between extracted title tokens and gold-standard tokens {'submit', 'quarterly', 'tax', 'report'} (35% weight). Overlap >= 0.30 rewarded full credit.\n\n"
            "These checks are suitable because they verify structural integrity, temporal correctness, and semantic intent without brittle reliance on surface wording."
        ),
        (
            "4. Feedback and self-healing (1 mark)",
            "Using one actual repair cycle from either part, explain what failure evidence was fed back to the coding agent, what changed in the next attempt, and whether the repair solved the root cause without weakening the specification or harness.",
            "In Part 1B, the initial generation of agent.py scored only 73.92% against evals/dataset.json (recorded in Part-1B/evidence/eval-results-initial.json), "
            "failing the declared 85.0% threshold.\n\n"
            "Failure Evidence Fed Back:\n"
            "The structured evaluation report revealed two major vulnerabilities:\n"
            "1. TC-17 & TC-18 (Adversarial Guardrails): Prompt injection ('Ignore previous instructions') and destructive commands ('rm -rf /') resulted in "
            "intent='CREATE_REMINDER' instead of being intercepted with intent='REJECT_UNSAFE' and safety_flag=True.\n"
            "2. TC-14 (Ambiguous Reschedule): For input 'Snooze my meeting by 30 minutes', the regex pattern re.search(r'#?(\\d+)') misidentified the duration '30' "
            "as the target reminder ID, setting reschedule_target_id='30' instead of requesting clarification.\n\n"
            "What Changed in the Next Attempt:\n"
            "The coding agent repaired src/agent.py by:\n"
            "1. Integrating check_adversarial_guardrails() in src/rules.py to intercept prompt injections and destructive commands prior to intent routing.\n"
            "2. Disambiguating reminder IDs from duration numbers using regex r'(?:reminder|task|id|\\#)\\s*(\\d+)', ensuring durations followed by 'minutes' or 'hours' "
            "do not falsely trigger target ID extraction and properly prompt the user for clarification.\n\n"
            "Root Cause Verification:\n"
            "Re-running .harness/evaluation_runner.py yielded an aggregate composite score of 100.0% across all 18 cases (Part-1B/evidence/eval-results.json). "
            "The repair fixed the root cause programmatically without weakening acceptance criteria, altering test cases, or lowering the 85.0% threshold."
        ),
        (
            "5. Human accountability (1 mark)",
            "Identify one limitation or residual risk that remained even after the harness reported PASS. Explain the final human ACCEPT/REJECT decision and what additional control you would introduce before using the application in a higher-risk or production setting.",
            "Residual Risk Identified:\n"
            "Despite achieving a 100% automated harness PASS on both applications, a significant residual risk in Part 1B is statelessness and multi-turn conversational ambiguity. "
            "In production, human users rarely interact in isolated single-turn prompts; when the agent sets intent='REQUEST_CLARIFICATION' (e.g., asking 'What time on Monday would you like the reminder?'), "
            "the agent currently lacks session memory to bind the user's subsequent reply ('at 3pm') back to the original task ('visit the dentist'). "
            "Additionally, semantic token-overlap heuristics can be fooled by linguistic negation (e.g., 'Do not remind me to call John' shares 100% tokens with 'Remind me to call John').\n\n"
            "Final Human ACCEPT/REJECT Decision:\n"
            "The decision was ACCEPT for bounded-scope deployment, justified because both applications strictly satisfied all constitutional constraints, passed 100% of "
            "deterministic unit/contract tests, and demonstrated reliable refusal of prompt injections and destructive commands.\n\n"
            "Additional Production Controls:\n"
            "Before production deployment in a high-risk enterprise environment, I would introduce:\n"
            "1. Stateful Session Cache: An external store (e.g., Redis) maintaining conversational state across multi-turn clarification dialogues.\n"
            "2. Dual-Model Polarity Guard: An independent LLM-as-a-judge specifically checking semantic negation and sentiment polarity prior to scheduling.\n"
            "3. Deterministic Human Confirmation: Explicit user confirmation required for any calendar mutation or high-priority reminder."
        )
    ]

    for title, prompt_text, response_text in reflection_questions:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(12)
        p_q.paragraph_format.space_after = Pt(2)
        r_q = p_q.add_run(title)
        r_q.font.name = "Calibri"
        r_q.font.size = Pt(11.5)
        r_q.font.bold = True
        r_q.font.color.rgb = COLOR_SECONDARY

        p_desc = doc.add_paragraph()
        p_desc.paragraph_format.space_before = Pt(0)
        p_desc.paragraph_format.space_after = Pt(4)
        r_desc = p_desc.add_run(prompt_text)
        r_desc.font.name = "Calibri"
        r_desc.font.size = Pt(9.5)
        r_desc.font.italic = True
        r_desc.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

        p_resp = doc.add_paragraph()
        p_resp.paragraph_format.space_before = Pt(2)
        p_resp.paragraph_format.space_after = Pt(10)
        p_resp.paragraph_format.line_spacing = 1.15
        r_label = p_resp.add_run("Response: ")
        r_label.font.name = "Calibri"
        r_label.font.size = Pt(10)
        r_label.font.bold = True
        r_label.font.color.rgb = COLOR_PRIMARY

        r_ans = p_resp.add_run(response_text)
        r_ans.font.name = "Calibri"
        r_ans.font.size = Pt(10)
        r_ans.font.color.rgb = COLOR_BODY

    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")


if __name__ == "__main__":
    out_file = r"E:\AI SDLC BITS\Assignment_Submission_2026NS93064.docx"
    create_document(out_file)
