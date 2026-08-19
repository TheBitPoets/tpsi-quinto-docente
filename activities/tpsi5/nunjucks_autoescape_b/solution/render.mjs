import path from "node:path";
import { fileURLToPath } from "node:url";
import nunjucks from "nunjucks";

const here = path.dirname(fileURLToPath(import.meta.url));
const viewsDir = path.join(here, "templates");
const loader = new nunjucks.FileSystemLoader(viewsDir, { noCache: true });
const env = new nunjucks.Environment(loader, {
  autoescape: true,
  throwOnUndefined: true,
});

const post = {
  id: "p1",
  author: "Alice",
  text: "<script>alert('x')</script>",
  canDelete: process.argv[2] !== "no-delete",
};

process.stdout.write(env.render("post.njk", { post }));
