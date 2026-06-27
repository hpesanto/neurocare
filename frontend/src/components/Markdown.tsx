import { type ReactNode } from "react";

// Renderizador de markdown leve, sem dependências externas.
// Cobre o subconjunto usado nos docs de ajuda: títulos (#, ##, ###),
// parágrafos, listas (-), tabelas GFM, negrito (**), código (`) e links.

function renderInline(text: string, keyBase: string): ReactNode[] {
  const nodes: ReactNode[] = [];
  // Tokeniza negrito, código inline e links.
  const regex = /(\*\*([^*]+)\*\*)|(`([^`]+)`)|(\[([^\]]+)\]\(([^)]+)\))/g;
  let last = 0;
  let m: RegExpExecArray | null;
  let i = 0;
  while ((m = regex.exec(text)) !== null) {
    if (m.index > last) nodes.push(text.slice(last, m.index));
    if (m[1]) {
      nodes.push(<strong key={`${keyBase}-b${i}`}>{m[2]}</strong>);
    } else if (m[3]) {
      nodes.push(
        <code key={`${keyBase}-c${i}`} className="px-1 rounded" style={{ background: "#eef2f1", color: "#1a3c40" }}>
          {m[4]}
        </code>
      );
    } else if (m[5]) {
      nodes.push(
        <a key={`${keyBase}-a${i}`} href={m[7]} target="_blank" rel="noreferrer">
          {m[6]}
        </a>
      );
    }
    last = regex.lastIndex;
    i++;
  }
  if (last < text.length) nodes.push(text.slice(last));
  return nodes;
}

function splitRow(line: string): string[] {
  return line
    .trim()
    .replace(/^\|/, "")
    .replace(/\|$/, "")
    .split("|")
    .map((c) => c.trim());
}

export default function Markdown({ content }: { content: string }) {
  const lines = content.split("\n");
  const blocks: ReactNode[] = [];
  let i = 0;
  let key = 0;

  while (i < lines.length) {
    const line = lines[i];

    // Linha em branco
    if (line.trim() === "") {
      i++;
      continue;
    }

    // Títulos
    const h = /^(#{1,3})\s+(.*)$/.exec(line);
    if (h) {
      const level = h[1].length;
      const text = h[2];
      const k = `b${key++}`;
      if (level === 1) blocks.push(<h4 key={k} className="fw-bold mb-3" style={{ color: "#1a3c40" }}>{renderInline(text, k)}</h4>);
      else if (level === 2) blocks.push(<h5 key={k} className="fw-semibold mt-4 mb-2" style={{ color: "#1a3c40" }}>{renderInline(text, k)}</h5>);
      else blocks.push(<h6 key={k} className="fw-semibold mt-3 mb-2 text-muted text-uppercase small">{renderInline(text, k)}</h6>);
      i++;
      continue;
    }

    // Tabela (linha com | seguida de linha separadora |---|)
    if (line.trim().startsWith("|") && i + 1 < lines.length && /^\s*\|?[\s:-]*\|[\s:|-]*$/.test(lines[i + 1])) {
      const header = splitRow(line);
      i += 2; // pula cabeçalho e separador
      const rows: string[][] = [];
      while (i < lines.length && lines[i].trim().startsWith("|")) {
        rows.push(splitRow(lines[i]));
        i++;
      }
      const k = `b${key++}`;
      blocks.push(
        <table key={k} className="table table-sm table-bordered align-middle">
          <thead className="table-light">
            <tr>{header.map((c, ci) => <th key={ci}>{renderInline(c, `${k}-h${ci}`)}</th>)}</tr>
          </thead>
          <tbody>
            {rows.map((r, ri) => (
              <tr key={ri}>{r.map((c, ci) => <td key={ci}>{renderInline(c, `${k}-r${ri}c${ci}`)}</td>)}</tr>
            ))}
          </tbody>
        </table>
      );
      continue;
    }

    // Lista (itens consecutivos começando com "- ")
    if (/^\s*-\s+/.test(line)) {
      const items: string[] = [];
      while (i < lines.length && /^\s*-\s+/.test(lines[i])) {
        items.push(lines[i].replace(/^\s*-\s+/, ""));
        i++;
      }
      const k = `b${key++}`;
      blocks.push(
        <ul key={k} className="mb-3">
          {items.map((it, ii) => <li key={ii}>{renderInline(it, `${k}-i${ii}`)}</li>)}
        </ul>
      );
      continue;
    }

    // Parágrafo (linhas consecutivas até uma linha em branco ou bloco especial)
    const para: string[] = [];
    while (
      i < lines.length &&
      lines[i].trim() !== "" &&
      !/^(#{1,3})\s+/.test(lines[i]) &&
      !lines[i].trim().startsWith("|") &&
      !/^\s*-\s+/.test(lines[i])
    ) {
      para.push(lines[i]);
      i++;
    }
    const k = `b${key++}`;
    blocks.push(<p key={k} className="mb-3">{renderInline(para.join(" "), k)}</p>);
  }

  return <div className="nc-markdown">{blocks}</div>;
}
