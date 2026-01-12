# 带查询参数的301重定向规则生成器

## 功能说明

此工具用于生成带查询参数的Nginx 301重定向规则，特别适用于以下场景：

- 将包含查询参数的旧URL重定向到新URL
- 生成 `location if` 格式的Nginx配置
- 批量处理带查询参数的URL重定向

## 生成的规则格式

将原来的格式：
```
location = /new_info.aspx?newsid=12262&AboutCateId=16 {
    return 301 http://www.bjng.gov.cn/article_5157.html;
}
```

转换为新的格式：
```
location = /new_info.aspx {
    if ($args = 'newsid=12262&AboutCateId=16') {
        return 301 http://www.bjng.gov.cn/article_5157.html;
    }
}
```

如果有多个相同路径但不同查询参数的URL，它们会被合并到同一个location块中：
```
location = /new_info.aspx {
    if ($args = 'newsid=12262&AboutCateId=16') {
        return 301 http://www.bjng.gov.cn/article_5222.html;
    }
    if ($args = 'newsid=12263&AboutCateId=45') {
        return 301 http://www.bjng.gov.cn/article_5157.html;
    }
}
```

## 使用方法

1. 运行程序：
   ```bash
   python query_param_redirect_generator.py
   ```

2. 在左侧文本框中输入源URL（包含查询参数），每行一个
3. 在右侧文本框中输入对应的目标URL，每行一个
4. 点击"生成301重定向规则"按钮
5. 生成的结果会显示在下方文本框中
6. 点击"复制结果到剪贴板"按钮可复制结果

## 示例

**源URL**:
```
/new_info.aspx?newsid=12262&AboutCateId=16
/new_info.aspx?newsid=12263&AboutCateId=45
/test.aspx?id=123&category=news
```

**目标URL**:
```
http://www.bjng.gov.cn/article_5157.html
http://www.bjng.gov.cn/article_5158.html
http://example.com/new_article
```

**生成结果**:
```
location = /new_info.aspx {
    if ($args = 'newsid=12262&AboutCateId=16') {
        return 301 http://www.bjng.gov.cn/article_5157.html;
    }
    if ($args = 'newsid=12263&AboutCateId=45') {
        return 301 http://www.bjng.gov.cn/article_5158.html;
    }
}

location = /test.aspx {
    if ($args = 'id=123&category=news') {
        return 301 http://example.com/new_article;
    }
}
```

## 注意事项

- 源URL必须包含查询参数（即URL中的`?`后面的部分）
- 源URL和目标URL的数量必须一致
- 程序会自动解析URL的路径部分和查询参数部分
- 如果源URL没有查询参数，则会生成普通的重定向规则