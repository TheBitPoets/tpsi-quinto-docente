import nunjucks from "nunjucks";

export function installViewEngine({ app, viewsDir }) {
  // TODO: FileSystemLoader + Environment esplicito.
  // Vincoli: autoescape:true, throwOnUndefined:true, env.express(app).
  void app;
  void viewsDir;
  void nunjucks;
}
