import boto3
from botocore.exceptions import ClientError
import sys

def extract_text_from_image(image_path):
    # Initialize Textract client
    textract = boto3.client('textract')

    # Read image file
    with open(image_path, 'rb') as document:
        image_bytes = document.read()

    # Call Textract to extract text
    try:
        response = textract.detect_document_text(Document={'Bytes': image_bytes})
    except ClientError as e:
        print(f"Error calling Textract: {e}")

    # Extract text blocks
    text_blocks = []
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            text_blocks.append(item['Text'])

    return '\n'.join(text_blocks)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    text = extract_text_from_image(image_path)
    print("Extracted Text:\n", text)