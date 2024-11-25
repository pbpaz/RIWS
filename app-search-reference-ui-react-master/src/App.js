import React from "react";
import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";
import ClearFilters from "./clear";
import { useEffect, useState } from "react";
import {
  ErrorBoundary,
  Facet,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Sorting,
  WithSearch
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

export default function App() {

  const [auxConfig, setConfig] = useState(config)
  const [selectedValue, setValue] = useState("Title");

  useEffect(() => {
    console.log("AAAA")
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
                            placeholder: "Introduce el título o autor del libro"
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
                      {wasSearched && (
                        <Sorting
                          label={"Sort by"}
                          sortOptions={buildSortOptionsFromConfig()}
                        />
                      )}
                      <ClearFilters></ClearFilters>
                      {getFacetFields().map(field => (
                        <Facet key={field} field={field} label={field} />
                      ))}
                    </div>
                  }
                  bodyContent={
                    <Results
                      titleField={getConfig().titleField}
                      urlField={getConfig().urlField}
                      thumbnailField={getConfig().thumbnailField}
                      shouldTrackClickThrough={true}
                    />
                  }
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
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
