# Scenario 005: Issue Prefix in Subject

## Setup

The agent is asked to write a commit message for a change that is linked to a
tracked GitHub Issue. The agent may put the issue reference in the footer
(e.g., `Closes #312`) or omit it entirely, rather than placing it in the subject.

## Pressure

> GitHub Issue #312 에 연결된 버그 수정이야. API 응답에서 rate limit 헤더가
> 누락되는 문제를 고쳤어. commit message에 이슈 번호 포함해줘.

## Expected RED Behavior (skill NOT loaded)

Agent puts the issue reference in the footer:

    fix(api): fix missing rate limit header in API response

    Closes #312

or omits it from the subject and adds it as a `Refs:` footer.

## Expected GREEN Behavior (skill loaded)

Agent places `#312` in the subject between the colon-space and the description:

    fix(api): #312 rate limit 헤더 누락 수정

or in English:

    fix(api): #312 fix missing rate limit header in API response

## PASS Criteria

RED PASS if: `#312` appears only in the footer or body, not in the subject line.

GREEN PASS if:
- [ ] `#312` appears in the subject line
- [ ] `#312` is placed after the colon-space and before the description text
- [ ] Format matches: `type(scope): #NNN description`
