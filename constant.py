from flask import url_for


dashboard_screen = "dashboard.html"
login_screen = "login.html"


column_useraccount = [
    "Number",
    "Name",
    "Email",
    "Password",
    "Level User",
    "Kampus",
    "Status",
    "Create By",
    "Last Login",
    "Action",
]


column_website_client = ["Number", "Name Website","Action"]
column_sidebar = ["Number","Name Page","Icon Page","Url Page","Action"] 
column_role = ["Number","Name Level","Action"]
column_pagese =["Number","User Account","Page1","Page2","Page3","Page4","Page5","Page6","Page7","Action"]

def get_icon_url():
    return url_for("static", filename="assets/book.png")


base_url = "https://"


title_website = "Aplikasi Untuk Literasi Science"


# ROUTE AJAX
ajaxaccount = "/ajaxAccount"
ajaxlevel = "/ajaxLevel"
ajaxwebsite = "/ajaxWebsite"
ajaxsidebar = "/ajaxSidebar"


# ROUTE GET AJAX
getajaxaccount = "/get_account_data"
getajaxlevel = "/get_level_data"
getajaxwebsite = "/get_website_data"
getajaxsidebar = "/get_sidebar_data"

# CRUD ROUTE
insertaccountcrud = "useraccount.create_useraccount"
deleteaccountcrud = "/account/delete/${productId}"
updateaccountcrud = "/userupdate/${productId}"

insertlevelcrud = "levelaccount.levelaccount"
deletelevelcrud = "/level/delete/${productId}"
updatelevelcrud = "/levelupdate/${productId}"

insertwebcrud = "websiteaccount.websiteaccount"
deletewebcrud = "/website/delete/${productId}"
updatewebcrud = "/websiteupadate/${productId}"

insertsidebarcrud = "sidebaraccount.sidebaraccount"
deletesidebarcrud = "/sidebar/delete/${productId}"
updatesidebarcrud = "/sidebarupadate/${productId}"


server = "localhost"
user_server = "root"
password_server = ""
db1 = "auls"

# Route Function

Dashboard = "dashboard"
Leveluser = "LevelUser"
Kampus = "Kampus"
Sidebarpage = "Page"

# ROUTE GET COLUMN
page1 = "account"
page2 = "leveluser"
page3 = "sidebar"
page6 = "website"
