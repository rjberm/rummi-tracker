from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # 1. Verify index.html button
        print("Navigating to index.html...")
        page.goto("http://localhost:8080/index.html")

        # Check if Mexican Train section is hidden (it should be initially)
        # We need to select "Mexican Train" from the dropdown to reveal it.
        # Dropdown ID: gameSelector
        # Option value: mexican_train

        print("Selecting Mexican Train...")
        try:
            page.select_option("#gameSelector", "mexican_train")

            # Wait for the tracker to appear
            # The class 'hidden' is removed.
            # page.wait_for_selector("#mexicanTrainTracker:not(.hidden)", state="visible")
            # Simplified wait
            page.wait_for_timeout(1000)

            # Check for the button
            # The button text is "📺 Open Live Board"
            button = page.get_by_text("📺 Open Live Board")
            if button.is_visible():
                print("SUCCESS: Live Board button is visible in index.html")
            else:
                print("FAILURE: Live Board button not found or not visible.")
        except Exception as e:
            print(f"Index.html interaction failed: {e}")

        # 2. Verify live.html
        print("Navigating to live.html...")
        page.goto("http://localhost:8080/live.html")

        # Wait a bit for JS to run (init firebase, etc)
        page.wait_for_timeout(5000)

        # Take screenshot
        print("Taking screenshot of live.html...")
        page.screenshot(path="live_preview.png")

        browser.close()

if __name__ == "__main__":
    run()
