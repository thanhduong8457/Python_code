import time
import pandas as pd
from playwright.sync_api import sync_playwright

def scrape_mac_tiktok():
    print("--- STARTING MAC SCRAPER ---")
    
    with sync_playwright() as p:
        # 1. Connect to the Chrome window you opened via Terminal
        try:
            browser = p.chromium.connect_over_cdp("http://localhost:9222")
        except Exception as e:
            print("❌ ERROR: Could not connect to Chrome.")
            print("Make sure you ran the long command in Terminal and Chrome is open.")
            print(f"Details: {e}")
            return

        # Get the active tab
        context = browser.contexts[0]
        if not context.pages:
            page = context.new_page()
        else:
            page = context.pages[0]

        print("✅ Connected to Chrome.")
        print("Please ensure the browser is on your TikTok Profile page.")
        print("⏳ Scrolling to load videos (Running for 15 seconds)...")

        # 2. Scroll down to load older videos
        # Adjust range(15) to a higher number if you have hundreds of videos
        for _ in range(15): 
            page.mouse.wheel(0, 5000)
            time.sleep(1.5) # Wait for videos to load

        print("👀 Reading video data...")

        # 3. Extract Data
        # We look for the specific container that holds video stats
        video_elements = page.locator('div[data-e2e="user-post-item"]')
        count = video_elements.count()
        
        print(f"Found {count} videos.")
        
        results = []

        for i in range(count):
            try:
                element = video_elements.nth(i)
                
                # Get View Count
                # Note: TikTok changes selectors often. 
                # We try the standard 'strong' tag used for views.
                views = element.locator('strong[data-e2e="video-views"]').inner_text()
                
                # Get Link
                link = element.locator('a').get_attribute('href')
                
                # Get Description (Alt text of the video cover)
                desc = "N/A"
                try:
                    desc = element.locator('img').get_attribute('alt')
                except:
                    pass

                results.append({
                    "Title": desc,
                    "Views": views,
                    "URL": link
                })
                
            except Exception as e:
                continue

        # 4. Save to CSV
        if results:
            df = pd.DataFrame(results)
            # Save to your Desktop
            df.to_csv('~/Desktop/tiktok_data.csv', index=False)
            print(f"🎉 Success! Saved {len(results)} videos to Desktop/tiktok_data.csv")
        else:
            print("⚠️ No videos found. TikTok might have changed their HTML layout.")

        # Disconnect cleanly (Keep browser open)
        browser.close()

if __name__ == "__main__":
    scrape_mac_tiktok()