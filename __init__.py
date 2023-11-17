import json
from binaryninja import PluginCommand
from binaryninja.interaction import OpenFileNameField, get_form_input
from binaryninja.log import *



def open_file() -> list | None:
    """Opens CAPA JSON output file by Binja's OpenNameField

    Returns:
        list: All rules that matches binary functions and their addresses
    """
    file = OpenFileNameField("CAPA JSON output")
    get_form_input([file], "Please open CAPA JSON output")
    if file:
        with open(file.result, 'r', encoding='utf-8') as f:
            log_info(f"Successfully opened file : {file.result}")
            try:
                data = json.loads(f.read())
                if data['rules']:
                    rules = data['rules']
                    log_info(f"{len(rules)} rules imported")
                    return rules
                else:
                    log_error("The file seems not to contain any match")
                    return None
            except Exception as e:
                log_error(f"Unable to load file : {e}" )
                return None
    
    
def get_capabilities(data : list) -> list:
    """Gets all the capabilities names

    Args:
        data (list): List of all capabilities and addresses

    Returns:
        list: List of only capabilities names (used to navigate through matches)
    """
    if data:
        return [cap for cap in data]

def main(bv):
    rules = open_file()
    if rules is not None:
        capabilities = get_capabilities(rules)
        if capabilities:
            for i in capabilities:
                matches = rules[i]['matches']
                rulename = rules[i]['meta']['name']
                if matches:
                    try:
                        matches[0][0]['value'] #Dummy check if matches have value
                        bv.create_tag_type(rulename, "🔵")
                        log_info(f"{rulename} tag type has been created")
                        for match in matches:
                            bv.add_tag(match[0]['value'], rulename, rulename)
                            log_info(f"Tag added for {rulename} at {hex(match[0]['value'])}")
                    except KeyError:
                        pass
                
                
PluginCommand.register("CAPA\\Load export file",
                       "Loads json output file from CAPA", main)