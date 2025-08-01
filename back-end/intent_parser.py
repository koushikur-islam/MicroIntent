from openai import OpenAI
import json

OPENAI_API_KEY = "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"

def read_local_slos():
    with open('slos.json', 'r') as json_file:
        return json.load(json_file)

def save_slos(json_slos):
    file_path = 'slos.json'
    try:
        with open(file_path, 'w') as json_file:
            json.dump(json_slos, json_file, indent=4)
    except Exception as e:
        print(f"Error saving slos: {str(e)}")
       
def get_llm_response(message, model_name="gpt-4o-mini"):
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": message}],
            max_tokens=3000
        )
        llm_response = response.choices[0].message.content if response.choices else "No response generated."
        return llm_response
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    
def prepare_llm_message(intents, infrastructure_description):
    merged_intents = ''
    for index, intent in enumerate(intents, start=1):
        merged_intents += f"{index}. {intent['intent']} for {intent['service']}. \n"
    
    extracted_slo_structure = '''
    
    [
    {
        "service": "Service Name",
        "layer": "edge | fog | cloud | any",
        "slos": [
            {
                "category": "networking",
                "requirements": [
                    {
                        "metric": "metric-name",
                        "unit": "matching unit",
                        "target": {
                            "min": value,
                            "max": value
                        }
                    }
                ]
            },
            {
                "category": "hardware",
                "requirements": [
                    {
                        "metric": "metric-name",
                        "unit": "matching unit",
                        "target": {
                            "min": value,
                            "max": value
                        }
                    }
                ]
            }
        ],
        "related_services": []
    }
    ]

'''
    
    message = f'''
    
        Generate a JSON file containing SLOs for the following user intents:
        {merged_intents}
        
        The output JSON file should have the following fields:
        1. `service`: Places the name of intended service.
        2. `layer`: Name of the intended layer.
        3. `slos`: Must be separated into two distinct categories as 3a and 3b:
            
            3a. `networking`: consists of an array which includes metrics like `latency`, `bandwidth`, or any other metrics related to network performance.
            3b. `hardware`: consists an array which includes metrics like `memory`, `cpu-cores`, `gpu-cores`, `operating-system`, or any other metrics related to hardware or system properties.

        Both 3a and 3b consisnts of the following fields:
        1. `metric`: Name of the metric from the intent like `latency` for `networking` and `memory` for `hardware` etc.
        2. `unit`: Name of the unit for the intended metric. `unit` field must follow the followings:
            
            2a. If no unit is specified in the intent then consider the unit from the matcing metric from the infrastructure description proviced.
            2b. If a unit is specified in the intent then match the unit to the corresponding unit of the metric from the infrastructure description proviced, if required convert it to the one is infrastructure description.

        3. `target`: The target is the value(s) of the intended metric. This can be both numeric and non-numeric on a high level.
            The `target` field consists of two values as follows:
            
            3a. `min`: This is the minimum value for the intended metric. The rules to put `min` value are as follows:
             1. If the intended metric is numeric and given in a range then put the lowest value in the range.
             2. If the intended metric is non-numeric and on high level description like minimum, low etc. then look for the minimum value of the matching metric from the infrastructure description for the intended layer and also make the corresponding `max` value as the same as `min`. If no layer is specified in intent then look in the first layer for the intended metric and put the lowest value.
            
                        
            3b. `max`: This is the maximum value for the intended metric. The rules to put `max` value are as follows:
             1. If the intended metric is numeric and given in a range then put the highest value in the range.
             2. If the intended metric is non-numeric and on high level description like minimum, maximum, low, high, average etc. then look for the maximum value of the matching metric from the infrastructure description for the intended layer and also make the corresponding `min` value as the same as `max`. If no layer is specified in intent then look in the first layer for the intended metric and put the highest value.

        4. `related_services`: This is an array of services the are associated with the requested service for networking purpose. For example, if Service A requires minimum latency with Services 2 and 3 then this array should contain Service 2 and Service 3.

        The structure of the JSON must match the matrices name and unit of the infrastructure description.
        The infrastructure description is as follows:
        
        {infrastructure_description}
        
        Overall, the requires SLO.json file must maintain a strcutreu like this: 
        
        {extracted_slo_structure}
        
        Strict considerations when generating the JSON file:
        1. Exclude any metrics that are not present in the provided infrastructure description.
        2. Use metric name from the provided intent to match with the infrastructure description. Always pick the exact name from infrastructure description which seems a possible match from the intent.
        3. The `layer` field should default to `'any'` unless explicitly mentioned in the intent.
        4. The `slos` field must be a list of two objects, `networking` and `hardware`, each containing their respective metrics with the fields `metric`, `unit` and `target` where target having two fields `min` and `max`.
        5. Each service must have a unique `service` field for the service name, `layer` for the intended layer name and the `slos` field must correspond to its requirements as defined in the intents.
        6. Generate only valid JSON output, starting with an array of the defined objects.
        7. When intent has latency metric specified to reduce between two services, then choose the same layer for those services and put latency equal to zero (0).
        8. Consider latency is always zero between two nodes in the infrastructure description within the same layer.
        9. Do not put anything in the `hardware` or `networking` array if no hardware or networking requriedment is specified in the intents.
        10. Ensure the JSON is formatted for readability with an indentation level of 4 spaces.
        11. No additional text apart from the JSON is expected to be generated.'''
        
    return message

def extract_slos(intents, infrastructure_description):
    message = prepare_llm_message(intents, infrastructure_description)
    print(message)
    llm_response = get_llm_response(message)
    extracted_json_response = llm_response.strip('```json').strip('```').strip()
    try:
         json_slos = json.loads(extracted_json_response)
         save_slos(json_slos)
         return json_slos
    except Exception as e:
        print(f"Error extracting the json:  {str(e)}")