import ServerApi from '../../api';

const categories = 
  ServerApi
    .fetchCategories()
    .catch(err => console.error(err));

export { categories };