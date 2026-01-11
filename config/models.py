from agno.models.openai.like import OpenAILike

dmxapi_base_url = "https://www.dmxapi.cn/v1"
dmxapi_api_key = "sk-r6piBAN9i1ebJI7gNRbhqoNvPL7OWramQTx5VQvKGLas5xrk"

qwen_plus_search = OpenAILike(
    id="qwen-plus-search",
    base_url=dmxapi_base_url,
    api_key=dmxapi_api_key
)
