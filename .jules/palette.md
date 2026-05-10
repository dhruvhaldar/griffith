## 2024-05-24 - Naming Forms for Explicit Landmark Regions
**Learning:** Adding an `aria-labelledby` attribute to a `<form>` tag that points to the ID of its respective heading element explicitly names the form, transforming it into a recognizable Landmark Region. This vastly improves screen reader navigation and accessibility within the application.
**Action:** When creating forms, especially in major interactive application parts wrapped in `<section>` or `<form>` tags, always ensure they use `aria-labelledby` pointing to their respective heading ID to explicitly name them as Landmark Regions.

## 2024-10-25 - Accessible Form Error States via CSS :has()
**Learning:** Validations states can be automatically propagated to their associated `<label>` tags purely using CSS. By using the `:has()` selector on the `<label>`, when an adjacent input becomes `:invalid`, the label itself can reflect this state without needing any JavaScript to toggle classes. This ensures immediate feedback for users filling out required fields, maintaining accessible and robust client-side validation natively.
**Action:** When setting up `<form>` tags containing `<input>` elements that have validation constraints (like `required`, `min`, `max`), utilize the `label:has(+ input:invalid)` CSS rule to easily and reliably style labels to display error states (e.g. changing color or injecting warning icons).## 2024-04-10 - Reverting Document Title on Stale State\n**Learning:** While updating `document.title` to show calculation results provides great context, forgetting to revert it when the data becomes stale leads to confusing tab titles that display outdated information.\n**Action:** When using a Stale State pattern that invalidates the UI, always remember to revert contextual elements like `document.title` back to their base or default state to avoid misleading users.

## 2024-04-11 - Disabling Form Inputs During Async Calculations
**Learning:** While disabling the submit button during an async calculation prevents double-submissions, leaving the input fields active allows users to modify values while the request is pending. If the request completes and renders the result, it will appear to correspond to the *new* input values, creating a confusing race condition.
**Action:** Always disable the entire form (all `input` and `select` elements) during an asynchronous calculation, and add appropriate visual styling (`opacity`, `cursor: not-allowed`, `background-color`) to clearly communicate that the form is temporarily locked.

## 2026-04-12 - Accessible Transient Feedback
**Learning:** Changing `aria-label` on a focused element often fails to trigger a screen reader announcement. For transient actions like copying, an explicit `aria-live` region is necessary.
**Action:** Implement a global `a11y-announcer` live region and dynamically update its text to provide reliable feedback for transient interactions.

## 2024-10-26 - Accessible Form Disabled States via CSS :has()
**Learning:** When form inputs are disabled (e.g., during async operations), leaving the associated `<label>` fully styled creates a disjointed user experience where the label appears active but the input is locked. We can propagate the `disabled` state to the `<label>` purely using CSS via the `:has()` selector (e.g., `label:has(+ input:disabled)`), allowing the label to visually dim alongside the input.
**Action:** When setting up `<form>` inputs that can be dynamically disabled, utilize the `label:has(+ input:disabled)` CSS rule to easily and reliably style labels to display their locked state (e.g. reducing opacity and setting cursor to not-allowed).

## 2024-10-27 - Double-Announcement via Focus + aria-live
**Learning:** If an element is dynamically focused (e.g., using `element.focus()` with `tabindex="-1"`) after an asynchronous operation, screen readers will automatically read its contents because of the focus event. Adding `aria-live="polite"` to that same container causes the screen reader to announce it twice—once for the live region update, and once for the focus—resulting in confusing, stuttering verbosity.
**Action:** When programmatically moving focus to a result container for accessibility, do not put `aria-live` on that container. Rely solely on the focus event to trigger the reading.
## 2024-04-16 - Dismissing Mobile Virtual Keyboard on Form Submission
**Learning:** When users submit a form on mobile web applications, the virtual keyboard remains active and covers the bottom of the screen, potentially obscuring dynamic success/error messages injected into the DOM. This is a poor user experience.
**Action:** When rendering dynamic asynchronous results after a form submission, proactively dismiss the virtual keyboard and scroll the response into view by setting `tabindex="-1"` on the result container and calling `.focus()` on it in JS. Prevent the native focus ring by adding `.result-container:focus { outline: none; }` in CSS. This explicitly redirects focus away from inputs.

## 2024-10-28 - Acknowledging Correction Attempts by Clearing Error States
**Learning:** When a user receives a form error and subsequently begins to modify an input, continuing to display the error state (e.g. red borders, error messages) feels punitive and broken. The user is actively trying to correct the issue, and the UI should immediately acknowledge this by reverting to a neutral or "needs recalculation" state.
**Action:** When implementing input modification listeners (like Stale State handlers), always check for and clear any global error messages, restoring the container to a neutral/empty state as soon as the user begins typing.

## 2024-05-25 - Stable Numerical Displays with Tabular Nums
**Learning:** When displaying dynamic numbers or calculated results, proportional fonts cause the text width to jitter horizontally as values change (e.g., '1' is narrower than '8'). This is especially noticeable in interactive calculators and live inputs.
**Action:** Apply `font-variant-numeric: tabular-nums;` to inputs, result containers, and data tables to force monospaced digit widths within proportional fonts, ensuring a stable and polished visual experience without layout shifts.

## 2026-05-04 - Maintaining role='alert' for Dynamic Errors
**Learning:** When displaying dynamically injected error messages, the `role="alert"` attribute is critical for screen readers to immediately announce the error. Removing this attribute, even if the element is programmatically focused, degrades accessibility by preventing the necessary assertive announcement.
**Action:** Always retain `role="alert"` on containers that dynamically display error messages to ensure proper screen reader notification.

## 2024-05-26 - Dismissing Mobile Virtual Keyboard on Form Submission
**Learning:** When users submit a form on mobile web applications, the virtual keyboard remains active and covers the bottom of the screen, potentially obscuring dynamic success/error messages injected into the DOM. This is a poor user experience.
**Action:** When rendering dynamic asynchronous results after a form submission, proactively dismiss the virtual keyboard and scroll the response into view by setting `tabindex="-1"` on the result container and calling `.focus()` on it in JS. Prevent the native focus ring by adding `.result-container:focus { outline: none; }` in CSS. This explicitly redirects focus away from inputs.

## 2024-10-29 - Preventing Misleading Hover States on Disabled Elements
**Learning:** When interactive elements like buttons are temporarily disabled (e.g., during asynchronous operations), applying standard `:hover` state styles (like background color changes) provides users with a false affordance of interactivity. This is misleading and creates a disjointed experience when the element is actually locked.
**Action:** Always append the `:not(:disabled)` pseudo-class to `:hover` selectors for interactive elements (e.g., `button:hover:not(:disabled)`) to ensure visual hover feedback is strictly reserved for actionable states.
