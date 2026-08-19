import express from "express";

export function installSpa(app,root){
  app.use("/vue",express.static(root));
  // BUG Express 5: wildcard non nominato.
  app.get("/vue/*",(req,res)=>res.sendFile("index.html",{root}));
}
