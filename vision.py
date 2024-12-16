# Task:
#   * Transcribe the text in each of the 5 research paper imgs
#   * Combine the text from each img into one large transcription
#   * Provide the entire transcription to Claude & ask for a non-technical summary of the entire paper

import base64
from anthropic import Anthropic
from dotenv import load_dotenv

def summarize_paper():
    load_dotenv()
    client = Anthropic()

    research_paper_pages = [
        "./research_paper/page1.png",
        "./research_paper/page2.png",
        "./research_paper/page3.png",
        "./research_paper/page4.png",
        "./research_paper/page5.png"
    ]
    complete_transcription = ""

    for idx, page in enumerate(research_paper_pages):
        # Print progress update
        print(f"Transcribing image {idx + 1} of {len(research_paper_pages)}...", end="")

        # Open image file and encode for transmission
        with open(page, "rb") as image_file:
            binary_data = image_file.read()
        base64_encoded_data = base64.b64encode(binary_data)
        base64_string = base64_encoded_data.decode("utf-8")
        
        # Construct message
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": base64_string
                        }
                    },
                    {
                        "type": "text",
                        "text": "Transcibe the text in this image. Reply only with the transcription."
                    }
                ]
            }
        ]

        # Fetch response and save it
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            messages=messages
        )
        complete_transcription += response.content[0].text

        # Print progress update
        print("DONE!")

    # Request non-technical summary of the paper
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Give me a non-technical summary of the following research paper transcription."
                    },
                    {
                        "type": "text",
                        "text": complete_transcription
                    }
                ]
            }
        ]
    )

    # Print result
    print("\n\nResult:\n", response.content[0].text)