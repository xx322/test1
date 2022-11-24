import subprocess
from time import sleep
import json
import argparse

vmlist = ['Standard_B1s']

HEADER = '\033[1m'
FAIL = '\033[91m'
ENDC = '\033[0m'


def run(cmd, shell=True):
    data = subprocess.run(cmd, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if 'ERROR' in data.stderr.decode():
        print(cmd)
        print(FAIL)
        print(data.stderr.decode())
        print(ENDC)
        exit()
    return data.stdout.decode()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vm', type=str, default='vm', help="VM name")
    parser.add_argument('-g', '--group', type=str, default='vm_group', help="Resource group name")
    parser.add_argument('-s', '--sub', type=str, default=None, help="Subscription id")
    param = parser.parse_args()

    vmips = {}

    #################
    s1 = f"az vm open-port --resource-group {param.group} --name {param.vm} --port 7071"
    s2 = f"az vm show -d -g {param.group} -n {param.vm} --query publicIps -o tsv"
    if param.sub:
        s1 = f"{s1} --subscription {param.sub}"
        s2 = f"{s2} --subscription {param.sub}"

    print(f'{HEADER}Open port 7071 for VM{ENDC}')
    run(s1)
    ip = run(s2).strip()
    vmips['vm'] = ip

    #################

    # print(f'{HEADER}Create Azure VM{ENDC}')
    # for i, size in enumerate(vmlist):
    #   name = f'vm{i+1}'
    #   dat = run(f'az vm create --resource-group vm_group --name {name} --size {size} --image UbuntuLTS --ssh-key-values keys/id_rsa.pub --admin-username azureuser')

    ##################

    # print(f'{HEADER}Wait for deployment (1 minute){ENDC}')
    # sleep(60)

    #################

    # print(f'{HEADER}Open port 7071 for other VMs{ENDC}')
    # for i, size in enumerate(vmlist):
    #   name = f'vm{i+1}'
    #   run(f'az vm open-port --resource-group vm_group --name {name} --port 7071')

    #################

    # print(f'{HEADER}Install Dependencies and Deploy Functions{ENDC}')
    # for i, size in enumerate(vmlist):
    #   name = f'vm{i+1}'
    #   ip = run(f"az vm show -d -g vm_group -n {name} --query publicIps -o tsv").strip()
    #   vmips[name] = ip
    #   run(f'ssh -o StrictHostKeyChecking=no -i ./keys/id_rsa azureuser@{ip} "mkdir ~/WorkflowSchedulingCwk"')
    #   run(f'rsync -Pav -e "ssh -i ./keys/id_rsa" ~/WorkflowSchedulingCwk/funcstart.sh azureuser@{ip}:/home/azureuser/WorkflowSchedulingCwk/funcstart.sh')
    #   run(f'rsync -Pav -e "ssh -i ./keys/id_rsa"  ~/WorkflowSchedulingCwk/functions/ azureuser@{ip}:/home/azureuser/WorkflowSchedulingCwk/functions/')
    #   run(f"ssh -o StrictHostKeyChecking=no -i ./keys/id_rsa azureuser@{ip} 'sudo apt-get -y update'")
    #   run(f"ssh -o StrictHostKeyChecking=no -i ./keys/id_rsa azureuser@{ip} 'sudo apt-get -y install python3-venv python3-pip python3-distutils python3-apt'")
    #   run(f"ssh -o StrictHostKeyChecking=no -i ./keys/id_rsa azureuser@{ip} 'wget -O ~/pkg.deb -q https://packages.microsoft.com/config/ubuntu/19.04/packages-microsoft-prod.deb'")
    #   run(f"ssh -o StrictHostKeyChecking=no -i ./keys/id_rsa azureuser@{ip} 'sudo dpkg -i ~/pkg.deb'")
    #   run(f"ssh -o StrictHostKeyChecking=no -i ./keys/id_rsa azureuser@{ip} 'sudo apt-get -y update && sudo apt-get -y install azure-functions-core-tools'")
    #   run(f"ssh -o StrictHostKeyChecking=no -i ./keys/id_rsa azureuser@{ip} 'sudo chmod +x ~/WorkflowSchedulingCwk/funcstart.sh'")
    #   run(f"ssh -o StrictHostKeyChecking=no -i ./keys/id_rsa azureuser@{ip} 'cd ~/WorkflowSchedulingCwk && ./funcstart.sh &>/dev/null'")

    #################

    print(f'{HEADER}Saving VM IPs to ips.json{ENDC}')
    with open('ips.json', 'w') as f:
        json.dump(vmips, f)
