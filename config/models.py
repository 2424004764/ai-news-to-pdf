from agno.models.openai.like import OpenAILike

dmxapi_base_url = "https://www.dmxapi.cn/v1"
dmxapi_api_key = "sk-8NejsU5m3uCr9KNXjGa6oIUSi6IdwfgwnMH525TyKA0PcQVy"

qwen_plus_search = OpenAILike(
    id="qwen-plus-search",
    base_url=dmxapi_base_url,
    api_key=dmxapi_api_key
)
