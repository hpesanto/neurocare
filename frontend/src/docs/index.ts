// Carrega todos os arquivos de ajuda (.md) desta pasta como texto bruto.
// O Vite resolve isso em tempo de build — nenhum fetch em runtime é necessário.
const files = import.meta.glob("./*.md", {
  query: "?raw",
  import: "default",
  eager: true,
}) as Record<string, string>;

// Indexa por "slug" (nome do arquivo sem ./ e sem .md). Ex.: "cadastro-pacientes".
const docs: Record<string, string> = {};
for (const [path, content] of Object.entries(files)) {
  const slug = path.replace(/^\.\//, "").replace(/\.md$/, "");
  docs[slug] = content;
}

// Regras para mapear a rota atual (pathname) para o slug do documento.
// A ordem importa: a primeira regra que casar é usada.
const ROUTE_RULES: { test: (p: string) => boolean; slug: string }[] = [
  // Rotas dinâmicas / casos especiais primeiro.
  { test: (p) => /^\/cadastro\/pacientes\/[^/]+$/.test(p), slug: "cadastro-paciente-detalhe" },
];

function slugFromPath(pathname: string): string {
  return pathname.replace(/^\//, "").replace(/\/$/, "").replaceAll("/", "-");
}

/** Retorna o conteúdo markdown de ajuda para a rota informada, ou null se não houver. */
export function getHelpDoc(pathname: string): string | null {
  for (const rule of ROUTE_RULES) {
    if (rule.test(pathname)) return docs[rule.slug] ?? null;
  }
  const slug = slugFromPath(pathname);
  return docs[slug] ?? null;
}

export { docs };
