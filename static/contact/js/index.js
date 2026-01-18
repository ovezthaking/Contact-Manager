function changeSorting() {
    const sortBy = document.getElementById('sort-select').value;
    const currentOrder = new URLSearchParams(window.location.search).get('order') || 'desc';
    window.location.href = `?sort_by=${sortBy}&order=${currentOrder}`;
}
