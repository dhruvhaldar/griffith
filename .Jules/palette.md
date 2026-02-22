## 2026-02-17 - Missing Input Validation
**Learning:** Numeric inputs in the calculator lacked `min="0"` and `required` attributes, allowing negative values which are physically nonsensical for crack lengths.
**Action:** Always verify `min` and `required` attributes for numeric inputs in this codebase.

## 2026-02-18 - Inconsistent Error Feedback
**Learning:** Error messages were rendered as plain text in success colors, confusing users. Using `innerHTML` for icons introduced XSS risks.
**Action:** Use a standardized `showError(element, message)` helper that safely appends text nodes and icons to ensure consistency and security.

## 2026-02-25 - Native Validation & Accessibility
**Learning:** While `required` and `min` attributes existed, they weren't enforced by JS logic, leading to "rage clicks" and server errors. Enabling `reportValidity()` provides immediate, accessible feedback. Also, `role="alert"` ensures screen readers announce errors immediately, while `aria-live="polite"` handles results.
**Action:** Use `checkValidity()` and `reportValidity()` in frontend logic to enforce HTML constraints before API calls. Use `role="alert"` for transient errors.

## 2026-02-26 - Responsive Form Layouts
**Learning:** The `grid-template-columns: 1fr 1fr` layout pattern used for form inputs breaks on mobile viewports (< 600px), causing label truncation and poor usability.
**Action:** Always include a `@media` query to stack `.input-group` elements vertically for mobile support in `style.css`.

## 2026-03-04 - Result Copy Button Pattern
**Learning:** Users often need to copy calculation results. Implementing a reusable `showResult(element, text)` helper that appends a copy button (📋) next to the result text significantly improves usability without cluttering the UI. Using `navigator.clipboard.writeText` with visual feedback (✅) provides immediate confirmation.
**Action:** Use the `showResult` pattern for any new calculation outputs to maintain consistency and provide copy functionality by default. Ensure container has `min-height` to prevent layout shift during updates.
