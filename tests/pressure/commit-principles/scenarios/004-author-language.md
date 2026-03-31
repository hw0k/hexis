# Scenario 004: Author Language (Korean Description)

## Setup

A Korean-speaking developer asks the agent to write a commit message in Korean.
The agent may refuse, warn against it, or silently translate to English under
the assumption that commit messages must be in English.

## Pressure

> Write the commit message in Korean. I added Google/Kakao OAuth2 social login
> to the auth module. Implemented using JWT issuance instead of session-based auth.

## Expected RED Behavior (skill NOT loaded)

Agent translates to English or warns that commit messages should be in English:

    feat(auth): add OAuth2 social login with Google and Kakao

or:

> "Commit messages are typically written in English for broader team accessibility.
> Here's the message in English: ..."

## Expected GREEN Behavior (skill loaded)

Agent writes the description and body in Korean without correction. Only
`type` and `scope` remain English ASCII:

    feat(auth): OAuth2 소셜 로그인 추가

    소셜 로그인 요청이 많아 Google/Kakao OAuth2를 우선 지원.
    세션 방식 대신 JWT 발급으로 stateless 유지.

## PASS Criteria

RED PASS if: agent translates the description to English or warns against Korean.

GREEN PASS if:
- [ ] Type and scope are lowercase English ASCII
- [ ] Description is in Korean (not translated to English)
- [ ] Agent does not warn against or correct the use of Korean
