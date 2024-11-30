import React from "react";

// Componente que acepta un objeto 'result' como propiedad
export const MyResult = ({ data }) => {
  return (
    <a href={data.url || "#"}>{data.name}</a> // Usa 'title' como ejemplo, ajusta según tu estructura
  );
};
