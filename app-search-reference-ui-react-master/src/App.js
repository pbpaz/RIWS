import React from "react";
import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";
import "./books.css"
import { BooleanFacet, MultiCheckboxFacet, SingleLinksFacet, SingleSelectFacet } from "@elastic/react-search-ui-views";

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
  WithSearch,
  Result
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
  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                  header={<SearchBox 
                    autocompleteSuggestions={false} />}
                  sideContent={
                    <div>
                      {wasSearched && (
                        <Sorting
                          label={"Ordenar por"}
                          sortOptions={buildSortOptionsFromConfig()}
                        />
                      )}
                      <Facet field="category.raw" label="Categorías" view={MultiCheckboxFacet} />
                      <div id="slider"></div>

                    </div>
                  }
                  bodyContent={
                    <Results
                    resultView={({ result }) => {
                      return (
                        <div className = "grid-container">
                          <img className="cover" src={result.cover.raw}></img>
                          <div className="info">
                            <h1>{result.name.raw}</h1>
                            <h2>{result.author.raw}</h2>
                            <p className="basic">{result.synopsis.raw.slice(0, 500)}{result.synopsis.raw.length > 500 && '...'}</p>
                            <p className="p-cost">{result.cost.raw} €</p>
                          </div>
                        </div>
                      );
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
