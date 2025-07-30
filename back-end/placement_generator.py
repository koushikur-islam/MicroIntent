import json
from collections import defaultdict
import intent_parser

def extract_all_nodes(infrastructure_description):
    nodes = []
    for item in infrastructure_description:
        if "nodes" in item:
            for node in item["nodes"]:
                if node not in nodes:
                    nodes.append(node)
    return nodes
    
def allocate_resource(continuum, slos):
    placement = []
    
    for slo in slos:
        layer = None
        nodes = []
        layer = next((item for item in continuum if item.get("layer") == slo["layer"]), None)
        if layer is None:
            layer = continuum[0]
        
        nodes = [node['name'] for node in layer.get('nodes', [])]
        
        for item in slo["slos"]:
            if item["category"] == "networking" and not item["requirements"]==[]:
                nodes = []
                for switch in layer["switches"]:
                    for intent in item["requirements"]:
                        if intent['metric'] == "latency" and intent["target"]["min"] ==0 and intent["target"]["max"] == 0:
                            nodes = switch["connected-nodes"]
                        elif (intent["metric"] in switch and switch[intent["metric"]] >= intent["target"]["min"] and switch[intent["metric"]] <= intent["target"]["max"]):
                            nodes = switch["connected-nodes"]
            
            if item["category"] == "hardware" and not item["requirements"]==[]:
                if nodes == []:
                    nodes = extract_all_nodes(continuum)
                    nodes = [node['name'] for node in nodes]
            
            node_found = False
            for node in extract_all_nodes(continuum):
                if node["name"] in nodes:
                    node_satisfies_all_slos = True
                    for hardwareItem in slo["slos"][1]["requirements"]:
                        if not (isinstance(node[hardwareItem['metric']], (int, float)) and (node[hardwareItem['metric']] >= hardwareItem["target"]["min"] and node[hardwareItem['metric']] <= hardwareItem["target"]["max"])):
                            node_satisfies_all_slos = False
                            break
                        
                    if node_satisfies_all_slos:
                        for related_service in slo["related_services"]:
                            if not any(entry["service"] == related_service and entry["node"] == node["name"] for entry in placement):
                                placement.append({'service': related_service, 'node': node["name"]})
                        
                        if not any(entry["service"] == slo["service"] and entry["node"] == node["name"] for entry in placement):
                            placement.append({'service': slo["service"], 'node': node["name"]})
                        node_found = True
                        break
            if not node_found:
                placement.append({'service': slo["service"], 'node': "No matching node found."})    
            
    return placement      
                     
                    
def generate_placement_strategy(intents, continuum):
    extracted_slos = intent_parser.extract_slos(intents, continuum)
    return allocate_resource(continuum, extracted_slos)