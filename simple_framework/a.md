1. VISIBILITY & PRESENCE ASSERTIONS (UI STATE)
One-liners (Python)

expect(locator).to_be_visible()
→ Element is in DOM and visible to user

expect(locator).to_be_hidden()
→ Element is hidden or removed

expect(locator).to_be_attached()
→ Element exists in DOM (visibility not required)

expect(locator).not_to_be_attached()
→ Element not present in DOM

Interview explanation:
“Visibility checks UI rendering, attachment checks DOM presence.”

2. ENABLED / DISABLED / INTERACTION STATE
One-liners

expect(locator).to_be_enabled()
→ User can interact

expect(locator).to_be_disabled()
→ Disabled via attribute or state

expect(locator).to_be_editable()
→ Enabled and writable

Interview explanation:
“I use enabled vs editable to distinguish clickable from writable elements.”

3. CHECKBOX & RADIO ASSERTIONS
One-liners

expect(locator).to_be_checked()
→ Checkbox or radio selected

expect(locator).to_be_unchecked()
→ Checkbox or radio not selected

Interview explanation:
“These assertions validate user selection state, not attributes.”

4. TEXT ASSERTIONS (MOST COMMON)
One-liners

expect(locator).to_have_text("Login")
→ Exact text match

expect(locator).to_contain_text("Log")
→ Partial match

expect(locator).to_have_text(re.compile("Log.*"))
→ Regex-based text validation

Interview explanation:
“I use to_have_text for strict UI checks and to_contain_text for flexible content.”

5. INPUT & FORM VALUE ASSERTIONS
One-liners

expect(locator).to_have_value("admin")
→ Input value check

expect(locator).to_have_attribute("type", "email")
→ Attribute validation

Interview explanation:
“Value assertions confirm what the application stored, not what we typed.”

6. COUNT & COLLECTION ASSERTIONS
One-liners

expect(locator).to_have_count(5)
→ Exact number of matching elements

Interview explanation:
“I use count assertions for lists, tables, and dynamic search results.”

7. PAGE-LEVEL ASSERTIONS
One-liners

expect(page).to_have_url("https://example.com")
→ Exact URL match

expect(page).to_have_url(re.compile("dashboard"))
→ Regex URL match

expect(page).to_have_title("Dashboard")
→ Page title validation

Interview explanation:
“Page-level assertions confirm navigation success without manual waits.”

8. NEGATIVE ASSERTIONS (VERY IMPORTANT)
One-liners

expect(locator).not_to_be_visible()
→ Element must NOT appear

expect(locator).not_to_have_text("Error")
→ Validate absence of error state

Interview explanation:
“Negative assertions are as important as positive ones for stability.”