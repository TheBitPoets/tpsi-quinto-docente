import nunjucks from "nunjucks";

export function installViewEngine({ app, viewsDir }) {
  const loader = new nunjucks.FileSystemLoader(viewsDir, { noCache: true });
  const env = new nunjucks.Environment(loader, {
    autoescape: true,
    throwOnUndefined: true,
  });
  env.express(app);
  app.set("view engine", "njk");
  return env;
}
