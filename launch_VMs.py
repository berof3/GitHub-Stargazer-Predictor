import time, os, sys
from os import environ as env
from novaclient import client
from keystoneauth1 import loading, session

# --- Configuration ---
flavor_name = "ssc.medium" 
private_net = "UPPMAX 2026/1-24 Internal IPv4 Network"
image_name = "Ubuntu 22.04 - 2024.01.15"
key_name = 'DEII_Final_Project_Key' 

# --- Authentication ---
loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(
    auth_url=env['OS_AUTH_URL'],
    username=env['OS_USERNAME'],
    password=env['OS_PASSWORD'],
    project_name=env['OS_PROJECT_NAME'],
    project_domain_id=env['OS_PROJECT_DOMAIN_ID'],
    user_domain_name=env['OS_USER_DOMAIN_NAME']
)
sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print("User authorization completed.")

# --- Find Resources ---
image = nova.glance.find_image(image_name)
flavor = nova.flavors.find(name=flavor_name)
net = nova.neutron.find_network(private_net)
nics = [{'net-id': net.id}]

# --- Load Config ---
cfg_file_path = os.getcwd() + '/cloud-cfg.txt'
userdata = open(cfg_file_path)

# --- Launch Dev and Prod ---
server_names = ["group15-dev", "group15-prod"]
created_instances = []

for name in server_names:
    print(f"Provisioning {name}...")
    instance = nova.servers.create(
        name=name, image=image, key_name=key_name, 
        flavor=flavor, userdata=userdata, nics=nics,
        security_groups=['default']
    )
    created_instances.append(instance)

print("Waiting for servers to become ACTIVE...")
time.sleep(10)
print("\nInfrastructure build initiated. Check your dashboard in 2 minutes.")
