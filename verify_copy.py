import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # Scenario 1: Mobile View (375x667)
        context = browser.new_context(viewport={"width": 375, "height": 667})
        context.grant_permissions(["clipboard-read", "clipboard-write"])
        page = context.new_page()

        # Mock API
        def handle_api(route):
            print(f"Intercepted: {route.request.url}")
            if "calculate-sif" in route.request.url:
                route.fulfill(status=200, json={"k1": 12345678.9})
            else:
                route.continue_()

        page.route("**/api/calculate-sif", handle_api)

        # Load page from static server
        page.goto("http://localhost:8080/index.html")

        # Scroll to SIF calculator
        sif_section = page.locator("#sif-calculator")
        sif_section.scroll_into_view_if_needed()

        # Click Calculate
        # Wait for button to be clickable
        calc_btn = sif_section.locator("button[type=submit]")
        calc_btn.click()

        # Wait for result
        result_container = page.locator("#sif-result .result-container")
        result_container.wait_for(state="visible")

        # Click Copy
        copy_btn = result_container.locator(".copy-btn")
        copy_btn.click()

        # Wait for tooltip
        tooltip = result_container.locator(".copy-tooltip.show")
        tooltip.wait_for(state="visible")

        # Take screenshot
        page.screenshot(path="verification_copy_mobile.png")
        print("Screenshot saved to verification_copy_mobile.png")

        # Verify Aria Label
        assert copy_btn.get_attribute("aria-label") == "Copied!"
        print("Aria label verified: Copied!")

        # Verify Content
        assert "✅" in copy_btn.inner_text()
        print("Button content verified: ✅")

        context.close()
        browser.close()

if __name__ == "__main__":
    run()
