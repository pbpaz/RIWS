import React from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./Details.css";

const Details = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state;

  if (!result) {
    return <p>No data available</p>; // Manejo de casos donde no se pasan datos
  }

  // Función para determinar el ID del CSS según el dominio
  const getCssIdFromUrl = (url) => {
    if (url.includes("librariapaz.gal")) {
      return "LibreriaPaz";
    } else if (url.includes("planetadelibros.com")) {
      return "PlanetaLibros";
    } else if (url.includes("buscalibre.es")) {
      return "BuscaLibre";
    }
    return "UnknownDomain"; // ID por defecto si no coincide con ninguno
  };

  // Determinar el ID del CSS
  const cssId = getCssIdFromUrl(result.url.raw);

  // Asegurarse de que 'result.category' es un array antes de mapear
  const categories = Array.isArray(result.category.raw) ? result.category.raw : [];

  return (
    <div>
      <button className="ButtonHome" onClick={() => navigate("/")}>
        Home
      </button>
      <div className="BookCart">
        <img className="Cover" src={result.cover.raw} alt={result.name.raw} />
        <div className="SimpleInfo">
          <div className="title">
            <strong>{result.name.raw}</strong>
          </div>
          <div>
            <strong>{result.author.raw}</strong>
            <div className="categories">
              {categories.map((c, index) => (
                <strong key={index}>
                  {c}
                  {index < categories.length - 1 && " / "}
                </strong>
              ))}
            </div>
          </div>
          <div className="SinopsisContainer">
            <h5>{result.synopsis.raw}</h5>
          </div>
        </div>
        <div
          className="offerContainer"
          id={cssId}
          onClick={() => window.open(result.url.raw, "_blank")}
        >
          <strong>{cssId}: {result.cost.raw} €</strong>
        </div>
      </div>
    </div>
  );
};

export default Details;
