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

## 2026-03-06 - Live Visual Feedback and Canvas Accessibility
**Learning:** When users edit physical dimensions (like width or crack length), waiting for form submission to update the visual representation breaks the connection between input and physical reality. Also, a `<canvas>` element used for rendering must explicitly include `role="img"` along with `aria-label` to be announced properly by screen readers. Hooking visual updates to the "input" event (as part of client-side validation) provides instant feedback, significantly improving the mental mapping of numbers to geometry.
**Action:** Always hook visual representations (like charts or diagrams) to update in real-time as users modify the associated input fields, and ensure explicit semantic roles like `role="img"` are added to `<canvas>` tags.

## 2026-03-06 - Stale State Prevention in Calculators
**Learning:** In interactive calculators, when a user modifies an input *after* a successful calculation, the previously rendered results (and plots) remain visible but are now mismatched with the current input values. This "stale" state can lead to users accidentally copying or misinterpreting incorrect data.
**Action:** Implement a "Stale State Pattern" by listening to `input` events on forms and visually dimming (e.g., `opacity: 0.6`, `grayscale(100%)`) the existing result containers and plots. Additionally, explicitly disable any copy functionalities in this state to prevent errors. Clear the stale state only when a new calculation completes successfully.

## 2026-03-06 - Explicit Keyboard Shortcut Affordance
**Learning:** The 'Enter to Submit' pattern is fully functional via wrapping inputs in `<form>` and using `onsubmit`, but users lack visual affordance of this shortcut, forcing unnecessary trackpad/mouse movement to click the primary button repeatedly.
**Action:** Always provide explicit, visual `<kbd>` hints on primary submit actions in forms to encourage fast, keyboard-driven workflows.

## 2026-03-06 - Select-on-Focus for Prefilled Inputs
**Learning:** In technical calculators where fields are heavily pre-filled with reasonable defaults (like initial crack lengths or remote stress values), users clicking into a field usually intend to entirely overwrite the existing value. Without auto-selecting the content, users are forced to manually highlight or backspace the existing value character-by-character, creating significant friction.
**Action:** Implement a Select-on-Focus pattern (`input.addEventListener('focus', function() { this.select(); })`) for pre-filled numerical inputs so users can instantly overwrite them upon focus, streamlining data entry.

## 2026-03-07 - Skip-Link Target Accessibility
**Learning:** Adding a "Skip to main content" link is useless if the target element (like `<main>`) cannot programmatically receive focus. Without `tabindex="-1"`, clicking the skip link visually scrolls the page, but the very next tab press will jump focus right back to the top of the page (e.g., to the header). Additionally, giving `<main>` focus natively triggers an unsightly focus ring that confuses sighted users.
**Action:** Always add `tabindex="-1"` to the target element of skip links to enable programmatic focus without making it part of the normal tab sequence. Always pair this with `#target:focus { outline: none; }` in CSS to hide the focus ring.

## 2026-03-07 - Active Label Highlight Pattern
**Learning:** Native browser forms provide visual affordance for the active input (focus rings), but the user's eye often needs to refer back to the label while typing. Visually connecting the active field to its label by changing the label's text color (using the primary brand color) significantly reduces cognitive load and improves form completion speed.
**Action:** Use the CSS `:has()` pseudo-class (e.g., `label:has(+ input:focus), label:has(+ .input-wrapper > input:focus) { color: var(--primary); }`) to elegantly highlight labels when their associated inputs are focused, supporting both direct siblings and dynamically wrapped inputs.

## 2026-03-09 - Missing CSS Styles for JS-Toggled State Classes
**Learning:** Adding CSS classes via JS (like `copyBtn.classList.add('copied')`) is ineffective if the corresponding CSS rules are missing. This results in missing visual affordances for success states, reducing clarity for the user even when text changes to an icon like "✅".
**Action:** Always verify that CSS state classes dynamically toggled in JavaScript (e.g., `.copied`, `.success`, `.error`) have corresponding styles defined in the CSS files to provide full visual feedback.
\n## 2026-03-10 - Native Validation for Arbitrary Precision
**Learning:** Setting specific `step` values (like `0.01`) on `<input type="number">` fields for continuous physical/scientific variables causes native HTML5 validation errors when users enter valid floats with higher precision.
**Action:** Always use `step="any"` on `<input type="number">`, allowing arbitrary precision for physical inputs and preventing frustrating native validation errors on valid entries.
