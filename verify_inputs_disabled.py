from playwright.sync_api import sync_playwright
import time

def run_cuj(page):
    page.goto("http://localhost:8080/index.html")
    page.wait_for_timeout(500)

    # Find the geometry select input (should be enabled initially)
    width_input = page.locator("#width")
    assert width_input.is_enabled()

    # Find the submit button
    sif_btn = page.locator("#sif-calculator button[type=submit]")

    # Fill out form to ensure we have a valid request
    width_input.fill("0.1")
    page.wait_for_timeout(500)

    # Click calculate. This will disable the inputs.
    sif_btn.click()

    # Wait for the interceptor to complete
    page.wait_for_timeout(2000)

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            record_video_dir="/home/jules/verification/videos"
        )

        # Intercept route to delay response and take a screenshot of the disabled state
        def handle_route(route):
            print(f"Intercepted: {route.request.url}")
            page = route.request.frame.page
            time.sleep(1) # sleep to let UI update
            page.screenshot(path="/home/jules/verification/screenshots/verification.png")
            route.continue_()

        page = context.new_page()
        page.route("**/api/calculate-sif", handle_route)

        try:
            run_cuj(page)
        finally:
            context.close()
            browser.close()