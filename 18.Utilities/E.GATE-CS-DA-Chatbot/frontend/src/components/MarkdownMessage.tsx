import { memo } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import rehypeHighlight from "rehype-highlight";

/**
 * Many models emit math with `\( … \)` / `\[ … \]` delimiters, which
 * remark-math doesn't recognise. Convert them to `$ … $` / `$$ … $$` so KaTeX
 * renders them. Code fences are left untouched. (Function replacers avoid the
 * `$$` special-substitution pitfall in String.replace.)
 */
function normalizeMath(input: string): string {
  const segments = input.split(/(```[\s\S]*?```|`[^`]*`)/g);
  return segments
    .map((seg, i) => {
      if (i % 2 === 1) return seg; // code span / fence — leave as-is
      return seg
        .replace(/\\\[/g, () => "$$")
        .replace(/\\\]/g, () => "$$")
        .replace(/\\\(/g, () => "$")
        .replace(/\\\)/g, () => "$");
    })
    .join("");
}

function MarkdownMessageInner({ content }: { content: string }) {
  return (
    <div className="md text-[15px] text-slate-800 dark:text-slate-100">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex, [rehypeHighlight, { detect: true }]]}
        components={{
          a: (props) => (
            <a {...props} target="_blank" rel="noreferrer noopener" />
          ),
        }}
      >
        {normalizeMath(content)}
      </ReactMarkdown>
    </div>
  );
}

export default memo(MarkdownMessageInner);
