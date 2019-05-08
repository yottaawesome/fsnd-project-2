import { Component, linkEvent } from 'inferno';
import ServerApi from '../../api';
import styles from './styles.module.scss';

export default class ApiTest extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  onGetBookshelfClick() {
    ServerApi
      .fetchBookshelf()
      .then(json => {
        console.log(json);
        return json;
      })
      .catch(err => console.error(err));
  }

  onCreateBookClick() {
    ServerApi
      .createBook('testname', 'testdescription', 'testweblink')
      .then(json => {
        console.log(json);
        return json;
      })
      .catch(err => console.error(err));
  }

  onGetBookClick() {
    ServerApi
      .fetchBook(1)
      .then(json => {
        console.log(json);
        return json;
      })
      .catch(err => console.error(err));
  }

  onEditBookClick() {
    ServerApi
      .editBook(1, 'testnameupdated', 'testdescriptionupdated', 'testweblinkupdated')
      .then(json => {
        console.log(json);
        return json;
      })
      .catch(err => console.error(err));
  }

  onDeleteBook() {
    ServerApi
      .fetchBookshelf()
      .then(books => {
        if(books.length == 0)
          return Promise.reject('Nothing found on server to delete')
        return books[books.length-1];
      })
      .then(book => {
        return ServerApi.deleteBook(book.id);
      })
      .catch(err => console.error(`Deleet book failed: ${err}`));
  }

  render() {
    return (
      <div>
        <div><button onClick={linkEvent(this, this.onGetBookshelfClick)}>Get bookshelf</button></div>
        <div><button onClick={linkEvent(this, this.onCreateBookClick)}>Create book</button></div>
        <div><button onClick={linkEvent(this, this.onGetBookClick)}>Get book</button></div>
        <div><button onClick={linkEvent(this, this.onEditBookClick)}>Edit book</button></div>
        <div><button onClick={linkEvent(this, this.onDeleteBook)}>Delete book</button></div>
      </div>
    );
  }
}
