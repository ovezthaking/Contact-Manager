function changeSorting() {
    const sortBy = document.getElementById('sort-select').value;
    const currentOrder = new URLSearchParams(window.location.search).get('order') || 'asc';
    const query = new URLSearchParams(window.location.search).get('q') || '';
    let url = `?sort_by=${sortBy}&order=${currentOrder}`;
    if (query) {
        url += `&q=${encodeURIComponent(query)}`;
    }
    window.location.href = url;
}
