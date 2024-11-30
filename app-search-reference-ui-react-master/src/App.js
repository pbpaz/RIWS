import React from "react";
import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";
import ClearFilters from "./clear";
import { useEffect, useState } from "react";
import "./books.css"
import { BooleanFacet, MultiCheckboxFacet, SingleLinksFacet, SingleSelectFacet } from "@elastic/react-search-ui-views";
import Details from "./Details";

import {
  ErrorBoundary,
  Facet,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  WithSearch,
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

import {
  buildAutocompleteQueryConfig,
  buildFacetConfigFromConfig,
  buildSearchOptionsFromConfig,
  buildSortOptionsFromConfig,
  getConfig,
  getFacetFields
} from "./config/config-helper";

const { hostIdentifier, searchKey, endpointBase, engineName } = getConfig();
const connector = new
ElasticsearchAPIConnector( {host:"http://localhost:9200", index: "books"});


const config = {
  debug: true,
  searchQuery: {
    facets: buildFacetConfigFromConfig(),
    ...buildSearchOptionsFromConfig()
  },
  autocompleteQuery: buildAutocompleteQueryConfig(),
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true
};

const omitFields = (result, fieldsToRemove) => {
  const newResult = { ...result };
  fieldsToRemove.forEach((field) => {
    delete newResult[field]; // Remove field from the copy
  });
  return newResult;
};

export default function App() {

  const [auxConfig, setConfig] = useState(config);
  const [selectedValue, setValue] = useState("Title");
  const [viewDetails, setViewDetials] = useState(false);

  useEffect(() => {
    console.log(auxConfig)
  },[auxConfig]);

  const changeConfig = (selector) => {
    setValue(selector)
    setConfig({
      debug: true,
      searchQuery: {
        facets: buildFacetConfigFromConfig(),
        ...buildSearchOptionsFromConfig(selector)
      },
      autocompleteQuery: buildAutocompleteQueryConfig(selector),
      apiConnector: connector,
      alwaysSearchOnInitialLoad: true})
  };

  const viewDetailsClick = (value) => (
    setViewDetials(value)
  )


  return (
    <SearchProvider id="search-provider" config={auxConfig}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                
                  header={<SearchBox inputView={({ getAutocomplete, getInputProps, getButtonProps }) => (
                    <>
                      <button>Inicio</button>
                      <select onChange={(e) => changeConfig(e.target.value)} name="cars" id="cars" value={selectedValue}> 
                        <option value="default">Por defecto</option>
                        <option value="author">Autor</option>
                        <option value="name">Título</option>
                        <option value="isbn">ISBN</option>
                        <option value="synopsis">Descripción</option>
                    </select>
                      <div className="sui-search-box__wrapper">
                        <input
                          {...getInputProps({
                            placeholder: "Introduce el título, autor, ISBN..."
                          })}
                        />
                        {getAutocomplete()}
                      </div>
                      <input
                        {...getButtonProps({
                          "data-custom-attr": "some value"
                        })}
                      />
                    </>
                  )}
                  autocompleteSuggestions = "true" />}
                  sideContent={
                    <div>
                      <ClearFilters></ClearFilters>
                      <Facet field="category.raw" label="Categorias" view={MultiCheckboxFacet} />
                      <Facet field="cost" label="Precio" view={MultiCheckboxFacet} />
                      <Facet field="pages" label="Páginas" view={MultiCheckboxFacet} />
                      
                    </div>
                  }
                  bodyContent={
                    <Results
                    resultView={({ result }) => {
                      if (viewDetails == false) {
                        return (
                          <div className="grid-container" onClick={() => viewDetailsClick(true)}>
                            <img className="cover" src={result.cover.raw} alt="Cover" />
                            <div className="info">
                              <h1>{result.name.raw}</h1>
                              <h2>{result.author.raw}</h2>
                              <p className="basic">
                                {result.synopsis.raw.slice(0, 500)}
                                {result.synopsis.raw.length > 500 && '...'}
                              </p>
                              <p className="p-cost">{result.cost.raw} €</p>
                            </div>
                          </div>
                        );
                      } else {
                        return <Details title={result.name.raw}
                          authors={result.author}
                          cover={result.cover.raw}
                          sinopsis={result.synopsis.raw}
                          categories={result.category.raw}
                          cost={result.cost.raw}
                          onClick={() => viewDetailsClick(true)} />;
                      }
                    }}
                    />
                  }
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo/>}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
  );
}
