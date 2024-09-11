from streamlit_cookies_controller import CookieController

cookie_manager = CookieController()


def get_cookie_manager():
    global cookie_manager
    if cookie_manager:
        return cookie_manager
    else:
        cookie_manager = CookieController()
        return cookie_manager
