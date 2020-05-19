import os
from libcloud_driver_kamatera import get_node_driver

print("Instantiating the driver")

if os.environ.get('KAMATERA_API_SERVER') == 'localhost':
    kwargs = {'secure': False, 'host': 'localhost', 'port': int(os.environ.get('CLOUDCLI_SERVER_PORT', '8000'))}
else:
    kwargs = {}

cls = get_node_driver()
driver = cls(os.environ["KAMATERA_API_CLIENT_ID"], os.environ["KAMATERA_API_SECRET"], **kwargs)

print("Setting create node params from capabilities, locations and size lists")

locations = {location.id: location for location in driver.list_locations()}
assert locations['IL'].country == 'Israel'
assert locations['IL-JR'].name == 'Jerusalem'
assert locations['EU'].id == 'EU'
location = locations['EU']
capabilities = driver.ex_list_capabilities(location)
cpuTypes = {cpuType['id']: cpuType for cpuType in capabilities['cpuTypes']}
assert cpuTypes['B']['name'] == 'Type B - General Purpose'
cpuType = cpuTypes['B']
assert len(cpuType['cpuCores']) > 2
cpuCores = cpuType['cpuCores'][1]
assert len(cpuType['ramMB']) > 3
ramMB = cpuType['ramMB'][2]
assert(len(capabilities['diskSizeGB']) > 3)
diskSizeGB = capabilities['diskSizeGB'][2]
billingCycle = driver.EX_BILLINGCYCLE_HOURLY
assert(len(capabilities['monthlyTrafficPackage']) > 1)
size = driver.ex_get_size(ramMB, diskSizeGB, cpuType['id'], cpuCores)
selected_image = None
for image in driver.list_images(location):
    if image.name == 'Ubuntu Server version 18.04 LTS (bionic) 64-bit':
        selected_image = image
        break
assert selected_image

CREATE_SERVER_NAME = os.environ.get("CREATE_SERVER_NAME")
if not CREATE_SERVER_NAME:
    print("Skipping create server tests")
    exit(0)

kwargs = {
    "name": CREATE_SERVER_NAME,
    "size": size,
    "image": selected_image,
    "location": location,
    "ex_billingcycle": billingCycle
}

print('creating node...')
print(kwargs)

node = driver.create_node(**kwargs)

created_node_name = node.name

assert created_node_name.startswith(CREATE_SERVER_NAME)
assert len(node.id) > 5
assert node.state == 'running'
assert len(node.public_ips) > 0
assert len(node.extra) > 3
assert len(node.extra['generated_password']) > 5

print('libcloud create node: Great Success!')

nodes = driver.list_nodes(created_node_name)
assert len(nodes) > 0
node = nodes[0]
assert node.name == created_node_name
assert len(node.id) > 5
assert node.state == 'running'
assert len(node.public_ips) > 0
assert len(node.extra) > 3

print('running node operations...')

print('stop')
assert node.stop_node()
print('start')
assert node.start()
print('reboot')
assert node.reboot()
print('destroy')
assert node.destroy()

print('libcloud node operations: Great Success!')
