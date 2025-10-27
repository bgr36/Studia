exports.buildQuery = query => {
  const page  = parseInt(query.page)  || 1;
  const limit = parseInt(query.limit) || 10;
  const skip  = (page - 1) * limit;

  // Budowanie filtrów
  const filter = {};
  for (const key of ['name','price','username']) {
    if (query[key]) filter[key] = query[key];
  }

  // Sortowanie
  const sort = {};
  if (query.sort) sort[query.sort] = query.order === 'desc' ? -1 : 1;

  return { filter, sort, pagination: { skip, limit } };
};