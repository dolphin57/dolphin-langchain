from markitdown import MarkItDown

def convert_pdf_to_markdown(pdf_path: str, output_path: str = None) -> str:
    """
    使用MarkItDown将PDF文件转换为Markdown格式
    
    Args:
        pdf_path: PDF文件的路径
        output_path: 输出Markdown文件的路径（可选）
    
    Returns:
        转换后的Markdown文本
    """
    md = MarkItDown()
    result = md.convert(pdf_path)
    markdown_text = result.text_content
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
    
    return markdown_text


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="将PDF文件转换为Markdown格式")
    parser.add_argument("pdf_path", help="PDF文件路径")
    parser.add_argument("-o", "--output", help="输出Markdown文件路径（可选）")
    
    args = parser.parse_args()
    
    markdown_content = convert_pdf_to_markdown(args.pdf_path, args.output)
    
    if args.output:
        print(f"转换完成！Markdown文件已保存到: {args.output}")
    else:
        print(markdown_content)
