# JS Source Map Restorer

This Python command-line application is designed to extract frontend source code from JavaScript files using the JS source map. It navigates to a provided URL, detects and retrieves JS and JS source map files, and extracts and restores the original source code.

## Prerequisites

The following packages need to be installed to run this application:

- `requests_html`

You can install these with pip:

```
pip install requests_html
```

The rest of the packages are part of the Python Standard Library and should already be available.

## Usage

To use this script, provide the `-u` or `-url` option followed by the URL you want to process, and the `-o` or `-output` option followed by the directory you want to store the output in:

```
python restore-js-map.py -u http://example.com -o /path/to/output/dir
```

If you do not provide any arguments, the application will display a help message.

## Output

The output is a set of JavaScript source files stored in the specified output directory, organized in a folder structure that mirrors the URL structure from where they were retrieved.

The restored JavaScript source codes will be saved in a location following this pattern: `{output_dir}/{netloc_from_url}`. The application will print this location upon completion.

## Contributing

We welcome contributions to this project. Please feel free to submit issues or PRs!

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is intended for educational purposes and legal use cases only. Please respect all applicable laws and use responsibly. The author is not responsible for misuse or for any damages that result from using this tool.

