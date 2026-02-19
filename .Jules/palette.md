## 2026-02-17 - Missing Input Validation
**Learning:** Numeric inputs in the calculator lacked `min="0"` and `required` attributes, allowing negative values which are physically nonsensical for crack lengths.
**Action:** Always verify `min` and `required` attributes for numeric inputs in this codebase.

## 2026-02-18 - Inconsistent Error Feedback
**Learning:** Error messages were rendered as plain text in success colors, confusing users. Using `innerHTML` for icons introduced XSS risks.
**Action:** Use a standardized `showError(element, message)` helper that safely appends text nodes and icons to ensure consistency and security.

## 2026-02-25 - Native Validation & Accessibility
**Learning:** While `required` and `min` attributes existed, they weren't enforced by JS logic, leading to "rage clicks" and server errors. Enabling `reportValidity()` provides immediate, accessible feedback. Also, `role="alert"` ensures screen readers announce errors immediately, while `aria-live="polite"` handles results.
**Action:** Use `checkValidity()` and `reportValidity()` in frontend logic to enforce HTML constraints before API calls. Use `role="alert"` for transient errors.
