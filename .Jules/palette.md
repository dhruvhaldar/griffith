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

## 2026-03-10 - Native Validation for Arbitrary Precision
**Learning:** Setting specific `step` values (like `0.01`) on `<input type="number">` fields for continuous physical/scientific variables causes native HTML5 validation errors when users enter valid floats with higher precision.
**Action:** Always use `step="any"` on `<input type="number">`, allowing arbitrary precision for physical inputs and preventing frustrating native validation errors on valid entries.

## 2026-03-11 - Landmark Regions Accessibility
**Learning:** Using generic `<section>` tags for major, distinct parts of an application (like multiple interactive calculators on a single page) is insufficient for screen reader users. Without names, these regions are less helpful or completely ignored in the landmark/rotor menus, making navigation significantly slower and harder.
**Action:** Always add explicit names to significant `<section>` or `<form>` elements by using `aria-labelledby` pointing to their respective heading IDs. This transforms them into named Landmark Regions, drastically improving programmatic navigation for assistive technologies.

## 2026-03-12 - Contextual Disabled State Tooltips
**Learning:** Disabling interactive elements like buttons dynamically (e.g., due to stale data) prevents errors, but without explaining *why* it's disabled, users are left confused. Also, decorative emojis inside interactive elements must be hidden from screen readers using `aria-hidden="true"`.
**Action:** Always update the `title` and `aria-label` to provide contextual explanations for dynamically disabled states, improving both visual UX and screen reader accessibility. Wrap decorative emojis in `<span aria-hidden="true">`.
## 2026-03-13 - Native Spin Buttons on Scientific Inputs
**Learning:** Browsers add native increment/decrement "spin buttons" to `<input type="number">` fields. For engineering/scientific applications where values are extremely large (e.g., `200000000` Pa) or extremely small (e.g., `1.5e-11`), the default step size (often `1` or what's defined in the `step` attribute) is completely useless. Worse, accidentally clicking the spin button can destroy precisely entered scientific notation or arbitrary values, causing immense user frustration. They also add visual clutter.
**Action:** Always hide native spin buttons (`::-webkit-inner-spin-button`, `-moz-appearance: textfield`) on numerical inputs designed for high-precision or wide-ranging scientific values to prevent accidental data destruction and clean up the UI.

## 2026-03-14 - iOS Safari Input Zoom and Disabled State Cursors
**Learning:** iOS Safari will automatically zoom the page when an input is focused if its font size is less than 16px. Also, due to CSS specificity, `button:disabled` (which often sets `cursor: not-allowed`) will override the `cursor: wait` set on `button.loading`, leading to confusing UX where a loading button looks non-interactive.
**Action:** Always set `font-size: 16px` (or `1rem` assuming a 16px base size) on `input` and `select` elements to prevent unwanted zooming on iOS. Additionally, explicitly add a `button.loading:disabled { cursor: wait; }` rule to ensure loading state cursors correctly override standard disabled state cursors.
## 2024-03-05 - Visual Framing for Custom Input Wrappers
**Learning:** When inputs are wrapped with additional helper elements (like the dynamic unit formatter), highlighting only the top label on focus leaves the component feeling disjointed. Highlighting both the label and the helper text synchronously creates a cohesive "visual frame" around the focused element.
**Action:** When implementing complex input wrappers with auxiliary text, use `:has(> input:focus)` to apply the primary brand color to all associated textual elements, framing the interaction context.

## 2026-03-18 - Dynamic ARIA Labels on Live Canvas Elements
**Learning:** Setting a static `aria-label` on `<canvas role="img">` elements is insufficient when the canvas updates visually based on user input. Screen reader users miss critical context changes (like updated dimensions) that sighted users see instantly.
**Action:** When using JavaScript functions to draw or update canvas elements based on inputs, always dynamically update the `canvas.setAttribute('aria-label', ...)` to reflect the new state or geometry.

## 2026-03-17 - Respecting Reduced Motion Preferences
**Learning:** Animations and transitions (like the result fade-in, copy tooltip slide, and loading spinners) can cause dizziness or nausea for users with vestibular disorders. While these micro-interactions add polish for some, they create an inaccessible experience for others who have explicitly opted out via OS-level settings.
**Action:** Always include a `@media (prefers-reduced-motion: reduce)` block at the end of stylesheets to globally set animation and transition durations to practically zero (`0.01ms`), ensuring a safer, accessible experience without breaking JS event listeners that depend on transition ends.

## 2026-03-19 - Plotly Chart Responsiveness
**Learning:** Plotly charts rendered without the `{ responsive: true }` configuration option do not automatically resize when the browser window changes dimensions or a mobile device is rotated, which can lead to clipped visualizations and a broken layout.
**Action:** When rendering Plotly charts in responsive layouts, always include `{ responsive: true }` in the configuration object of `Plotly.newPlot()` to ensure the chart scales correctly.

## 2026-03-23 - Destructive Native Keybindings on Scientific Inputs
**Learning:** Browsers bind the `ArrowUp` and `ArrowDown` keys to increment/decrement `<input type="number">` fields. For engineering/scientific applications where values are extremely large (e.g., `200000000` Pa) or extremely small (e.g., `1.5e-11`), a user accidentally pressing an arrow key when the input is focused can instantly destroy their high-precision values by aggressively rounding or incrementing them to standard units (like `1`). This is particularly destructive for scientific notation input.
**Action:** Always add a global or input-specific `keydown` listener that checks if `document.activeElement.type === 'number'` and calls `event.preventDefault()` for `ArrowUp` and `ArrowDown`, ensuring high-precision data is not accidentally wiped out by basic keyboard navigation.

## 2026-03-25 - Mobile Keyboard Optimization for Technical Inputs
**Learning:** Native `<input type="number">` fields often trigger less-than-ideal keyboards on mobile devices (e.g., standard keyboards with a number row, or keyboards lacking a decimal point), and browsers aggressively try to autofill engineering numbers with saved phone numbers or ZIP codes, cluttering the UI.
**Action:** Always dynamically apply `inputmode="decimal"`, `autocomplete="off"`, and `spellcheck="false"` to all `<input type="number">` fields in engineering/scientific calculators. This forces mobile devices to present the optimal pure-numeric keypad and prevents distracting browser autofill popups on high-precision numerical inputs.

## 2026-03-26 - Reliable WCAG 2.5.5 Minimum Touch Targets
**Learning:** Native form inputs, select elements, buttons, and particularly small icon-only utility buttons often do not meet the WCAG 2.5.5 minimum touch target size of 44x44px due to default browser styling or insufficient padding. This creates a frustrating "fat finger" experience on mobile devices and reduces accessibility for users with motor impairments. Relying solely on `padding` is risky as it depends on font-size and line-height.
**Action:** Always enforce accessible touch targets by adding `min-height: 44px` and `box-sizing: border-box` to global `input`, `select`, and `button` CSS rules. For icon-only buttons (like a copy icon), explicitly set both `min-width: 44px` and `min-height: 44px` to ensure a reliable square hit area regardless of the internal content size.

## 2026-03-27 - Contextual Warning for Visually Dimmed Stale States
**Learning:** While dimming results prevents copying "stale" data, users (both sighted and screen reader) may be confused about *why* the content is dimmed or disabled without explicit context. Visual dimming is completely hidden from assistive technologies.
**Action:** When applying a "stale" visual state, always add an explicit `title` attribute for mouse-hover tooltips, and dynamically inject an `.sr-only` warning span containing text like "Warning: Inputs have changed. Please recalculate" so that screen readers announce the context change explicitly.

## 2026-03-28 - Focus Management for Async Results
**Learning:** For asynchronous calculators on mobile devices, when users submit a form, the virtual keyboard remains open and obscures the result displayed lower on the page, forcing users to manually dismiss the keyboard. Screen readers also may not instantly navigate to the dynamically inserted content.
**Action:** Whenever an asynchronous result or error is successfully displayed in a dynamic container (like `#result`), explicitly add `tabindex="-1"` and programmatically focus the container (`element.focus()`). This action naturally dismisses the mobile virtual keyboard, natively scrolls the new result into the viewport, and directly aids screen readers in finding the new content, significantly improving the end-to-end user experience.
