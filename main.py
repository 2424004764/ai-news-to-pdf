import json

from jinja2 import Environment, FileSystemLoader
import datetime
from agent.news import get_news_agent
from agno.agent import Message
from dotenv import load_dotenv


def render_html(all_news, doc_title="新闻汇编", template_path='.'):
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template('news_template.html')

    rendered_html = template.render(
        doc_title=doc_title,
        current_date=datetime.date.today().strftime("%Y年%m月%d日"),
        all_news=all_news
    )
    return rendered_html


def get_news():
    user_date = "2022年5月"
    day_news_num = 1
    total_num = 2
    agent = get_news_agent()
    result = agent.run(
        input=[Message(role='user',
                       content=f"请给我提供 {user_date} 的新闻内容，每天获取{day_news_num}条新闻，总共只要{total_num}条新闻即可")],
        stream=False)
    return json.loads(result.content)


# 保存为 HTML 文件进行预览
# with open("output_news.html", "w", encoding="utf-8") as f:
#     f.write(generated_html)
# print("HTML 文件已生成：output_news.html")


def convert_html_to_pdf(html_content, output_pdf_path):
    from weasyprint import HTML

    # 可以将CSS直接嵌入HTML，也可以单独加载CSS文件
    # html_doc = HTML(string=html_content, base_url=os.getcwd()) # base_url 用于解析图片等相对路径

    # 为了处理HTML中的相对路径图片，需要提供一个基URL。
    # 如果图片是绝对路径（如 https://...），则不需要base_url
    html_doc = HTML(string=html_content)

    # 如果有额外的CSS文件，可以这样加载
    # styles = [CSS(filename='additional_styles.css')]
    # html_doc.write_pdf(output_pdf_path, stylesheets=styles)

    html_doc.write_pdf(output_pdf_path)
    print(f"PDF 文件已生成：{output_pdf_path}")


def main():
    load_dotenv()
    news_source = "api"  # model：大模型 api：api接口
    news_data = []
    if news_source == "model":
        news_data = get_news()
    elif news_source == "api":
        from spi.bochaai import BoChaAiApi

        news_api = BoChaAiApi()
        news_data = news_api.get_news(["2022-05", "2022-06"], "的中文新闻", 5)

    # print(news_data)
    # return
    print("开始生成pdf")
    generated_html = render_html(news_data, doc_title="每日AI新闻简报")
    convert_html_to_pdf(generated_html, "AI_News.pdf")


if __name__ == '__main__':
    main()
