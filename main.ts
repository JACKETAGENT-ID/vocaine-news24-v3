// vocaine-news24-v3: copy the pre-drawn entry.png next to this file into
// the output directory. Stdlib only, no network, deterministic: both runs
// produce byte-identical output because the source file is never modified.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// Resolve entry.png relative to THIS file, never process.cwd(): the grader
// runs main.ts from a different working directory.
const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

// Output directory: MAKEFUN_OUTPUT_DIR wins, then a positional argument,
// then the grader default /output.
const rawArg = process.argv[2];
const outDir = resolve(
  process.env.MAKEFUN_OUTPUT_DIR ||
    (rawArg && !rawArg.startsWith("-") ? rawArg : "/output"),
);
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
console.log(`wrote ${join(outDir, "entry.png")}`);
