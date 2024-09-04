import asyncio
import os
import httpx
import json
import base64
from sig_v4 import aws_sig_v4_headers


async def main():
    method = "POST"
    host = "bedrock-runtime.us-east-1.amazonaws.com"
    path = f"/model/anthropic.claude-3-sonnet-20240229-v1:0/invoke-with-response-stream"
    payload = {
        "messages": [{"role": "user", "content": "Hi, how are you?"}],
        "top_p": 1,
        "temperature": 0,
        "max_tokens": 20000,
        "anthropic_version": "bedrock-2023-05-31",
    }
    pre_auth_headers = {}
    query = {}
    headers = aws_sig_v4_headers(
        os.environ["AWS_ACCESS_KEY_ID"],
        os.environ["AWS_SECRET_ACCESS_KEY"],
        pre_auth_headers,
        "bedrock",
        "us-east-1",
        host,
        method,
        path,
        query,
        json.dumps(payload).encode(),
    )
    client = httpx.AsyncClient()
    async with client.stream(
        method, f"https://{host}{path}", headers=headers, json=payload
    ) as response:
        async for chunk in response.aiter_bytes():
            # print(chunk)
            start = chunk.find(b'{"bytes":"') + 10
            end = chunk.find(b'","p":"') + 0
            #
            # # bytes slice
            encoded_json = chunk[start:end]
            # print(encoded_json)
            #
            # # base64 decode
            decoded_json = base64.b64decode(encoded_json)
            #
            # # parse dict
            data = json.loads(decoded_json)
            print(data)


asyncio.get_event_loop().run_until_complete(main())
