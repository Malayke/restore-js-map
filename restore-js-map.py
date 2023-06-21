import json
import os
from pathlib import Path
import sys
from typing import List
from requests_html import HTMLSession
from urllib.parse import urljoin,urlparse,urlunparse
import argparse


session = HTMLSession()


def find_js(r):
    js_files = set()
    for link in r.html.find('link'):
        href = link.attrs.get('href')
        if href.endswith('.js'):
            js_files.add(href)

    for script in r.html.find('script'):
        src = script.attrs.get('src')
        if src and src.endswith('.js'):
            js_files.add(src)
    return js_files

def extract_js(js_map_content: dict, output_dir: str, url: str):
    file_location_lst: List[str] = js_map_content.get('sources') # type: ignore
    file_content_lst: List[str] = js_map_content.get('sourcesContent') # type: ignore

    all_file_with_content = dict(zip(file_location_lst,file_content_lst))

    for file_location,file_content in all_file_with_content.items():
        file_location = file_location.replace('../','')
        if file_location.startswith('webpack:///'):
            location = Path(file_location.replace('webpack:///',''))
        else:
            location = Path(file_location)
        output_location = Path(output_dir).absolute() / Path(urlparse(url).netloc) / location
        if not output_location.exists():
            os.makedirs(output_location.parent, exist_ok=True)
        if file_content:
            with open(output_location,'w') as f:
                f.write(file_content)
    
    

def main(url: str, output_dir: str):
    r = session.get(url)
    for js in find_js(r):
        js_url = urljoin(url,js)
        r = session.get(js_url)
        JS_MAP_KEYWORD = '//# sourceMappingURL='
        js_bottom_content = r.html.html[-100:] # type: ignore
        if JS_MAP_KEYWORD in r.html.html: # type: ignore
            js_map_file = js_bottom_content.split('=')[-1]
            js_map_path = str(Path(urlparse(js_url).path).parent / Path(js_map_file))
            js_map_url = urlunparse(urlparse(js_url)._replace(path=js_map_path))
            print("[*] Deptect js source map: {js_map_url}".format(js_map_url=js_map_url))
            r = session.get(js_map_url)
            js_map_content = json.loads(r.html.html) # type: ignore
            print("[*] Extracting... ")
            extract_js(js_map_content, output_dir, url)
    output_location = Path(output_dir).absolute() / Path(urlparse(url).netloc)
    print("[*] Done!")
    print("[*] Restored js source codes saved in {outout_location}".format(outout_location=output_location))
    

def parse_args():
    parser = argparse.ArgumentParser(description='Python command line application for restoring js source map')

    parser.add_argument('-u', '-url', required=True, type=str, 
                        help='URL to be processed')

    parser.add_argument('-o', '-output', required=True, type=str, 
                        help='Directory to store the output')

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args.u, args.o)
