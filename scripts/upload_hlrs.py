import yaml
import subprocess

# 1 Open and load YAML file

data = yaml.safe_load(open('docs/requirements.yaml'))

# 2 Loop through each module (e.g. physics engine)
for module_name, hlr_list in data.items():
    if isinstance(hlr_list, dict):
        # 3 Loop through HLRS
        for hlr_id, spec in hlr_list.items():
            title = f"[{hlr_id}]{spec['title']}"
            body = spec['description']
            labels = f"requirements,{module_name}"

            # 4 Run GitHub CLI issue creation command
            subprocess.run([
                'gh','issue','create',
                '--title', title,
                '--body', body,
                '--labels', labels
                ])