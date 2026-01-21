from playwright.sync_api import sync_playwright, expect
import re
import json

link="https://rahulshettyacademy.com/AutomationPractice/"
def test_navigate_to_google(page):
    """Test basic navigation to Google"""
    page.goto('https://www.google.com/')


def test_browser_setup_with_context():
    """Test manual browser setup with context"""
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto('https://www.google.com')
        context.close()
        browser.close()

def test_radio_button_selection(page):
    """Test selecting a radio button"""
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    radio = page.locator("xpath=//label[contains(normalize-space(.),'Radio1')]/input")
    radio.check()
    expect(radio).to_be_checked()

def test_autocomplete_dropdown_selection(page):
    """Test autocomplete dropdown with text input"""
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    input_field = page.locator("xpath=//div[@id='select-class-example']//input")
    input_field.type('india')
    page.get_by_text('India', exact=True).click()
    expect(input_field).to_have_value('India')

def test_select_dropdown_selection(page):
    """Test HTML select dropdown"""
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    select = page.locator("#dropdown-class-example")
    expect(select).to_be_enabled()
    select.select_option("option2")
    expect(select).to_have_value("option2")
    
def test_checkbox_selection(page):
    """Test selecting a checkbox"""
    page.goto(link)
    check_box = page.locator("xpath=//div[@id='checkbox-example']//input[@value='option1']")
    check_box.check()
    expect(check_box).to_be_checked()

def test_handle_new_window_popup(page):
    """Test handling new window popup"""
    page.goto(link)
    with page.context.expect_page() as new_page:
        page.get_by_role("button", name="Open Window").click()

    new_page = new_page.value
    new_page.wait_for_load_state()
    expect(new_page).to_have_url(re.compile('.*click.*'))

def test_handle_new_tab_click(page):
    """Test handling new tab from link click"""
    page.goto(link)
    with page.context.expect_page() as new_page:
        page.locator("xpath=//a[@href='https://www.qaclickacademy.com']").click()

    new_page = new_page.value
    new_page.wait_for_load_state()
    expect(new_page).to_have_url(re.compile("click"))

def test_handle_alert_dialog(page):
    """Test handling alert dialog"""
    page.goto(link)
    page.locator("xpath=//input[@id='name']").type('testing')
    
    def handle_dialog(dialog):
        assert "share your knowledge" in dialog.message
        dialog.accept()
    
    page.once("dialog", handle_dialog)
    page.locator("xpath=//input[@id='alertbtn']").click()
        
def test_handle_confirm_dialog(page):
    """Test handling confirm dialog"""
    page.goto(link)
    page.locator("xpath=//input[@id='name']").type('testing')

    def handle_popup(dialog):
        assert 'confirm' in dialog.message
        dialog.dismiss()

    page.once("dialog", handle_popup)
    page.locator("xpath=//input[@id='confirmbtn']")

def test_element_visibility_check(page):
    """Test element visibility and enabled state"""
    page.goto(link)
    locate = page.locator("xpath=//input[@id='displayed-text']")
    hide_button = page.locator("xpath=//input[@id='hide-textbox']")
    hide_button.click()
    expect(locate).to_be_enabled()

def test_table_row_count_with_header(page):
    """Test counting table rows including header"""
    page.goto(link)
    table = page.locator("xpath=(//table[@id='product'])[1]")
    rows = table.locator("xpath=./tbody/tr")
    rows_count = rows.count()
    assert rows_count == 11

def test_table_row_count_without_header(page):
    """Test counting table rows excluding header"""
    page.goto(link)
    table = page.locator("xpath=(//table[@id='product'])[1]")
    rows = table.locator("xpath=./tbody/tr[position()>1]")
    rows_count = rows.count()
    assert rows_count == 10

def test_extract_table_cell_text(page):
    """Test extracting text from table cell"""
    page.goto(link)
    table = page.locator("xpath=(//table[@id='product'])[1]")
    first_cell = table.locator("xpath=./tbody/tr[position()>1]/td[1]").nth(0)
    first_cell.inner_text() == "Rahul Shetty"

def test_extract_table_data_to_json(page):
    """Test extracting all table data and saving to JSON"""
    page.goto(link)
    table = page.locator("xpath=(//table[@id='product'])[1]")
    
    first_cell = table.locator("xpath=./tbody/tr[position()>1]")
    data_ = []
    for i in range(first_cell.count()):
        first_cel = first_cell.nth(i)
        first_cell_1 = first_cel.locator(f"xpath=./td[1]").inner_text()
        second_cell = first_cel.locator(f"xpath=./td[2]").inner_text()
        third_cell = first_cel.locator(f"xpath=./td[3]").inner_text()

        data = {
            "first_cell": first_cell_1,
            "second_cell": second_cell,
            "third_cell": third_cell
        }
        data_.append(data)

    with open("a.json", "w") as f:
        json.dump(data_, f, indent=2)

def test_extract_second_table_data_to_json(page):
    """Test extracting second table data and saving to JSON"""
    page.goto(link)
    table = page.locator("xpath=(//table[@id='product'])[2]")
    table_head = table.locator("xpath=./thead")
    table_rows = table.locator("xpath=./tbody/tr")

    data = []
    for i in range(table_rows.count()):
        rws = table_rows.nth(i)
        one = rws.locator("xpath=./td[1]").inner_text()
        two = rws.locator("xpath=./td[2]").inner_text()
        three = rws.locator("xpath=./td[3]").inner_text()

        data.append({"one": one, "two": two, "three": three})

    with open('x.json', 'w') as f:
        json.dump(data, f, indent=2)
