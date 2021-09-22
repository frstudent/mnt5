#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is frstudent homework module

version_added: "1.0.0"

description: Create file on remote host and write contnent to it

options:
    path:
        description: Path to file
        required: true
        type: str
    context:
        description: Content of file
        required: false
        type: str
    overwrite:
        description: Force overwrite if file exist
        required: false
        type: bool

author:
    - FR student of Netology (@frstudent)
'''

EXAMPLES = r'''
# Pass
- name: Test with a message
  netology.frstudent.fr_module:
    path: /tmp/testfile.txt

'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
path:
    description: The file path
    type: str
    returned: always
    sample: '/tmp/testfile.txt'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'File successfully created and written'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_bytes
import os

def run_module():
    # creates file on remote host with context defined by context
    module_args = dict(
        path=dict(type='str', required=True),
        context=dict(type='str', required=False, default=False),
	overwrite=dict(type='bool', required=False, default=False)
    )

    result = dict(
        changed=False,
        path='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # part where your module will do what it needs to do)
    filepath = module.params['path']
    fileexist = os.path.isfile(filepath)
    result['path'] = filepath

    # Check file
    if module.check_mode:
        if fileexist:
           result['message'] = 'File already exist'
        else:
           result['message'] = 'File not exist'
        module.exit_json(**result)

    # made any modifications to your target
    if fileexist and not module.params['overwrite']:
        result['changed'] = False
        result['message'] = 'File exist. No changes made'
        module.exit_json(**result)
    try:
        with open(filepath, "w") as outfile:
#           outfile.write(to_bytes(module.params['context']))
           outfile.write(module.params['context'])
    except IOError:
           result['message'] = 'Unable create or write file. Not enough access rights?'
           module.exit_json(**result)

    result['message'] = 'File successfully created and written'
    result['changed'] = True

    # We will not generated exception. Only results

    #if module.params['name'] == 'fail me':
    #    module.fail_json(msg='You requested this to fail', **result)

    # All done!
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
