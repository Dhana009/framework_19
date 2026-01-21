# Playwright Python - Locators & Assertions Guide

## 1. Accessibility Roles (HTML → ARIA Mapping)

### What is it?
Playwright maps HTML semantics to ARIA roles. These are the most stable, user-centric locators.

### HTML Element to Accessibility Role Mapping

| HTML Element | Accessibility Role |
|---|---|
| `<button>` | `button` |
| `<input type="text">`, `<textarea>` | `textbox` |
| `<input type="radio">` | `radio` |
| `<input type="checkbox">` | `checkbox` |
| `<select>` | `combobox` |
| `<option>` | `option` |
| `<a>` | `link` |
| `<img>` | `img` |
| `<ul>` / `<ol>` | `list` |
| `<li>` | `listitem` |
| `<table>` | `table` |
| `<tr>` | `row` |
| `<td>` | `cell` |
| `<th>` | `columnheader` / `rowheader` |
| `<h1>–<h6>` | `heading` |
| `<form>` | `form` |

### Interview Line
> "Playwright's `get_by_role()` works on accessibility roles, not just DOM tags, which reduces locator brittleness."

---

## 2. Playwright Locators (Python)

### What is it?
Locators are lazy, strict, and auto-waiting objects that find elements on the page.

### Locator Types (In Order of Preference)

```python
# 1. BEST: Accessibility-based (most stable)
page.get_by_role("button", name="Login")           # Semantic
page.get_by_label("Email")                          # Form labels
page.get_by_text("Welcome")                         # Visible text
page.get_by_placeholder("Enter email")             # Placeholder text
page.get_by_test_id("submit-btn")                  # data-testid attribute

# 2. FALLBACK: CSS or XPath (less stable)
page.locator("button.primary")                      # CSS selector
page.locator("xpath=//button[@id='submit']")       # XPath
```

### Interview Line
> "I always prefer role or label locators before XPath because they're based on actual semantics, not implementation details."

---

## 3. XPath Locators (When Required)

### What is it?
XPath is DOM traversal - powerful but fragile. Use only when semantic locators aren't available.

### Critical XPath Patterns

```python
# Basic patterns
//button                                            # Relative XPath
//button[text()='Login']                           # Exact text
//button[contains(text(),'Log')]                   # Partial text
//button[normalize-space(text())='Login']          # Whitespace safe

# Attributes
//input[@id='email']                               # Exact attribute
//input[starts-with(@id,'user')]                  # Starts with

# Multiple conditions
//input[@type='text' and @name='email']           # AND operator
//input[@type='text' or @type='password']         # OR operator

# Navigation
..                                                 # Parent
ancestor::div                                     # Any ancestor
following-sibling::span                           # Following sibling
preceding-sibling::label                          # Preceding sibling
```

### Interview Line
> "I use XPath only when semantic locators aren't available, because XPath breaks easily with DOM changes."

---

## 4. User Actions (Interactions)

### What is it?
Actions simulate real user behavior with built-in waiting. No manual `sleep()` needed.

### Common Actions

```python
page.goto(url)                                     # Navigate
locator.click()                                    # Click
locator.fill(value)                               # Clear + type
locator.type(value)                               # Append text
locator.clear()                                    # Clear field
locator.check()                                    # Check checkbox/radio
locator.uncheck()                                  # Uncheck
locator.hover()                                    # Hover over
locator.press("Enter")                            # Press key
locator.select_option("value")                    # Select dropdown
page.wait_for_url("https://example.com")          # Wait for URL
page.wait_for_load_state("networkidle")           # Wait for page load
```

### Interview Line
> "Playwright auto-waits before every action, so explicit sleeps are unnecessary and make tests flaky."

---

## 5. Text & Value Extraction

### What is it?
These APIs read actual rendered state for assertions and debugging.

### Extraction Methods

```python
locator.inner_text()                              # Visible text only
locator.text_content()                            # Raw DOM text
locator.input_value()                             # Input field value
locator.get_attribute("href")                     # Attribute value
page.title()                                      # Page title
page.url                                          # Current URL
```

### Interview Line
> "I use `inner_text()` for UI validation and `text_content()` for DOM checks."

---

## 6. Event Handling (Windows, Tabs, Alerts)

### What is it?
Playwright is event-driven, not delay-driven. Handle popups and new tabs correctly.

### New Tab / Window

```python
with page.context.expect_page() as new_page:
    page.get_by_role("button", name="Open").click()

new_page = new_page.value
new_page.wait_for_load_state()
```

