def pagination(request, total, page, page_size):
    # Calculate total pages
    total_pages = (total + page_size - 1) // page_size

    # Build URLs
    base_url = str(request.url).split("?")[0]

    next_url = None
    if page < total_pages:
        next_url = f"{base_url}?page={page+1}&page_size={page_size}"

    previous_url = None
    if page > 1:
        previous_url = f"{base_url}?page={page-1}&page_size={page_size}"

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "next": next_url,
        "previous": previous_url
    }