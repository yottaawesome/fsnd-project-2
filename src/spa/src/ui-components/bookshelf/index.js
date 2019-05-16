import { Component, linkEvent } from 'inferno';
import autobind from 'auto-bind';
import ServerApi from '../../api';
import { GlobalState, State, Events } from '../../app-state';
import styles from './index.module.scss';

export default class Bookshelf extends Component {
  constructor(props) { 
    super(props);
    autobind(this);
    GlobalState.subscribe(this, Events.LOGIN, Events.LOGOUT);
    this.state = { 
      bookshelf: []
    };
  }

  componentWillUnmount() {
    GlobalState.unsubscribe(this);
  }

  componentDidMount() {
    this.fetchBookshelf();
  }

  onAppEventLogin(event, data) {
    this.fetchBookshelf();
  }

  onAppEventLogout(event, data) {
    this.setState({ bookshelf: null });
  }

  fetchBookshelf() {
    ServerApi
      .fetchBookshelf()
      .then(json => {
        this.setState({ bookshelf: json || [] });
        return json;
      })
      .catch(err => console.error(err));
    ServerApi.fetchSortedBookshelf();
  }

  deleteBook(id, index) {
    if(confirm(`Are you sure you wish to delete ${this.state.bookshelf[index].name}?`)) {
      ServerApi
        .deleteBook(id)
        .then(response => {
          this.fetchBookshelf();
          return response;
        })
        .catch(err => console.error(err));
    }
  }

  bindDeleteBookEvent(id, index) {
    return () => this.deleteBook(id, index);
  }

  render() {
    return (
      <div className={styles.root}>
        <h2>Your bookshelf</h2>
        <p><a href='/#/new'>Add a book</a></p>
        <hr />
        
        {
          this.state.bookshelf.length == 0
            ? <p>You don't have anything in your bookshelf... yet! Why don't you <a href='/#/new'>add a book?</a></p>
            : null
        }

        {
          this.state.bookshelf.map((book, index) => 
            <div>
              <h3><strong>Title:</strong> {book.name}</h3>
              <p><strong>Description:</strong> {book.description}</p>
              <p><strong>Web link:</strong> {book.web_link}</p>
              <p><strong>Author:</strong> {book.author}</p>
              <p><strong>Publisher:</strong> {book.publisher}</p>
              <a href="javascript:" onClick={linkEvent(this, this.bindDeleteBookEvent(book.id, index))}>delete</a>
              &nbsp;
              <a href={`/#/edit/${book.id}`}>edit</a>
              <hr />
            </div>
          )
        }
      </div>
    );
  }
}
