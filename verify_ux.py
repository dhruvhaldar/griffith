import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        # Load page from static server
        page.goto("http://localhost:8080/index.html")

        # Select the 'width' input and clear it to trigger the 'invalid' state (because it has required min="0")
        width_input = page.locator("#width")
        width_input.fill("")

        # Click outside to remove focus and active states
        page.locator("body").click()

        # Select the associated label
        width_label = page.locator("label[for='width']")

        # We need to evaluate the pseudo-element style
        pseudo_content = width_label.evaluate("el => window.getComputedStyle(el, '::before').content")
        label_color = width_label.evaluate("el => window.getComputedStyle(el).color")

        # Take a screenshot
        page.screenshot(path="verification_error_state.png")
        print("Screenshot saved to verification_error_state.png")

        print(f"Computed pseudo content: {pseudo_content}")
        print(f"Computed label color: {label_color}")

        # Assertions
        assert "⚠️" in pseudo_content, "The pseudo element should contain the warning icon"

        print("All validations passed!")

        context.close()
        browser.close()

if __name__ == "__main__":
    run()
