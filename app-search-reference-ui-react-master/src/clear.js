import { withSearch } from "@elastic/react-search-ui";

function ClearFilters({ filters, clearFilters }) {
  return (
    <div style={{ paddingBottom: "20px" }}>
      <button onClick={() => clearFilters()}
        style={{
          fontSize: "14px",
          padding: "10px 10px",
          justifyContent: "center",
          alignItems: "center",
          width: "270px", 
          height: "35px", 
        }}
        >
        Clear {filters.length} Filters
      </button>
    </div>
  );
}
export default withSearch(({ filters, clearFilters }) => ({
  filters,
  clearFilters
}))(ClearFilters);