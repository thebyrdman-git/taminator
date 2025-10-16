#!/usr/bin/env python3

from ansible.module_utils.basic import AnsibleModule
import os
import subprocess
import sys

def copy_to_clipboard(content):
    """Copy content to clipboard using available method"""
    
    # Try different clipboard methods
    methods = [
        ['xclip', '-selection', 'clipboard'],
        ['wl-copy'],
        ['pbcopy'],
        ['xsel', '--clipboard', '--input']
    ]
    
    for method in methods:
        try:
            process = subprocess.Popen(method, stdin=subprocess.PIPE, 
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(input=content.encode('utf-8'))
            
            if process.returncode == 0:
                return True, method[0]
        except (OSError, subprocess.SubprocessError):
            continue
    
    return False, None

def main():
    module = AnsibleModule(
        argument_spec=dict(
            report_file=dict(type='str', required=True),
            display_content=dict(type='bool', default=True)
        ),
        supports_check_mode=True
    )
    
    report_file = module.params['report_file']
    display_content = module.params['display_content']
    
    # Check if file exists
    if not os.path.exists(report_file):
        module.fail_json(msg=f"Report file not found: {report_file}")
    
    # Read file content
    try:
        with open(report_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        module.fail_json(msg=f"Failed to read report file: {str(e)}")
    
    # Try to copy to clipboard
    copied, method = copy_to_clipboard(content)
    
    result = {
        'report_file': report_file,
        'content_length': len(content),
        'copied_to_clipboard': copied,
        'clipboard_method': method
    }
    
    if display_content:
        result['content'] = content
    
    if copied:
        module.exit_json(changed=False, msg=f"Report copied to clipboard using {method}", **result)
    else:
        module.exit_json(changed=False, msg="Report content available (clipboard not available)", **result)

if __name__ == '__main__':
    main()
