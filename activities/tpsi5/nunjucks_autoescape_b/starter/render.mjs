import path from "node:path";
import { fileURLToPath } from "node:url";
import nunjucks from "nunjucks";

const here = path.dirname(fileURLToPath(import.meta.url));
const viewsDir = path.join(here, "templates");

// TODO: crea FileSystemLoader + Environment con autoescape e throwOnUndefined.
// TODO: renderizza post.njk e stampa l'HTML.

void nunjucks;
void viewsDir;
