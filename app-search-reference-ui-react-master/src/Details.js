import React from "react";
import "./Details.css"

export const Details = ({title, cover, authors, sinopsis, categories, cost}) => {
    return(
        <div>
            <button class="ButtomHome">Home</button>
            <div class="BookCart">
                <img class="Cover" src={cover}/>
                <div class="SimpleInfo">
                    <div class="title">
                        <strong>{title}</strong>
                    </div>
                    <div>
                        {Array.isArray(authors) &&
                        authors.map((author, index) => (
                            <strong key={index}>
                            {author}
                            {index < authors.length - 1 && '/'}
                            </strong>
                        ))}
                        <div className="categories">
                            {categories.map((category, index) => (
                                <span key={index}>
                                    {category}
                                    {index < categories.length - 1 && '/'}
                                </span>
                            ))}
                        </div>
                    </div>
                </div>
                <div>
                <div class="SinopsisContainer">
                    <h5>{sinopsis}</h5>
                </div>
                <div class="offerContainer" id="LaCasaDelLibro">
                    <strong>Planeta de libros {cost} €</strong>
                </div>  
                </div>
            </div>
        </div>
    )
}

export default Details