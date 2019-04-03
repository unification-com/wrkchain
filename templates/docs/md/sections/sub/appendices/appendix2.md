
## $__SECTION_NUMBER__.$__SUB_SECTION_NUMBER__ Appendix 2: Production Deployment via Ansible

Ansible is an IT automation framework supported by RedHat. To help deploy a 
production WRKChain, Ansible scripts also generated and deposited into the 
`build/ansible` directory. These Ansible scripts have been tested against a 
CentOS 7 machine. They should be generic enough to be run on any Linux 
variation.

Instructions how to set up and use Ansible can be obtained here:
<https://www.ansible.com/resources/get-started>

These scripts can optionally be tested with Vagrant, and then deployed to 
production machines.

### $__SECTION_NUMBER__.$__SUB_SECTION_NUMBER__.1 Vagrant Testing

Testing the Ansible script via Vagrant can simply be started by:

```bash
cd build/ansible
vagrant up
```

Instruction how to set up Vagrant can be found here:
<https://www.vagrantup.com/intro/index.html>

### $__SECTION_NUMBER__.$__SUB_SECTION_NUMBER__.2 Production Deployment

Add each of the node names to `/etc/ansible/hosts`

Add name resolution to the node names. The simplest is to add mappings to 
`/etc/hosts`

Run each of the Ansible playbooks generated:
```bash
ansible-playbook -u <REMOTE_USER> wrkchain-node-1.yml
```

For example, on a standard AWS host, the REMOTE_USER is ec2-user.

Once these machines are provisioned, read the specific sections on how
to either provision a Bootnode or a Validator Node in the previous sections.
