import { Component } from 'inferno';
import autobind from 'auto-bind';
import ServerApi from '../../api';
import { GlobalState, State, Events } from '../../app-state';
import styles from './index.module.scss';

export default class Bookshelf extends Component {
    constructor(props) { 
        super(props);
        autobind(this);
        GlobalState.subscribe(this, Events.LOGIN, Events.LOGOUT);
        this.state = { bookshelf: null };
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
            .then(response => {
                if(response.status == 401)
                    return Promise.reject(`User is not logged in, can't fetch bookshelf`);
                if (response.status != 200)
                    return Promise.reject(`Unknown server response: ${response.status}`);

                return response.json();
            })
            .then(json => {
                this.setState({ bookshelf: json });
                return json;
            })
            .catch(err => console.error(err));
    }

    render() {
        if(this.state.bookshelf == null || this.state.bookshelf.length == 0) {
            return (
                <div className={styles.root}>
                    <p>You don't have anything in your bookshelf... yet! Why don't you <a href='/#/new'>add a book?</a></p>
                </div>
            );
        }

        return (
            <div className={styles.root}>
            </div>
        )
    }
}
