#!/usr/bin/env node
/**
 * Extract cinematic-design text from a PDF and flag empty / screenshot / chat exports.
 *
 * Usage:
 *   node extract_pdf_design.mjs <file.pdf>
 *
 * Prints JSON:
 *   { path, totalPages, charCount, empty, screenshotLikely, chatExportLikely,
 *     cinematicLikely, excerpt, tokens, warnings }
 */
import { readFileSync } from "node:fs";
import { basename, resolve } from "node:path";
import { pathToFileURL } from "node:url";

const EMPTY_CHARS = 400;
const SCREENSHOT_CHARS = 800;

async function loadUnpdf() {
  try {
    return await import("unpdf");
  } catch {
    return await import(pathToFileURL("/workspace/node_modules/unpdf/dist/index.mjs").href);
  }
}

function collapse(s) {
  return String(s || "")
    .replace(/\u0000/g, "")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

const SHOT_PATTERNS = [
  [/establishing(?:\s+shot)?/gi, "ES"],
  [/extreme\s+wide(?:\s+shot)?/gi, "EWS"],
  [/\bwide\s+shot\b/gi, "WS"],
  [/\bfull\s+shot\b/gi, "FS"],
  [/medium\s+full|knees?\s+to\s+head/gi, "MFS"],
  [/\bcowboy(?:\s+shot)?\b|\bamerican\s+shot\b/gi, "CS"],
  [/\bmedium\s+shot\b/gi, "MS"],
  [/medium\s+close[-\s]?up|bust\s+shot/gi, "MCU"],
  [/\bclose[-\s]?up\b/gi, "CU"],
  [/extreme\s+close[-\s]?up|\binsert\s+shot\b/gi, "ECU"],
];

const CINEMATIC =
  /\b(storyboard|lookbook|screenplay|establishing|close-?up|cinemat|animatic|previz|shot list|INT\.|EXT\.|cowboy shot|full shot|medium shot)\b/i;
const CHAT_CHROME = /\b(chatgpt|claude|gemini|copilot)\b/i;
const IP_TERMS =
  /\b(starcraft|warcraft|terran|zerg|protoss|horde|alliance|marvel|disney|star wars|pokemon)\b/i;

function tokensFrom(text) {
  const shotCalls = [];
  const seen = new Set();
  for (const [re, code] of SHOT_PATTERNS) {
    re.lastIndex = 0;
    if (re.test(text) && !seen.has(code)) {
      seen.add(code);
      shotCalls.push(code);
    }
  }
  const locations = [
    ...text.matchAll(/\b(?:INT|EXT)\.\s+[A-Z0-9][A-Z0-9 .'/-]{2,60}/g),
  ].map((m) => m[0].trim());
  return { shotCalls, locations: [...new Set(locations)].slice(0, 12) };
}

async function main() {
  const file = process.argv[2];
  if (!file) {
    console.error("Usage: extract_pdf_design.mjs <file.pdf>");
    process.exit(1);
  }
  const abs = resolve(file);
  const bytes = new Uint8Array(readFileSync(abs));
  const { extractText, getDocumentProxy } = await loadUnpdf();
  const pdf = await getDocumentProxy(bytes);
  const result = await extractText(pdf, { mergePages: true });
  const raw = Array.isArray(result.text) ? result.text.join("\n\n") : result.text;
  const text = collapse(raw || "");
  const totalPages = result.totalPages ?? 0;
  const charCount = text.replace(/\s+/g, " ").length;
  const empty = charCount < EMPTY_CHARS;
  const lower = text.toLowerCase();
  const cinematicLikely = CINEMATIC.test(text);
  const chatExportLikely =
    CHAT_CHROME.test(text) &&
    (totalPages > 8 || /print to pdf|at \d{1,2}:\d{2} (am|pm)/i.test(text));
  const screenshotLikely =
    empty ||
    (totalPages >= 8 && charCount < SCREENSHOT_CHARS) ||
    (chatExportLikely && charCount < 1200);

  const warnings = [];
  if (empty) warnings.push("near-empty extractable text");
  if (screenshotLikely)
    warnings.push("likely screenshot / Print-to-PDF chat export — do not invent a bible");
  if (chatExportLikely && !cinematicLikely)
    warnings.push(
      "ChatGPT/Claude-style export without cinematic language — not a shot bible; ask for a paste",
    );
  if (IP_TERMS.test(text) || IP_TERMS.test(basename(abs)))
    warnings.push("possible copyrighted franchise — keep grammar, rebuild original names/faces");
  if (!empty && !cinematicLikely)
    warnings.push("extracted text does not look like a screenplay, lookbook, or shot list");

  const excerpt = text.slice(0, 1200);
  const out = {
    path: abs,
    name: basename(abs),
    totalPages,
    charCount,
    empty,
    screenshotLikely,
    chatExportLikely,
    cinematicLikely,
    excerpt,
    tokens: empty ? { shotCalls: [], locations: [] } : tokensFrom(text),
    warnings,
  };
  process.stdout.write(`${JSON.stringify(out, null, 2)}\n`);
}

main().catch((err) => {
  console.error(`extract failed: ${err instanceof Error ? err.message : err}`);
  process.exit(1);
});
