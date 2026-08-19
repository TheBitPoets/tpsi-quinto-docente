import express from "express";

export function installSpa(app,root){
  app.use("/vue",express.static(root));
  app.get("/vue/{*splat}",(req,res)=>res.sendFile("index.html",{root}));
}
