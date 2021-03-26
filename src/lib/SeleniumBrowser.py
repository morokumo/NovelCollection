# from selenium import webdriver
# from selenium.webdriver import DesiredCapabilities
#
# from config import DRIVER_URL
#
#
# class Browser:
#     def __init__(self):
#         self.DRIVERS = {
#             'narou': webdriver.Remote(
#                 command_executor=DRIVER_URL,
#                 desired_capabilities=DesiredCapabilities.FIREFOX.copy(),
#                 # options=options
#             ),
#             # 'hameln': webdriver.Remote(
#             #     command_executor=DRIVER_URL,
#             #     desired_capabilities=DesiredCapabilities.FIREFOX.copy(),
#             #     # options=options
#             # )
#         }
#
#     def restart(self):
#         self.DRIVERS = {
#             'narou': webdriver.Remote(
#                 command_executor=DRIVER_URL,
#                 desired_capabilities=DesiredCapabilities.FIREFOX.copy(),
#                 # options=options
#             ),
#             # 'hameln': webdriver.Remote(
#             #     command_executor=DRIVER_URL,
#             #     desired_capabilities=DesiredCapabilities.FIREFOX.copy(),
#             #     # options=options
#             # )
#         }