### Alert / Confirm Dialogs

```python
def handle_dialog(dialog):
    print(f"Dialog message: {dialog.message}")
    dialog.accept()  # or dialog.dismiss()

page.on("dialog", handle_dialog)  # Register BEFORE triggering
page.get_by_role("button", name="Alert").click()
```

### Interview Line
> "I always register the event listener BEFORE triggering the action to avoid race conditions."

---

## 7. Assertions (expect - Python)

### What is it?
Assertions are **auto-retrying smart waits**. They retry until the condition passes or timeout occurs. This is why Playwright tests are stable without `sleep()`.

### 7.1 Visibility & Presence Assertions

```python
expect(locator).to_be_visible()                   # In DOM and visible
expect(locator).to_be_hidden()                    # Hidden or removed
expect(locator).to_be_attached()                  # Exists in DOM
expect(locator).not_to_be_attached()              # Not in DOM
```

**Interview**: "Visibility checks UI rendering, attachment checks DOM presence."

---

### 7.2 Enabled / Disabled / Interaction State

```python
expect(locator).to_be_enabled()                   # User can interact
expect(locator).to_be_disabled()                  # Disabled
expect(locator).to_be_editable()                  # Enabled and writable
```

**Interview**: "I use `enabled` vs `editable` to distinguish clickable from writable elements."

---

### 7.3 Checkbox & Radio Assertions

```python
expect(locator).to_be_checked()                   # Selected
expect(locator).to_be_unchecked()                 # Not selected
```

**Interview**: "These assertions validate user selection state, not attributes."

---

### 7.4 Text Assertions (Most Common)

```python
expect(locator).to_have_text("Login")             # Exact match
expect(locator).to_contain_text("Log")            # Partial match
expect(locator).to_have_text(re.compile("Log.*")) # Regex match
```

**Interview**: "I use `to_have_text()` for strict checks and `to_contain_text()` for flexible content."

---

### 7.5 Input & Form Value Assertions

```python
expect(locator).to_have_value("admin")            # Input value
expect(locator).to_have_attribute("type", "email") # Attribute
```

**Interview**: "Value assertions confirm what the application stored, not what we typed."

---

### 7.6 Count & Collection Assertions

```python
expect(locator).to_have_count(5)                  # Exact count
expect(locator_list).to_have_count(0)             # Empty list
```

**Interview**: "I use count assertions for lists, tables, and dynamic search results."

---

### 7.7 Page-Level Assertions

```python
expect(page).to_have_url("https://example.com")   # Exact URL
expect(page).to_have_url(re.compile("dashboard")) # Regex URL
expect(page).to_have_title("Dashboard")           # Page title
```

**Interview**: "Page-level assertions confirm navigation without manual waits."

---

### 7.8 Negative Assertions (Very Important)

```python
expect(locator).not_to_be_visible()               # Must NOT appear
expect(locator).not_to_have_text("Error")         # No error message
expect(page).not_to_have_url("login")             # Not on login page
```

**Interview**: "Negative assertions are as important as positive ones for test stability."

---

## Complete Interview Power Answer

> **"In Python Playwright, I use accessibility-based locators (`get_by_role`, `get_by_label`) for stability, rely on auto-waiting actions and assertions instead of sleeps, handle navigation and dialogs through events with proper registration order, and fall back to XPath only when semantic locators aren't available. Assertions are auto-retrying, which prevents flakiness."**

---

## How Interviewers Will Test This

1. **Why `get_by_role` over XPath?**
   - Answer: "It's based on accessibility semantics, not implementation. Survives DOM changes."

2. **Difference between `fill()` and `type()`?**
   - Answer: "`fill()` clears first, `type()` appends. Use `fill()` for inputs, `type()` for search fields."

3. **How do you handle new tabs safely?**
   - Answer: "I use `context.expect_page()` before clicking, not after, to avoid race conditions."

4. **Why are Playwright tests less flaky?**
   - Answer: "Auto-waiting + auto-retrying assertions. No manual sleeps = no timing issues."

5. **When would you use XPath?**
   - Answer: "Only when I can't use role, label, or text locators. It's a fallback."

---

## Practice Checklist

- [ ] Convert one real website into only `get_by_role()` locators
- [ ] Replace every `sleep()` with assertions
- [ ] Handle one popup + one new tab without race conditions
- [ ] Write negative assertions for error states
- [ ] Use regex assertions for dynamic content

---

**You're ready for any Playwright Python interview! 🚀**
