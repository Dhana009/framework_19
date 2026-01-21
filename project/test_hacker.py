from ast import expr_context
from math import exp
from playwright.sync_api import expect
import re
import json

class TestOne:
    def test_title(self, page):
        page.wait_for_url('https://projects.hackerearth.com/p2#/')
        return {"title":page.title}
    
    def test_profile(self,page):
        profile_loc = page.get_by_role('link',name="Profile")
        profile_loc.click()
        expect(page).to_have_url(re.compile('.*profile.*'))

        profile_header_text = page.get_by_role('heading',name="Profile Page")
        profile_text = profile_header_text.inner_text()

        return {
            "profile_url":page.url,
            "profile_header":profile_text
        }
    
    def test_navigate_details(self,page):
        profile_loc = page.get_by_role('link',name="Profile")
        profile_loc.click()
        expect(page).to_have_url(re.compile('.*profile.*'))
        view_details = page.locator("xpath=//a[@href='#/profile/details']")
        view_details.click()

        expect(page).to_have_url(re.compile('.*details.*'))
        header_text = page.locator("xpath=//h2[text()='Profile Details']")
        name_text = page.locator("xpath=(//section/p[@class='sc-enNhQL jraRAA'])[1]")

        expect(name_text).to_contain_text("Name: John Doe")
        x ={
            "url":page.url,
            "header":header_text.inner_text(),
            "name":name_text.text_content()

        }

        with open('a.json','a') as f:
            json.dump(x,f,indent=2)

        return x
    
    def test_edit_profile(self,page):
        profile_loc = page.get_by_role('link',name="Profile")
        profile_loc.click()
        expect(page).to_have_url(re.compile('.*profile.*'))
        edit_details = page.locator("xpath=//a[@href='#/profile/edit']")
        edit_details.click()

        x = page.get_by_label('Name:')
        expect(x).to_have_value('John Doe')

        x.fill('Jane Doe')
        expect(x).to_have_value('Jane Doe')

        button = page.locator("xpath=//button[text()='Save Changes']")
        expect(button).to_be_enabled()

        button.click()

        view_details = page.locator("xpath=//a[@href='#/profile/details']")
        view_details.click()

        name_text = page.locator("xpath=(//section/p[@class='sc-enNhQL jraRAA'])[1]")

        expect(name_text).to_contain_text("Name: Jane Doe")
        x ={
            "url":page.url,
            "name":name_text.text_content()

        }

        with open('a.json','a') as f:
            json.dump(x,f,indent=2)

        return x




