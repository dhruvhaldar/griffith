from playwright.sync_api import sync_playwright
import time

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(record_video_dir=".")
        page = context.new_page()

        # Mock the API route directly in Playwright!
        def handle_api(route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body='{"k1": 15000000, "unit": "Pa*sqrt(m)"}'
            )

        page.route("**/api/calculate-sif", handle_api)

        # Load page from static server
        page.goto("http://localhost:8080/index.html")
        page.wait_for_timeout(500)

        # 1. Fill input to start
        page.locator("#width").fill("0.2")
        page.locator("#crack-length").fill("0.02")
        page.locator("#stress").fill("200000000")

        # 2. Click the button inside the #sif-calculator form
        submit_btn = page.locator("#sif-calculator form button[type='submit']")
        submit_btn.click()
        page.wait_for_timeout(2000)

        # 3. Take screenshot of result
        page.screenshot(path="verification_result.png")

        # 4. Modify an input to trigger the stale state
        page.locator("#crack-length").fill("0.05")
        page.wait_for_timeout(1000)

        # 5. Take screenshot of the pulsing button
        page.screenshot(path="verification_pulse_state.png")

        # 6. Verify the classes and aria-labels
        class_list = submit_btn.evaluate("el => el.className")
        aria_label = submit_btn.evaluate("el => el.getAttribute('aria-label')")

        print(f"Button classes: {class_list}")
        print(f"Button aria-label: {aria_label}")

        assert "needs-recalc" in class_list, "Button should have 'needs-recalc' class"
        assert aria_label == "Recalculate (inputs modified)", "Button should have updated aria-label"

        # 7. Click calculate again to verify the state clears
        submit_btn.click()
        page.wait_for_timeout(2000)

        class_list_after = submit_btn.evaluate("el => el.className")
        aria_label_after = submit_btn.evaluate("el => el.getAttribute('aria-label')")

        print(f"Button classes after click: {class_list_after}")
        print(f"Button aria-label after click: {aria_label_after}")

        assert "needs-recalc" not in class_list_after, "Button should not have 'needs-recalc' class after click"
        assert aria_label_after is None, "Button should not have aria-label after click"

        print("All validations passed!")

        context.close()
        browser.close()

if __name__ == "__main__":
    run()
