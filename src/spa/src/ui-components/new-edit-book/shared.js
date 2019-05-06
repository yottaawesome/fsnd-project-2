import ServerApi from '../../api';

const categories = 
  ServerApi
    .fetchCategories()
    .then(response => response.json());

export { categories };