'''This file will import the necessary packages using pip'''

try:
    import pip
except ImportError:
    print("This program requires pip to be install or you must manually install the dependencies.")

installed_packages = pip.get_installed_distributions()
flat_installed_packages = [package.project_name for package in installed_packages]

required_packages = ['chardet','flask','httplib2','google-api-python-client','pydrive','tlslite','twilio','urllib3']

for package in required_packages:
    if package not in flat_installed_packages:
        pip.main(['install',package])
