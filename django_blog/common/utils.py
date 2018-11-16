import mistune
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name


def block_code(text, lang, inlinestyles=False, linenos=False):
    if not lang:
        text = text.strip()
        return u"<pre><code>%s</code></pre>\n" % mistune.escape(text)

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(noclasses=inlinestyles, linenos=linenos)
        code = highlight(text, lexer, formatter)
        if linenos:
            return '<div class="highlight-wrapper">%s</div>\n' % code
        return code
    except Exception:
        return '<pre class="%s"><code>%s</code></pre>\n' % (lang, mistune.escape(text))


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        inlinestyles = self.options.get("inlinestyles", False)
        linenos = self.options.get("linenos", False)
        return block_code(code, lang, inlinestyles, linenos)


renderer = HighlightRenderer()
