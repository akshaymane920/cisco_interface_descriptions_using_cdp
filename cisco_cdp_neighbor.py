import re

# Taken from napalm-automation
# GitHub Issue #185-->napalm-iosImplemented get_cdp_neighbors() and modified get_lldp_neighbors()
# Link--> https://github.com/napalm-automation/napalm-ios/pull/185/files/63ff90c33fbbecfa868eb0477b56f8b5b89d133e


def get_cdp_neighbors(cdp_neighbor_output):
    """IOS implementation of get_cdp_neighbors."""
    cdp = {}

    # Check if router supports the command
    if '% Invalid input' in cdp_neighbor_output:
        return {}

    # Process the output to obtain just the CDP entries
    try:
        split_output = re.split(r'^Device ID.*$', cdp_neighbor_output, flags=re.M)[1]
        split_output = re.split(r'^Total cdp entries displayed.*$', split_output, flags=re.M)[0]
    except IndexError:
        return {}

    split_output = split_output.strip()

    partial_line = False  # When true, the hostname is on a different line than the other entries
    for cdp_entry in split_output.splitlines():
        # Example, Router3  Eth 0/2 138  R B  Linux Uni Eth 0/1
        # We can't use the same method as for LLDP because there are spaces between items
        # belonging in the same column. Instead we parse the output using the column lenghts,
        # hoping these have a fixed size between different IOS versions.
        if len(cdp_entry.split()) == 1:
            # Only one field means the hostname was too long and this line belongs with the next one
            # Retrieve the
            device_id = cdp_entry
            partial_line = True
            continue
        if not partial_line:
            device_id = cdp_entry[:16]
        device_id = device_id.split('.')[0]  # We want only the hostname, not the FQDN
        local_int_brief = cdp_entry[17:35].strip()
        hold_time = cdp_entry[35:46].strip()
        capability = cdp_entry[46:58].strip()
        remote_port = cdp_entry[68:].strip()
        platform_tmp = cdp_entry[
                       58:68].strip()
        local_port = local_int_brief
        entry = {'port': remote_port, 'hostname': device_id}
        cdp.setdefault(local_port, [])
        cdp[local_port].append(entry)
        partial_line = False
    return cdp
