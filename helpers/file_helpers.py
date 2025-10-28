import json, os


def process_llm_json_response(content, output_file_path: str = '~/output.json'):
    try:
        if output_file_path.startswith('~/'):            
            output_file_path = os.path.expanduser(output_file_path)
        
        if os.path.exists(output_file_path):
            print('File already exists! Nothing done!')
            return None
        
        data = json.loads(content)
        
        if not data:
            raise ValueError('No JSON data found in response')
        
        with open(output_file_path, 'w') as file:
            json.dump(data, file, indent=2)
        
        print(f'Successfully created {output_file_path}')
    except Exception as e:
        print(f'Error processing file: {e}')
