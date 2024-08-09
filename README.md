# Web Scraping and HTML Conversion for Articles

This project provides a Python script for scraping web pages, processing the scraped data, and converting the results into a formatted HTML output. The script uses the `Firecrawl`, `OpenAI`, and `AgentOps` APIs to extract data, format it, and track the process.

## Features

- **Web Scraping with Retry Logic:** The script scrapes data from specified URLs using the `Firecrawl` API, with built-in retry logic for robust operation.
- **Data Processing:** Extracted data is processed to obtain relevant information such as publication name, summary, and more.
- **HTML Conversion:** The processed data is converted into an HTML script with specific formatting requirements using the `OpenAI` API.
- **Tracking and Logging:** The entire process is tracked and logged using the `AgentOps` API for monitoring and debugging.

## Prerequisites

Before running the script, ensure you have the following:

1. **Python 3.7+**: Make sure Python is installed on your system.
2. **API Keys**: You will need API keys for:
   - [OpenAI API](https://openai.com/)
   - [Firecrawl API](https://firecrawl.com/)
   - [AgentOps API](https://agentops.com/)
3. **Required Python Packages**: Install the required packages using `pip`:

   ```bash
   pip install firecrawl openai agentops
   ```

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Set Environment Variables**:
   - Create a `.env` file in the project root directory and add your API keys:
   ```bash
   OPENAI_API_KEY=<Your-OpenAI-API-Key>
   AGENTOPS_API_KEY=<Your-AgentOps-API-Key>
   FIRE_CRAWL_API_KEY=<Your-Firecrawl-API-Key>
   ```
   - Alternatively, you can export these keys directly in your terminal:
   ```bash
   export OPENAI_API_KEY=<Your-OpenAI-API-Key>
   export AGENTOPS_API_KEY=<Your-AgentOps-API-Key>
   export FIRE_CRAWL_API_KEY=<Your-Firecrawl-API-Key>
   ```

3. **Run the Script**:
   - Execute the script with:
   ```bash
   python script_name.py
   ```
   Replace `script_name.py` with the actual name of your script.

## Usage

1. **Scraping URLs**:
   - The script is designed to scrape a predefined list of URLs. You can modify the `urls` list in the `main()` function to include the URLs you want to scrape.

2. **Data Processing and HTML Conversion**:
   - After scraping, the data is processed and converted into an HTML string. The output includes:
     - Publication name (hyperlinked to the source).
     - Short summary of the content with the first sentence bolded and italicized.
   
3. **Output**:
   - The final HTML script is printed to the console. You can redirect this output to an HTML file if needed:
   ```bash
   python script_name.py > output.html
   ```

## Customization

- **Extraction Schema**: You can modify the extraction schema in the `scrape_with_retries()` function to match the structure of the data you want to extract from the target web pages.
- **HTML Formatting**: Adjust the HTML formatting in the `generate_html_script()` function according to your needs.

## Logging and Debugging

- The script uses the `AgentOps` API to log and track actions. This provides visibility into the scraping process and helps with debugging.
- Debugging statements are included in the `generate_html_script()` function to print the HTML string and its type before calling the OpenAI API.

## Error Handling

- The script includes retry logic to handle temporary scraping failures. If a URL fails to scrape after the specified number of retries, the process will continue with the next URL.
- If no data is scraped or the HTML conversion fails, the script will log a failure message and terminate.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
