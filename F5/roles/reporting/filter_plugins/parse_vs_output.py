def parse_vs_output(stdout_lines):
    vs_list = []
    current_vs = {}
    in_policies = False
    for line in stdout_lines:
        line = line.strip()
        if line.startswith('ltm virtual'):
            if current_vs:
                vs_list.append(current_vs)
            current_vs = {'name': line.split()[2], 'destination': '', 'asm_policy': 'none'}
            in_policies = False
        elif line.startswith('destination'):
            current_vs['destination'] = line.split()[1]
        elif line.startswith('policies {'):
            in_policies = True
        elif line.startswith('}'):
            in_policies = False
        elif in_policies and '{' in line:
            policy_name = line.split('{')[0].strip()
            if 'asm' in policy_name.lower():
                current_vs['asm_policy'] = 'present'
        elif line.startswith('policies none'):
            current_vs['asm_policy'] = 'none'
    if current_vs:
        vs_list.append(current_vs)
    return vs_list