import json
import time
from firecrawl import FirecrawlApp
from openai import OpenAI
import os
import agentops
from agentops import record_action, track_agent

# Set API keys from environment variables (ensure these are set securely in your environment)
# os.environ["OPENAI_API_KEY"] = "<Your-OpenAI-API-Key>"
# os.environ["AGENTOPS_API_KEY"] = "<Your-AgentOps-API-Key>"
# os.environ["FIRE_CRAWL_API_KEY"] = "<Your-Firecrawl-API-Key>"
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Initialize Firecrawl app with API key
app = FirecrawlApp(api_key=os.environ["FIRE_CRAWL_API_KEY"])

# Function to scrape a URL with retry logic
def scrape_with_retries(url, retries=3, delay=5):
    for attempt in range(retries):
        try:
            # Attempt to scrape the URL
            response = app.scrape_url(
                url=url,
                params={
                    'extractorOptions': {
                        'mode': 'llm-extraction',
                        'extractionPrompt': 'Based on the information on the page, extract the information from the schema.',
                        'extractionSchema': {
                            "type": "object",
                            "properties": {
                                "supports_sso": {"type": "boolean"},
                                "is_open_source": {"type": "boolean"},
                                "short_summary": {"type": "string"},
                                "publication_name": {"type": "string"},
                                "title": {"type": "string"},
                                "url": {"type": "string"},
                            }
                        }
                    }
                }
            )
            return response
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Failed to scrape {url} after {retries} attempts.")
                return None

# Function to process the response from the scraping and extract necessary information
def process_response(url, response):
    if response and 'llm_extraction' in response:
        llm_data = response['llm_extraction']
        return {
            'supports_sso': llm_data.get('supports_sso', None),
            'is_open_source': llm_data.get('is_open_source', None),
            'short_summary': llm_data.get('short_summary', None),
            'publication_name': llm_data.get('publication_name', None),
            'title': llm_data.get('title', None),
            'url': url,
        }
    else:
        print(f"Key 'llm_extraction' not found in response for URL {url}")
        return None

# Decorator for recording the action of scraping URLs
@record_action("Scrape url")
def scrape_urls(urls):
    data = []
    for url in urls:
        print(f"Scraping URL: {url}")
        response = scrape_with_retries(url)
        if response:
            processed_data = process_response(url, response)
            if processed_data:
                data.append(processed_data)
    return data

# Decorator for recording the action of converting data to HTML
@record_action("convert to html")
def convert_to_html(data):
    html_string = ""
    for item in data:
        html_string += f"• <a href='{item['url']}'>{item['publication_name']}</a>: {item['short_summary']}<br>"
    return html_string

# Decorator for tracking the agent's operation in converting data to an HTML script
@track_agent("openai convert to html")
def generate_html_script(html_string):
    print(f"HTML String: {html_string}")  # Debugging line
    print(f"Type of html_string: {type(html_string)}")  # Debugging line

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"""
        You are given the following input string describing an article with a short summary:

        {html_string}

        Please convert this input into an HTML script where the first sentence of each item in each entry is bolded and italicized. Each entry is an item in a bulleted list. Include a period at the end of each list item. Only print the HTML. Finally, ensure that the publication name is hyperlinked to where the article is originally published.
        """}
        ]
    )

    result = response.choices[0].message.content
    return result

# Main function to orchestrate the scraping and conversion process
def main():
    agentops.init(api_key=os.environ["AGENTOPS_API_KEY"], default_tags="main")
    urls = [
        "https://www.theinformation.com/articles/skims-chime-take-new-steps-to-2025-ipos?rc=h3vnyp",
        "https://arxiv.org/pdf/2406.14283",
        "https://techcrunch.com/2024/07/30/sec-charged-crypto-founder-bitclout-startup-backed-by-a16z-sequoia/",
        "https://www.theinformation.com/articles/tiktok-spending-drove-microsofts-booming-ai-business?rc=h3vnyp",
        "https://www.newsweek.com/kamala-harris-vs-donald-trump-nate-silver-election-forecast-1932580",
        "https://www.nytimes.com/live/2024/07/31/world/israel-gaza-war-hamas-iran",
        "https://www.wired.com/story/donald-trumps-plan-to-hoard-billions-in-bitcoin-has-economists-stumped/",
        "https://www.washingtonpost.com/technology/2024/07/28/jd-vance-peter-thiel-donors-big-tech-trump-vp/",
        "https://www.washingtonpost.com/technology/2024/07/28/silicon-valley-startup-roast/",
        "https://finance.yahoo.com/news/crypto-libertarians-and-silicon-valley-billionaires-the-mashup-fueling-new-support-for-trump-113020793.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAAoxQrDfrQ7wFubbF-6bGXGRcVZSpYMGL6QSoxOVRL7QxjUGzpbJLSg_oNqr6mOalvchSlFRMCT70EyrJUMrvV_aJm3SckEH9F3f5He8c5zEtTNETggD-_CoEjwvfBsBf5aCVKwt-etgXE_0yGmMzMKeFa0mbGw6wsFbSooi0ID9"
    ]
    data = scrape_urls(urls)
    if not data:
        print("No data to process.")
    else:
        print("Scraping successful. Converting to HTML...")
        html_string = convert_to_html(data)

        if not html_string:  # Check if html_string is empty
            print("HTML string is empty. Cannot proceed.")
            agentops.end_session("Failure")
            return

    html_script = generate_html_script(html_string)
    agentops.end_session("Success")
    print(html_script)


if __name__ == "__main__":
    main()
