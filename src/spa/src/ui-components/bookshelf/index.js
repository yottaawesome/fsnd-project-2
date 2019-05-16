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
      bookshelf: {
        totalBooks: 0,
        categories: []
      }
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
      .fetchSortedBookshelf()
      .then(json => {
        this.setState({bookshelf: json});
        return json;
      })
      .catch(err => console.error(err));
  }

  deleteBook(id, name) {
    if(confirm(`Are you sure you wish to delete ${name}?`)) {
      ServerApi
        .deleteBook(id)
        .then(response => {
          this.fetchBookshelf();
          return response;
        })
        .catch(err => console.error(err));
    }
  }

  bindDeleteBookEvent(id, name) {
    return () => this.deleteBook(id, name);
  }

  render() {
    return (
      <div className={styles.root}>
        <h2>Your bookshelf</h2>
        <p>You have {this.state.bookshelf.totalBooks} books across {this.state.bookshelf.categories.length} categories!</p>
        <p><a href='/#/new'>Add a book</a></p>
        <hr />
        
        {
          this.state.bookshelf.categories.length == 0
            ? <p>You don't have anything in your bookshelf... yet! Why don't you <a href='/#/new'>add a book?</a></p>
            : null
        }

        {
          this.state.bookshelf.categories.map((category, index) => 
            <div>
              <h3>{category.name} -- {category.books.length} {category.books.length == 1 ? 'book' : 'books'}</h3>
              {
                category.books.map((book, index) => 
                  <div className={styles.bookDetails}>
                    <h3><strong>{book.name}</strong><br /> <small>{book.author || 'No author'}, {book.publisher || 'No publisher'}</small></h3>
                    <p><strong>Description:</strong><br />{book.description || 'No description'}</p>
                    {
                      book.web_link
                        ? <span><a href={book.web_link}>web link</a>&nbsp;&nbsp;</span>
                        : null
                    }             
                    <a href={`/#/edit/${book.id}`}>edit</a>
                    &nbsp;&nbsp;
                    <a href="javascript:" onClick={linkEvent(this, this.bindDeleteBookEvent(book.id, book.name))}>delete</a>
                    <hr />
                  </div>
                )
              }
            </div>
          )
        }
      </div>
    );
  }
}
