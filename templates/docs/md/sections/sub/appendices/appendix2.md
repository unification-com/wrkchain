
### $__SECTION_NUMBER__.$__SUB_SECTION_NUMBER__ Appendix 2: Production Deployment via Ansible

To help deploy a production WRKChain, Ansible scripts also generated and 
deposited into the `build/ansible` directory. These Ansible scripts have been 
tested against a CentOS 7 machine. They should be generic enough to be run on 
any Linux variation.

Instructions how to set up Ansible can be obtained here:
<https://www.ansible.com>

#### Vagrant Testing

The Ansible scripts can be tested via Vagrant by running:

```bash
cd build/ansible
vagrant up
```
Instruction how to set up Vagrant can be found here:
<https://www.vagrantup.com>

#### Production Deployment

Add each of the node names to `/etc/ansible/hosts`

Add name resolution to the node names. The simplest is to add mappings to 
`/etc/hosts`

Run each of the Ansible playbooks generated:
```bash
ansible-playbook wrkchain-node-1.yml
```

Once these machines are provisioned, read the specific sections on how
to either provision a Bootnode or a Validator Node in the previous sections.