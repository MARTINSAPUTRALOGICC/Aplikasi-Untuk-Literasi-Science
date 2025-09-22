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


column_kampus = ["Number", "Name Kampus", "Alamat Kampus", "Action"]
column_sidebar = ["Number","Name Page","Icon Page","Url Page","Action"] 
column_role = ["Number","Name Level","Action"]

def get_icon_url():
    return url_for("static", filename="assets/book.png")


base_url = "https://"


title_website = "Aplikasi Untuk Literasi Science"


# ROUTE AJAX
ajaxaccount = "/ajaxAccount"
ajaxlevel = "/ajaxLevel"
ajaxkampus = "/ajaxKampus"
ajaxsidebar = "/ajaxSidebar"


# ROUTE GET AJAX
getajaxaccount = "/get_account_data"
getajaxlevel = "/get_level_data"
getajaxkampus = "/get_kampus_data"
getajaxsidebar = "/get_sidebar_data"

# CRUD ROUTE
insertaccountcrud = "useraccount.create_useraccount"
deleteaccountcrud = "/account/delete/${productId}"
updateaccountcrud = "/userupdate/${productId}"

insertlevelcrud = "levelaccount.levelaccount"
deletelevelcrud = "/level/delete/${productId}"
updatelevelcrud = "/levelupdate/${productId}"

insertsidebarcrud = "sidebaraccount.sidebaraccount"
deletesidebarcrud = "/sidebar/delete/${productId}"
updatesidebarcrud = "/sidebarupadate/${productId}"


insertkampuscrud = "kampusaccount.createkampus"
deletekampuscrud = "/kampus/delete/${productId}"
updatekampuscrud = "/kampusupdate/${productId}"

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
page6 = "kampus"
