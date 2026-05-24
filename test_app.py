import pytest
from app import app

@pytest.fixture
def flattened_components():
    """Recursively collects all elements from the Dash app layout tree."""
    components = []
    def flatten(component):
        components.append(component)
        if hasattr(component, 'children') and component.children is not None:
            if isinstance(component.children, list):
                for child in component.children:
                    flatten(child)
            else:
                flatten(component.children)
    flatten(app.layout)
    return components

def test_header_present(flattened_components):
    """Verify the H1 header is present."""
    h1_exists = any(
        hasattr(c, 'element') and c.element == 'h1' or type(c).__name__ == 'H1'
        for c in flattened_components
    )
    assert h1_exists, "The dashboard H1 header element is missing."

def test_region_picker_present(flattened_components):
    """Verify the region picker with ID 'region-filter' is present."""
    radio_items = [c for c in flattened_components if type(c).__name__ == 'RadioItems']
    assert len(radio_items) > 0, "The region picker component is missing from the layout."
    assert radio_items[0].id == "region-filter", "The region picker component must have the ID 'region-filter'."

def test_visualization_present(flattened_components):
    """Verify the visualization graph with ID 'sales-line-chart' is present."""
    graphs = [c for c in flattened_components if type(c).__name__ == 'Graph']
    assert len(graphs) > 0, "The visualization chart component is missing from the layout."
    assert graphs[0].id == "sales-line-chart", "The visualization graph must have the ID 'sales-line-chart'."