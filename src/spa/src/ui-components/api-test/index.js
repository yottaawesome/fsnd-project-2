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
            .then(response => response.json())
            .then(json => {
                console.log(json);
                return json;
            })
            .catch(err => console.error(err));
    }

    onCreateBookClick() {
        ServerApi
            .createNewBook('testname', 'testdescription', 'testweblink')
            .then(response => response.json())
            .then(json => {
                console.log(json);
                return json;
            })
            .catch(err => console.error(err));
    }

    onGetBookClick() {
        ServerApi
            .fetchBook(1)
            .then(response => response.json())
            .then(json => {
                console.log(json);
                return json;
            })
            .catch(err => console.error(err));
    }

    onEditBookClick() {
        ServerApi
            .editBook(1, 'testnameupdated', 'testdescriptionupdated', 'testweblinkupdated')
            .then(response => response.json())
            .then(json => {
                console.log(json);
                return json;
            })
            .catch(err => console.error(err));
    }

    onDeleteBook() {
        ServerApi
            .fetchBookshelf()
            .then(response => response.json())
            .then(books => {
                if(books.length == 0)
                    Promise.reject('Nothing found on server to delete')
                return books[books.length-1];
            })
            .then(book => {
                return ServerApi.deleteBook(book.id);
            })
            .then(response => {
                if(response.status == 204)
                    return true;
                Promise.reject(`Delete failed with status ${response.status}`);
            });
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
