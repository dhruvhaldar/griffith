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

## 2026-03-05 - Enhanced Copy Feedback & Mobile Responsiveness
**Learning:** Simple icon changes (📋 -> ✅) for copy actions lack persistence and clear accessibility context. Adding a transient tooltip ("Copied!") provides unmistakable confirmation for visual users, while updating `aria-label` ensures screen reader users are informed. Additionally, unconstrained `canvas` elements cause horizontal overflow on mobile devices, breaking the layout.
**Action:** Implement a `showCopyFeedback` pattern with a positioned tooltip and transient `aria-label` update for copy actions. Always ensure `canvas` elements have `max-width: 100%; height: auto;` to maintain responsiveness.

## 2026-03-05 - Scientific Notation Usability
**Learning:** Users struggle with entering large physical constants (like 200 GPa) into numeric inputs, often leading to order-of-magnitude errors. A live, client-side formatter that displays the human-readable metric equivalent (e.g., "200 GPa") below the input significantly reduces cognitive load and errors.
**Action:** Implement a `LiveUnitFormatter` pattern for any scientific/engineering inputs that automatically parses and displays metric prefixes based on the label's unit.

## 2026-03-05 - Client-Side Logical Validation
**Learning:** Native form validation handles data types and ranges, but misses logical constraints between fields (e.g., crack length > plate width). This leads to frustrating server errors.
**Action:** Implement `setCustomValidity` with descriptive messages on `input` events to enforce logical constraints client-side, ensuring users see helpful errors before submission.

## 2026-03-05 - Visual Required Indicators & Dynamic DOM
**Learning:** Native HTML `required` attributes exist but lack visual indicators (like asterisks), causing friction before submission. Because client-side scripts (like `LiveUnitFormatter`) dynamically wrap inputs in `.input-wrapper` divs, traditional adjacent sibling selectors (`label + input`) break.
**Action:** Use the CSS `:has()` pseudo-class (`label:has(+ input[required]), label:has(+ .input-wrapper > input[required])`) to create robust visual indicators that survive dynamic DOM manipulation.

## 2026-03-05 - Color Contrast Failures in Default Colors
**Learning:** Default CSS colors for success states (like `#27ae60` green) and empty states (like `#7f8c8d` gray) often fail WCAG AA minimum contrast ratios (4.5:1) when placed on light backgrounds (e.g., `#ffffff` or `#f8f9fa`), making text unreadable for visually impaired users.
**Action:** Always test foreground/background combinations using a contrast checker script or tool, and select darker shades (like `#1e8449` or `#546e7a`) to meet accessibility standards.

## 2026-03-05 - Missing Cursor Affordance on Labels
**Learning:** Native `<label>` elements focus their associated inputs when clicked, but lack visual indicators for this interactivity. Users may not realize they can click the label text, especially on complex or lengthy forms. Adding a `cursor: pointer;` provides a clear visual cue for this affordance, improving usability and reducing perceived friction.
**Action:** Always add `cursor: pointer;` to `<label>` elements in CSS to visually communicate their interactive nature to users.
