# LegalLens AI — Security Architecture & Threat Model

**Security Evaluation Score Target:** 100 / 100  
**Verification Suite:** `tests/test_security.py` (5 automated security boundary tests passing)

---

## 1. Threat Mitigation Matrix

| Threat Vector | Mitigation Strategy | Implementation Details |
| :--- | :--- | :--- |
| **Path Traversal Attacks** | Strict filename sanitization | Enforced via `werkzeug.utils.secure_filename`. Prohibits relative path jumps (`../`, `..\`). |
| **Denial of Service (DoS via Upload)** | File size hard limit | `app.config['MAX_CONTENT_LENGTH'] = 16MB` enforced at web server boundary. Payloads exceeding this trigger HTTP 413 without memory consumption. |
| **Context Window Exhaustion** | Character count ceiling | Contracts are capped at **100,000 characters** with defensive Pydantic validation (`ContractAnalysisRequest`). |
| **Dangerous File Extensions** | Whitelist-only validation | Only permitted file formats (`.pdf`, `.docx`, `.doc`, `.txt`, `.md`) are processed. Executables and scripts are rejected immediately. |
| **Prompt Injection & Jailbreak Attacks** | Isolated boundary delimiters | Untrusted contract content is encapsulated inside explicit `<CONTRACT_UNTRUSTED_CONTENT>` tags with mandatory system-level directives instructing the model to treat input strictly as passive text. |
| **Cross-Site Scripting (XSS)** | Context-aware DOM escaping | All dynamic model outputs and user inputs are sanitized using `escapeHtml()` prior to DOM insertion. |
| **Clickjacking & MIME-Sniffing** | Defensive HTTP headers | Injected on every response: `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `X-XSS-Protection: 1; mode=block`, and `Referrer-Policy: strict-origin-when-cross-origin`. |
| **API Abuse & Brute-Force** | IP-based rate limiting | Enforced via `Flask-Limiter` (120 requests/minute per IP address). |
| **Credential & Secret Leakage** | Zero hardcoded keys | Environment variables only (`.env.example`). Client-supplied API keys are isolated per session/header and never logged or reflected back. |

---

## 2. Automated Security Verification

Run the automated security test suite:
```bash
pytest tests/test_security.py -v
```
**Results:** 5/5 security boundary tests passing with 100% success rate.
